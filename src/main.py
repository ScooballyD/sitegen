import os
import shutil
from markd import markdown_to_html


def main(path):
    clear_directory(path)
    copy_files(path)
    print("====== Finished Copy ======")
    genereant_pages_recursive("content", "template.html", "public")


def clear_directory(source):
    if not os.path.exists(source):
        raise Exception("File path nonexistent")
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    print("=== Cleared public dir ===")

def copy_files(source):
    src_dir = os.listdir(source)
    split = source.split("/", 1)
    for src in src_dir:
        if os.path.isfile(f"{source}/{src}"):
            if len(split) == 1:
                shutil.copy(f"{source}/{src}",f"public/{src}")
                print(f"copy = {source}/{src} => public/{src}")
            else:
                shutil.copy(f"{source}/{src}",f"public/{split[1]}/{src}")
                print(f"copy = {source}/{src} => public/{split[1]}/{src}")
            continue
        if len(split) == 1:
            os.mkdir(f"public/{src}")
            print(f"create dir = public/{src}")
        else:
            os.mkdir(f"public/{split[1]}/{src}")
            print(f"create dir = public/{split[1]}/{src}")
        copy_files(f"{source}/{src}")
            
def extract_title(markdown):
    markdown.split("\n")
    for split in markdown.split("\n"):
        if split.startswith("# "):
            return split.replace("#", "").strip()
        continue
    raise Exception("No primary header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        md = f.read()
    with open(template_path) as f:
        template = f.read()
    html = markdown_to_html(md).to_html()
    title = extract_title(md)
    prod = template.replace("{{ Title }}", title)
    prod = prod.replace("{{ Content }}", html)
    with open(dest_path, "w") as f:
        f.write(prod)

def genereant_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dc = os.listdir(dir_path_content)
    html = "index.html"
    for file in dc:
        if os.path.isfile(os.path.join(dir_path_content, file)):
            generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, html))
            print(f"++++++++{html}++++++++++")
            print(f"==== Finished Generating == {os.path.join(dest_dir_path, html)} ====")
            continue
        print(f"Searching dir {os.path.join(dir_path_content, file)}")
        print(f"New destination = {os.path.join(dest_dir_path, file)}")
        os.mkdir(os.path.join(dest_dir_path, file))
        genereant_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))


main("static")

