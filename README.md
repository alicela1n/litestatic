<a href='https://ko-fi.com/S6S2A9XRF' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi6.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

# Litestatic
Tiny lightweight static site generator written in Python that uses markdown and liquid to generate a website.

# How it works
The way it works is simple by design. The `generate.py` script checks for a `site` directory, which is your website's source directory. A template `site_template` is provided as a submodule, which can be copied and modified for your site. The `(site_directory)/templates` directory contains [liquid](https://shopify.github.io/liquid/) templates for generating the html skeleton of your website. [Markdown](https://www.markdownguide.org/) is used for the webpage contents. The index.md is the markdown file that generates the front page of the website.

You can put markdown files in the site directory and have them generated as `(site_directory)/(page name)`. You can also put html in the markdown files and it will render in the body.To customize the html outside the body use templates. For javascript you can source your scripts either in the markdown files or html template. You can also have blog-style posts by putting markdown files in the `site/(posts_directory)/` directory. `posts_directory` is by default `posts`.

The name for the posts needs to be formatted as: `(posts_directory)/YYYY-MM-DD-title.md`.

The posts need to have a metadata header:
```
title: Post Title
date: YYYY-MM-DD HH:mm
```

Posts will be indexed in `/posts` which you can link in index.md or anywhere else.

The `(site_directory)/files/` directory is for any miscellaneous files that get copied to the output directory `out/`.

The generated website is outputted to the output directory ready to be deployed to a web server or wherever.

# Configuration
You can configure many things, such as blog post generation, the name of the index page, rss feed generation, and the posts directory.

To configure these things, copy the `config_template.yaml` to your site directory.

If you change the `posts_directory` you must also rename it in your site directory, since that is the directory it will look for at generation time. This will change the url where your posts are, for example if you want it to be `/blog` such as `example.com/blog` change the `posts_directory` to `blog`.

# RSS Feed Generation
You can generate an RSS feed `(posts_directory)/rss.xml` by setting `rss_feed_generation` in the `config.yaml` to `True`. You need to set a `site_url`, `language`, and `feed_description`. If you do not set an `index_page_title` it uses the `site_url` as the RSS feed title.

# How to use
First you need to install the requirements:
```
$ pip3 install -r requirements.txt
```

Next, either provide a site directory or use the template:
```
$ git submodule update --init
$ cp site-template site
```

Next, edit the site how you see fit.

Finally, to generate a website run:
```
$ python3 litestatic.py (site_directory) (output_directory)
```

To view your website locally, run a web server:
```
$ python3 -m http.server -d (output_directory)
```
