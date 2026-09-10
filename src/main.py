import os
import shutil
from markdown_blocks import markdown_to_html_node
import sys
def main():
    basepath = sys.argv[1] if len(sys.argv) == 2 else "/"
    print(basepath)
    copy_static_recursive()
    generate_pages_recursive("content/", "template.html", "docs/", basepath)

def copy_static_recursive():
    if os.path.exists("docs/"):
        shutil.rmtree("docs/")
        os.mkdir("docs/")
    else:
        os.mkdir("docs/")
    recursive_helper()


def recursive_helper(path="static/"):
    entries = os.listdir(path)
    for entry in entries:
        dest = os.path.join("docs/", path.removeprefix("static/"), entry)
        source = os.path.join(path, entry)
        if os.path.isfile(source):
            print("FILE: ", source, "TO: ", dest)
            shutil.copy(source, dest)
        else:
            print("DIR: ", source, "TO: ", dest)
            os.mkdir(dest)
            recursive_helper(source)


def extract_title(markdown):
    lines_list = markdown.split("\n")
    for line in lines_list:
        if line.startswith("# "):
            return line.removeprefix("# ")
    raise Exception("No header found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}") 
    f = open(from_path, 'rt')
    md_file = f.read()
    f.close()
    f = open(template_path, 'rt')
    template = f.read()
    f.close()
    nodes = markdown_to_html_node(md_file)
    html = nodes.to_html()
    title = extract_title(md_file)
    template_with_title = template.replace("{{ Title }}", title)
    template_title_content = template_with_title.replace("{{ Content }}", html)
    template_title_content = template_title_content.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    f = open(dest_path, 'w')
    f.write(template_title_content)
    f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dst_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(src_path):
            generate_page(src_path, template_path, os.path.join(dest_dir_path, "index.html"), basepath)
        else:
            generate_pages_recursive(src_path, template_path, dst_path, basepath)

if __name__ == "__main__":
    main()
