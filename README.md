# Genshin Feed

Genshin Feed is a Atom and RSS feed generator for offical
[Genshin Impact](https://genshin.mihoyo.com) news.

All feeds are automatically generated every hour with GitHub Actions and available on
[genshin-feed.com](https://genshin-feed.com) or in the [feed](feed) folder.

The project is separated in two parts:

 * `generate_feed.py`: this is the feed generator developped with Python,
 [feedgen](https://github.com/lkiesow/python-feedgen) and [httpx](https://github.com/encode/httpx).
 * `site`: a Hugo website (totally overkill yes.) for [genshin-feed.com](https://genshin-feed.com).

*Message for miHoYo*: Please don't break anything until you implemented RSS/Atom feeds on
[genshin.mihoyo.com](https://genshin.mihoyo.com), thanks :)


## TODO

 * [x] Add other languages to the project
 * [x] Increase the timeout of `httpx`
 * [ ] Find a way to add a `<media:content>` tag in the feeds for the post image
 * [ ] Having a better website? (If you have good CSS skills and free time, don't hesitate!)
   * [ ] Find a better way to display all languages and categories feeds than the actual table


## Contribution

Feel free to send me a pull request or opening an issue if you want to contribute to the project.
It can be for adding new feeds, enhance the code, beautify the website or for all my spelling
mistakes.


## License

Project under MIT license.
