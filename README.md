<a href='https://ko-fi.com/S6S2A9XRF' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi6.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

# Litestatic
Tiny lightweight static site generator written in Python that uses markdown and liquid to generate a website.

# How it works
The way it works is simple by design. The `generate.py` script checks for a `site` directory, which is your website's source directory. A template `site_template` is provided as a submodule, which can be copied (**must be named `site`**) and modified for your site. The `site/templates` directory contains [liquid](https://shopify.github.io/liquid/) templates for generating the html skeleton of your website. [Markdown](https://www.markdownguide.org/) is used for the webpage contents. The index.md is the markdown file that generates the front page of the website.

You can put markdown files in the `site/` directory and have them generated as `site/(page name)`.
You can also have blog-style posts by putting markdown files in the `site/posts/` directory.

The name for the posts needs to be formatted as: `posts/YYYY-MM-DD-title.md`.

The posts need to have a metadata header:
```
title: Post Title
date: YYYY-MM-DD HH:mm
```

Posts will be indexed in `/posts` which you can link in index.md or anywhere else.

The `site/files/` directory is for any miscellaneous files that get copied to the output directory `out/`.

The generated website is outputted to `out/` ready to be deployed to a web server or wherever.

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

Next, edit the site how you see fit

Finally, run `generate.py` to generate a website:
```
$ python3 generate.py
```

To view your website locally, run a web server:
```
$ python3 -m http.server -d out
```

