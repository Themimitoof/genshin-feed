<div align="center">
  <a href="https://genshin-feed.com">
    <img src="site/static/img/genshin-feed-logo.png">
  </a>
  <p>
    Visit <a href="https://genshin-feed.com">genshin-feed.com</a> to get the
    latest RSS/Atom feeds for your reader!
  </a>
</div>
<br>

# Genshin Feed

Genshin Feed is a Atom and RSS feed generator for offical
[Genshin Impact](https://genshin.hoyoverse.com) news.

All feeds are automatically generated every hour with GitHub Actions and available on
[genshin-feed.com](https://genshin-feed.com).

The project is separated in two parts:

- `generate_feed.py`: this is the feed generator developped with Python,
  [feedgen](https://github.com/lkiesow/python-feedgen) and [httpx](https://github.com/encode/httpx).
- `site`: a Hugo website (totally overkill yes.) for [genshin-feed.com](https://genshin-feed.com).

All feeds are updated and available on [genshin-feed.com](https://genshin-feed.com). The website is
hosted and located in France (with IPv4 and IPv6 connectivity).


_Message for miHoYo_: Please don't break anything until you implemented RSS/Atom feeds on
[genshin.hoyoverse.com](https://genshin.hoyoverse.com), thanks :)

_Domain name and web hosting by [Gandi.net](https://gandi.link/f/31b9edb5) (Affiliated link)._

## About website Analytics

[genshin-feed.com](https://genshin-feed.com) uses the software [Umami](https://umami.is) as website
analytics. This solution is very neat because it is privacy-focused. No cookies stored, no IP
addresses stored and either, no visitor profiles, just a few metrics about the visits, DONE. If
have _Do Not Track_ enabled on your browser, it will respect you and will not send data to the
server. Speaking of server, the server (like the website) is hosted in France and protected by
French laws about personal data. So don't worry, we added a tracker just for having few metrics,
not for tracking you and selling your data to third-party Genshin Impact merch sellers or whatever.

If you're a developer, I highly recommend you to take a look on [Umami](https://umami.is) and other
similar privacy-focused analytics solutions.

## Contribution

Feel free to send me a pull request or opening an issue if you want to contribute to the project.
It can be for adding new feeds, enhance the code, beautify the website or for all my spelling
mistakes.

## License

Project under MIT license.

The content in generated feeds are the property of miHoYo Co., Ltd.

Genshin Feed is not affiliated with or endorsed by miHoYo Co., Ltd.

Genshin Impact is a trademark and a game owned by miHoYo Co., Ltd.

All other trademarks mentioned are the property of their respective owners.
