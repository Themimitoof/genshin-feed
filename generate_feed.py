import hashlib
import json
import os
import traceback
from datetime import datetime
from typing import Dict, List

import httpx
import pycountry
import pytz
import yaml
from feedgen.feed import FeedGenerator

GENSHIN_DEFAULT_AUTHOR = "Genshin Impact communication team"
GENSHIN_NEWS_LINK = "https://genshin.hoyoverse.com/%s/news"
COUNTRY_EMOJIS = {
    "en": "🇺🇸",
    "fr": "🇫🇷",
    "zh": "🇨🇳",
    "de": "🇩🇪",
    "es": "🇪🇸",
    "id": "🇮🇩",
    "ja": "🇯🇵",
    "ko": "🇰🇷",
    "pt": "🇵🇹",
    "ru": "🇷🇺",
    "th": "🇹🇭",
    "vi": "🇻🇳",
    "default": "🌐",
}


def generate_feed(category: str, lang: str) -> FeedGenerator:
    """
    Generate a feed for the given lang and category.
    """

    feed = FeedGenerator()
    feed.id(GENSHIN_NEWS_LINK % lang)
    feed.title("Genshin Impact %s - %s" % (lang.upper(), category))
    feed.author({"name": GENSHIN_DEFAULT_AUTHOR})
    feed.link({"href": GENSHIN_NEWS_LINK % lang, "rel": "self"})
    feed.generator("Genshin-feed: https://github.com/themimitoof/genshin-feed")
    feed.icon(icon="https://genshin.hoyoverse.com/favicon.ico")
    feed.image(url="https://genshin.hoyoverse.com/favicon.ico")
    feed.language(lang)
    feed.description("%s feed of Genshin Impact in %s" % (category, lang))

    return feed


def fetch_posts(config: dict, channel_id: int) -> List[Dict]:
    """
    Fetch all posts from Mihoyo for the given channel.
    """

    feed_url = config["url"]
    post_per_pages = config["perPage"]

    posts = []

    last_page_posts = int(post_per_pages)
    page = 1

    while last_page_posts == post_per_pages:
        url = (
            f"{feed_url}?pageSize={post_per_pages}&pageNum={page}"
            f"&channelId={channel_id}"
        )
        resp = httpx.get(url, timeout=15.0)

        if (
            resp.status_code != 200
            or resp.headers["Content-Type"] == "application/json"
        ):
            raise Exception("Unable to fetch articles")

        page += 1
        posts += resp.json()["data"]["list"]
        last_page_posts = 1

    posts.sort(key=lambda d: d["start_time"])
    return posts


def generate_feed_entry(
    feed: FeedGenerator, post: dict, lang: str, category: str, timezone: str
) -> List[Dict]:
    """
    Generate a ``post_info`` dict that contains all the informations needed to create a
    post and generate the entry in the feed.
    """

    if "_generated_post_info" in post:
        post_info = post
    else:
        published_at = datetime.strptime(post["start_time"], "%Y-%m-%d %H:%M:%S")
        published_at = pytz.timezone(timezone).localize(published_at)

        post_info = {
            "id": post["id"],
            "title": post["title"],
            "author": post.get("author") or GENSHIN_DEFAULT_AUTHOR,
            "link": (
                "https://genshin.hoyoverse.com/%s/news/detail/%s" % (lang, post["id"])
            ),
            "intro": post.get("intro", "No summary available."),
            "published": published_at,
            "category": category,
            "_generated_post_info": True,
        }

        # Get the banner/thumbnail of the post
        if "ext" in post:
            for ext in post["ext"]:
                if "arrtName" in ext and ext["arrtName"] == "banner":
                    if isinstance(ext["value"], list) and len(ext["value"]) > 0:
                        post_info["banner"] = ext["value"][0]["url"]
                        break

        # Generate the content
        content = str()

        if "banner" in post_info:
            content = '<img src="%s"><br/><br/>' % post_info["banner"]

        if post_info["intro"]:
            intro = post_info["intro"]
            content += f"{intro}<br/><br/>"

        content += 'Read more on <a href="%s">%s</a>.' % (
            post_info["link"],
            post_info["title"],
        )

        post_info["content"] = content

    # Generate the feed entry
    fp = feed.add_entry()
    fp.id(post_info["id"])
    fp.title(post_info["title"])
    fp.link(href=post_info["link"])
    fp.summary(post_info["intro"])
    fp.description(post_info["intro"])
    fp.content(content=post_info["content"], type="CDATA")
    fp.published(post_info["published"])
    fp.updated(post_info["published"])

    return post_info


def update_manifest(type_: str, lang: str, category: str) -> None:
    """
    Update the manifest file ``last-updates.json`` used by static page generator for
    generating the last updates table.
    """

    path = "feed/last-updates.json"
    date_now = datetime.utcnow().isoformat()

    if not os.path.exists(path):
        with open(path, "w") as manifest_file:
            locale = "zh" if lang.startswith("zh") else lang
            language = pycountry.languages.get(alpha_2=locale)
            manifest = {
                lang: {
                    "lang_label": language.name,
                    "emoji": COUNTRY_EMOJIS.get(locale, COUNTRY_EMOJIS["default"]),
                    "feeds": {
                        category: [{"type": type_, "updated_at": date_now}],
                    },
                }
            }

            manifest_file.write(json.dumps(manifest, indent=4))
    else:
        with open(path, "r+") as manifest_file:
            manifest = json.loads(manifest_file.read())

            if lang not in manifest:
                locale = "zh" if lang.startswith("zh") else lang
                language = pycountry.languages.get(alpha_2=locale)
                manifest[lang] = {
                    "lang_label": language.name,
                    "emoji": COUNTRY_EMOJIS.get(locale, COUNTRY_EMOJIS["default"]),
                    "feeds": {},
                }

            if category not in manifest[lang]["feeds"]:
                manifest[lang]["feeds"][category] = []

            feed_found = False
            for idx, feed in enumerate(manifest[lang]["feeds"][category]):
                if feed["type"] == type_:
                    manifest[lang]["feeds"][category][idx]["updated_at"] = date_now
                    feed_found = True
                    break

            if not feed_found:
                manifest[lang]["feeds"][category].append(
                    {"type": type_, "updated_at": date_now}
                )

            manifest_file.truncate(0)
            manifest_file.seek(0)
            manifest_file.writelines(json.dumps(manifest, indent=4))


def check_feed_need_update(feed: FeedGenerator, type_: str, file_path: str) -> bool:
    """
    Calculate the checksum between the freshly generated feed and the actual one and
    check if an update is required.

    Return True if a update is needed, otherwise, it returns False.

    TODO: Do the check without the ``<update>`` (atom)/``<lastBuildDate>`` (RSS) fields.
    """

    # Check if the file exists
    if not os.path.exists(file_path):
        return True

    current_feed_checksum = None
    generated_feed_checksum = None

    # Calculate the newly generated feed checksum
    if type_ == "rss":
        feed_bytes = feed.rss_str(pretty=True)
    elif type_ == "atom":
        feed_bytes = feed.atom_str(pretty=True)
    else:
        return True

    generated_feed_checksum = hashlib.sha256(feed_bytes).hexdigest()

    # Calculate the actual feed checksum
    with open(file_path, "rb") as feed_file:
        current_feed_checksum = hashlib.sha256(feed_file.read()).hexdigest()

    return current_feed_checksum != generated_feed_checksum


def generate_feed_files(feed: FeedGenerator, lang: str, category: str) -> None:
    """
    Generate all feed files and execute the ``update_manifest`` method.
    """
    file_path = f"feed/rss-{lang}-{category}.xml"

    if not check_feed_need_update(feed, "rss", file_path):
        print(
            "Feed %r in %r doesn't not need an update. Skiping it." % (category, lang)
        )
        return

    feed.rss_file(file_path, pretty=True)
    update_manifest("rss", lang, category)

    file_path = f"feed/atom-{lang}-{category}.xml"
    feed.atom_file(file_path, pretty=True)
    update_manifest("atom", lang, category)


def generate_all_feeds() -> None:
    """
    Main method that generate all feeds by calling Mihoyo endpoints.
    """

    with open("feed.yml", "r") as conffile:
        config = yaml.load(conffile, Loader=yaml.UnsafeLoader)

    updated_feeds = 0
    feeds_errors = 0

    # Generate a feed for each category
    for lang, feeds in config["feeds"].items():
        all_posts = []

        for category, channel_id in feeds.items():
            print("Generating feed %r for %r" % (category, lang))

            try:
                timezone = config["timezones"].get(lang, "UTC")
                feed = generate_feed(category, lang)

                for post in fetch_posts(config, channel_id):
                    post_info = generate_feed_entry(
                        feed, post, lang, category, timezone
                    )
                    all_posts.append(post_info)

                generate_feed_files(feed, lang, category)
                updated_feeds += 1
            except Exception as exc:
                print("Unable to generate the feed in %r for %r" % (lang, category))
                traceback.print_exc()
                feeds_errors += 1

        # Generate a feed that aggregate all feeds
        try:
            category = "all-articles"

            print("Generating feed %r for %r" % (category, lang))
            timezone = config["timezones"].get(lang, "UTC")
            feed = generate_feed(category, lang)

            # Sort, dedup and generate the all-articles feed
            all_posts.sort(key=lambda d: d["published"])
            post_ids = []

            for post in all_posts:
                if post["id"] in post_ids:
                    continue

                generate_feed_entry(feed, post, lang, category, timezone)
                post_ids.append(post["id"])

            generate_feed_files(feed, lang, category)
            updated_feeds += 1
        except Exception as exc:
            print("Unable to generate the feed in %r for %r" % (lang, category))
            traceback.print_exc()
            feeds_errors += 1

    print(
        "Generation of the feeds is now finished. %r have been updated, %r are errored."
        % (updated_feeds, feeds_errors)
    )


if __name__ == "__main__":
    generate_all_feeds()
