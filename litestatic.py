#!/usr/bin/env python3
from marko import Markdown
from pathlib import Path
from liquid import Template
from liquid import Environment
from liquid import FileSystemLoader
import os
import shutil
import frontmatter
import datetime
markdown = Markdown(extensions=['codehilite'])
import pygments
import yaml
import argparse

# Each post is a markdown file which gets parsed into an object which contains it's metadata, date,
# and HTML content (converted from the Markdown).
class Post:
    def __init__(self, name, title, date, html):
        self.name = name
        self.title = title
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        self.html = html

# generate_index_page(): Produce the index.html file which will be the front page of the website
def generate_index_page(index_page_title, site_directory, templates_directory, output_directory):
    env = Environment(loader=FileSystemLoader(f"{site_directory}/{templates_directory}/"))
    template = env.get_template("index.html")

    if not os.path.exists(f"{output_directory}"):
        os.makedirs(f"{output_directory}")

    with open(f"{site_directory}/index.md", "r") as index_file:
        index_buffer = frontmatter.load(index_file)
        index_body = markdown.convert(index_buffer.content)

    with open(f"{output_directory}/index.html", "w") as output_file:
        print(f"Generating {output_directory}/index.html")
        output_file.write(template.render(page_title=index_page_title,index_body=index_body,))

# generate_html_pages(): Produce the HTML pages out of markdown files that will make up the site
def generate_html_pages(site_directory, templates_directory, output_directory):
    env = Environment(loader=FileSystemLoader(f"{site_directory}/{templates_directory}/"))

    if not os.path.exists(f"{output_directory}"):
        os.makedirs(f"{output_directory}")

    page_files = Path(site_directory).glob("*.md")
    for page in page_files:
        with open(page, "r") as md_file:
            page_buffer = frontmatter.load(md_file)
            page_body = markdown.convert(page_buffer.content)
            page_name = str(page.with_suffix(''))
            page_name = page_name.split('/')[1]

        if not page_name == "index": # Exclude index
            if not os.path.exists(f"{output_directory}/{page_name}"):
                os.makedirs(f"{output_directory}/{page_name}")
            
            if os.path.exists(f"{site_directory}/{templates_directory}/{page_name}.html"):
                template = env.get_template(f"{page_name}.html")
            else:
                template = env.get_template("page.html")

            with open(f"{output_directory}/{page_name}/index.html", "w") as output_file:
                print(f"Generating {output_directory}/{page_name}/index.html")
                output_file.write(template.render(page_title=page_name, page_body=page_body,))

# generate_posts(): Produce an array of post objects
def generate_posts(site_directory, posts_directory):
    post_files = Path(f"{site_directory}/{posts_directory}").glob("*.md")
    
    posts = []
    for post in post_files:
        with open(post, "r") as md_file:
            # Remove the extension from the post name
            post_name = str(post.with_suffix(''))
            # Remove the site_directory and post_directory from the post name
            post_name = post_name.split('/')[2]

            post_buffer = frontmatter.load(md_file)
            post_title = post_buffer['title']
            post_date = post_buffer['date']
            post_html = markdown.convert(post_buffer.content)

            posts.append(Post(post_name, post_title, post_date, post_html))

    return posts

# generate_post_files(): Generate the html files for the posts
def generate_post_files(posts, site_directory, templates_directory, posts_directory, output_directory):
    env = Environment(loader=FileSystemLoader(f"{site_directory}/{templates_directory}/"))
    template = env.get_template("post-template.html")

    if not os.path.exists(f"{output_directory}/{posts_directory}"):
        os.makedirs(f"{output_directory}/{posts_directory}")

    for post in posts:
        if not os.path.exists(f"{output_directory}/{posts_directory}/{post.name}"):
            os.makedirs(f"{output_directory}/{posts_directory}/{post.name}")

        with open(f"{output_directory}/{posts_directory}/{post.name}/index.html", "w") as output_file:
            print(f"Generating {output_directory}/{posts_directory}/{post.name}")
            output_file.write(template.render(page_title=post.title, post_title=post.title, post_date=post.date, post_html=post.html,))

# generate_post_index(): Generate the post index
def generate_post_index(posts, site_directory, templates_directory, posts_directory, output_directory):
    posts_list = []

    for post in posts:
        posts_dict = {"title": post.title, "date": post.date, "path": f"{post.name}"} 
        posts_list.append(posts_dict)
    
    posts_data = { "posts" : posts_list }

    env = Environment(loader=FileSystemLoader(f"{site_directory}/{templates_directory}/"))
    template = env.get_template("posts-index.html")

    with open(f"{output_directory}/{posts_directory}/index.html", "w") as output_file:
        print(f"Generating {output_directory}/{posts_directory}/index.html")
        output_file.write(template.render(**posts_data))

# copy_files_to_out(): Copy the files in the files directory to the output directory
def copy_files_to_out(site_directory, files_directory, output_directory):
    shutil.copytree(f"{site_directory}/{files_directory}", output_directory, symlinks=False, ignore=None, copy_function=shutil.copy2, ignore_dangling_symlinks=False, dirs_exist_ok=True)

# main(): Main function
def main(arguments):
    site_directory = args.site_directory
    posts_directory = "posts"
    files_directory = "files"
    templates_directory = "templates"

    if not os.path.exists(site_directory):
        print("No site directory found!")
        print("Provide a site directory or create one using the site_template!")
        exit();

    output_directory = "out"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if os.path.isfile(f"{site_directory}/config.yaml"):
        config = yaml.safe_load(Path(f"{site_directory}/config.yaml").read_text()) # Read the config file
    else:
        config = yaml.safe_load(Path("config_template.yaml").read_text()) # Fall back to config_template.yaml
    
    index_page_title = config["index_page_title"]
    generate_index_page(index_page_title, site_directory, templates_directory, output_directory)
    generate_html_pages(site_directory, templates_directory, output_directory)

    if config["blog_post_generation"] == True:
        posts = generate_posts(site_directory, posts_directory)
        generate_post_files(posts, site_directory, templates_directory, posts_directory, output_directory)
        generate_post_index(posts, site_directory, templates_directory, posts_directory, output_directory)

    copy_files_to_out(site_directory, files_directory, output_directory)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("site_directory", type=str, help="The website source directory to be generated")
    parser.add_argument("output_directory", type=str, help="The directory to output the generated website")
    args = parser.parse_args()
    main(args)
