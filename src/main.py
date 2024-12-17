import functools
import os
import shutil
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_image
from markdown import extract_title, markdown_to_html_node
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from block_markdown import block_to_block_type, markdown_to_blocks

def move_files(paths, source, dest):
    if len(paths) == 0:
        return
    
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    for path in paths:
        path_source = os.path.join(source, path)
        path_dest = os.path.join(dest, path)
        if os.path.isfile(path_source):
            shutil.copy(path_source, path_dest)
        else:
            move_files(os.listdir(path_source), path_source, path_dest)

def generate_page(from_path, template_path, dest_path):
    print(f"generating content from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    markdown = f.read()
    f = open(template_path)
    template = f.read()
    
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

    f = open(dest_path, "w")
    f.write(page)
    f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path.replace("md","html"))
        return
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    paths = os.listdir(dir_path_content)
    if len(paths) == 0: return
    for path in paths:
        dest = os.path.join(dest_dir_path, path)
        source = os.path.join(dir_path_content, path)
        generate_pages_recursive(source, template_path, dest)
    
source = "static"
files = os.listdir(source)
destination = "public"
move_files(files, source, destination)

# generate_page("content/index.md", "template.html", "public/index.html")
generate_pages_recursive("content", "template.html", "public")
