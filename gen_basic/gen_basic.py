import markdown
import os
import sys

def read_all_to_list(path):
    f = open(path, "r")
    line_list = [line for line in f]
    f.close()
    return line_list

def read_all_to_string(path):
    return "".join(read_all_to_list(path))

def write_all_to_file(path, content):
    f = open(path, "w")
    f.write(content)
    f.close()

def template_transform(source, \
                       page_title=None, \
                       page_body=None, \
                       page_nav=None):
    return source.replace("{{{page.title}}}", page_title) \
                 .replace("{{{page.nav}}}", page_nav) \
                 .replace("{{{page.body}}}", page_body)

template_body = read_all_to_string("gen_basic/template-basic.html")
template_nav = read_all_to_list("template-nav.html")

def run_transform_for(markdown_path):
    global template_body, template_nav

    destination = markdown_path.replace("markdown/", "output/") \
                               .replace(".md", ".html")

    markdown_body_list = read_all_to_list(markdown_path)
    page_title = markdown_body_list[0]

    if page_title.startswith("@title: ") == False:
        print("gen_simple.py: %s should start with '@title: ...'." % filename_markdown)
        sys.exit(EXIT_FAILURE)

    local_nav = template_nav[:]
    nav_name = destination.replace("output/", "")

    for i in range(len(local_nav)):
        nav_item = local_nav[i]

        if nav_item.find(nav_name) != -1:
            nav_item = nav_item.replace("<li>", "<li class=\"active\">")
            local_nav[i] = nav_item
            break

    page_title = page_title.split("@title: ")[1].strip()
    local_nav = "".join(local_nav).strip()
    page_body = "".join(markdown_body_list[1:])
    page_body = markdown.markdown(page_body, \
                    extensions=["markdown.extensions.fenced_code"])

    output = template_transform(template_body, \
                                page_title=page_title, \
                                page_nav=local_nav, \
                                page_body=page_body)

    print("Generating %s." % (destination))
    write_all_to_file(destination, output)

def get_markdown_paths():
    out_paths = []
    for root, dirs, files in os.walk("markdown"):
        for f in files:
            out_paths.append(os.path.join(root, f))

    return out_paths

for path in get_markdown_paths():
    run_transform_for(path)
