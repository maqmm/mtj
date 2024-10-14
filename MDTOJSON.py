import re
import json
import argparse
import sys

def text_to_json(text):
    lines = text.split('\n')
    root = []
    stack = [(root, -1)]  # (current_list, indent_level)

    for line in lines:
        if not line.strip():
            continue  # skip empty lines

        indent = len(line) - len(line.lstrip())
        content = line.strip()

        # pop items from stack while current indent is less than or equal to their indent
        while stack and indent <= stack[-1][1]:
            stack.pop()

        if not stack:
            root.append({content: []})
            stack.append((root[-1][content], indent))
        else:
            parent_list, parent_indent = stack[-1]
            if indent > parent_indent:
                parent_list.append({content: []})
                stack.append((parent_list[-1][content], indent))
            else:
                parent_list.append({content: []})
                stack.append((parent_list[-1][content], indent))

    return root

def read_input(input_text):
    lines = []
    for line in input_text.strip().splitlines():
        line = line.rstrip('\n')
        if not line.strip():
            continue  # skip empty lines
        indentation = len(line) - len(line.lstrip('\t'))
        level = indentation // 1  # assuming indentation unit is 1 tab
        content = line.lstrip(' ')
        lines.append((level, content))
    return lines

def build_tree(lines):
    nodes = []
    stack = []
    for idx, (level, content) in enumerate(lines):
        node = {
            'content': content,
            'level': level,
            'parent_index': None,
            'children_indices': [],
            'line_number': idx,
            'end_line': idx,  # will be updated later
        }
        while stack and nodes[stack[-1]]['level'] >= level:
            stack.pop()
        if stack:
            parent_index = stack[-1]
            node['parent_index'] = parent_index
            nodes[parent_index]['children_indices'].append(len(nodes))
        nodes.append(node)
        stack.append(len(nodes) -1)
    return nodes

def compute_end_lines(nodes):
    # post-order traversal to compute end_line for each node
    def helper(index):
        node = nodes[index]
        if not node['children_indices']:
            node['end_line'] = node['line_number']
        else:
            for child_idx in node['children_indices']:
                helper(child_idx)
            node['end_line'] = max(nodes[child_idx]['end_line'] for child_idx in node['children_indices'])
        return node['end_line']
    for i in reversed(range(len(nodes))):
        if 'end_line' not in nodes[i]:
            helper(i)

def process_node(index, nodes):
    node = nodes[index]
    sequence = []
    for child_index in node['children_indices']:
        sequence.append(child_index)
        if nodes[child_index]['children_indices']:  # node has children
            if len(sequence) >= 2:
                last_child_indices = nodes[child_index]['children_indices']
                for prev_index in sequence[:-1]:
                    # copy the children to previous nodes in the sequence
                    nodes[prev_index]['children_indices'].extend(last_child_indices)
            sequence = []
        # process the child node recursively
        process_node(child_index, nodes)
    # in case the sequence continues till the end
    if sequence and len(sequence) >=2 and nodes[sequence[-1]]['children_indices']:
        last_child_indices = nodes[sequence[-1]]['children_indices']
        for prev_index in sequence[:-1]:
            nodes[prev_index]['children_indices'].extend(last_child_indices)

def output_tree(nodes):
    output_lines = []
    def helper(index, indent):
        node = nodes[index]
        output_lines.append('  ' * indent + node['content'])
        for child_index in node['children_indices']:
            helper(child_index, indent + 1)
    # find root nodes (nodes with no parent)
    root_indices = [i for i, node in enumerate(nodes) if node['parent_index'] is None]
    for root_index in root_indices:
        helper(root_index, 0)
    return '\n'.join(output_lines)

def process_node_tom(key, value, parent_text="", fly_pie_flag = False):
    # FULL TEXT FOR LAST ITEM
    key_for_full = tag_replacer(key, 't', '')
    key_for_full = tag_replacer(key_for_full, 'i', '')
    key_for_full = tag_replacer(key_for_full, 'a', '')
    key_for_full = key_for_full.replace('<enter>', '\n')
    key_for_full = key_for_full.replace('<space>', ' ')

    current_text = parent_text + key_for_full

    # NAME FOR CURRENT ITEM
    icon = tag_matcher(key, 'i', 'default_icon_flag')
    angle = tag_matcher(key, 'a', -1)

    key = tag_replacer(key, 'i', '')
    key = tag_replacer(key, 'a', '')

    key = key.replace('<enter>', '')
    key = key.replace('<space>', ' ')

    permanent = tag_matcher(key, 'p')
    title = tag_matcher(key, 't')
    if title != '':
        key = title
    else:
        if permanent != '':
            key = permanent
        else:
            key = tag_replacer(key, 'p')
            key = tag_replacer(key, 't')

    if isinstance(value, list):
        if not value:  # if no child create "InsertText"
            icon = "📄" if icon == 'default_icon_flag' else icon

            permanent_out = tag_matcher(current_text, 'p', full = True)
            if permanent_out != '':
                current_text = ''.join(permanent_out)

            if fly_pie_flag:
                return {
                    "name": key,
                    "icon": icon,  # icon
                    "type": "InsertText",
                    "data": {
                        "text": current_text  # full text from parents
                    },
                    "angle": angle
                }
            else:
                result = {
                    "type": "text",
                    "data": {
                        "text": current_text
                    },
                    "name": key,
                    "icon": icon,
                    "iconTheme": "emoji"
                }
                if angle != -1:
                    result["angle"] = angle
                return result

        else:  # if have child create folder (menu)
            icon = "📂" if icon == 'default_icon_flag' else icon
            if fly_pie_flag:
                return {
                    "name": key,
                    "icon": icon,  # icon
                    "type": "CustomMenu",
                    "children": [process_node_tom(k, v, current_text + "", fly_pie_flag) for child in value for k, v in child.items()],
                    "angle": angle,
                    "data": {},
                    "showLabels": True,
                    "showChildLabels": True
                }
            else:
                result = {
                    "type": "submenu",
                    "data": {},
                    "name": key,
                    "icon": icon,
                    "iconTheme": "emoji",
                    "children": [process_node_tom(k, v, current_text + "", fly_pie_flag) for child in value for k, v in child.items()]
                }
                if angle != -1:
                    result["angle"] = angle
                return result

def convert_json_to_menu(json_data, icon_menu="🥝", name_menu="Root Menu", shortcut_menu="", fly_pie_flag = False):
    if fly_pie_flag:
        menu = {
            "name": name_menu,
            "icon": icon_menu,
            "type": "CustomMenu",
            "children": [],
            "id": 1,
            "shortcut": shortcut_menu,
            "angle": -1,
            "data": {},
            "centered": False,
            "touchButton": False,
            "superRMB": False,
            "showLabels": True,
            "showChildLabels": True
        }
    else:
        menu = {
            "type": "submenu",
            "name": name_menu,
            "icon": icon_menu,
            "iconTheme": "emoji",
            "children": []
        }

    # start recurs for root elements
    for item in json_data:
        for key, value in item.items():
            menu["children"].append(process_node_tom(key, value, fly_pie_flag = fly_pie_flag))

    kando_root = {
        "root": {},
        "shortcut": shortcut_menu,
        "shortcutID": "",
        "centered": False,
        "anchored": False,
        "warpMouse": False
    }
    if not fly_pie_flag:
        kando_root["root"] = menu
        return kando_root
    else:
        return menu

def tag_replacer(text, tag, replacement=r'\1'):
    #replacement by default delete tag
    result = re.sub(rf'<{tag}>(.*?)<\/{tag}>', replacement, text)
    return result

def tag_matcher(text, tag, default='', full = False):
    matches = re.findall(rf'<{tag}>(.*?)<\/{tag}>', text)
    if not matches:
        return default

    if full:
        return matches
    else:
        return matches[0]

def main():
    # parse args
    parser = argparse.ArgumentParser(description='Convert MD list to JSON format.')
    parser.add_argument('-i', '--input', required=True, help='Input MD file name')
    parser.add_argument('-o', '--output', required=True, help='Output JSON file name')
    parser.add_argument('-n', '--name', default='Converted menu', required=False, help='Menu name')
    parser.add_argument('-sc', '--shortcut', default='default', required=False, help='Menu execite shortcut')
    parser.add_argument('--flypie', action='store_true', help='JSON menu for Fly-Pie, by default for Kando')
    parser.add_argument('-p', '--print', action='store_true', help='Print output JSON to cmd out')
    args = parser.parse_args()

    # read md
    with open(args.input, 'r', encoding='utf-8') as file:
        md_text = file.read()

    lines = read_input(md_text)
    nodes = build_tree(lines)
    compute_end_lines(nodes)
    root_indices = [i for i, node in enumerate(nodes) if node['parent_index'] is None]
    for root_index in root_indices:
        process_node(root_index, nodes)
    md_text = output_tree(nodes)
    
    result = text_to_json(md_text)
    if args.shortcut == "default":
        shortcut_default = "KP_3" if args.flypie else "num3" # temp
    else:
        shortcut_default = args.shortcut

    output_menu = [convert_json_to_menu(result, name_menu=args.name, shortcut_menu=shortcut_default, fly_pie_flag = args.flypie)]
    if args.print:
        print(json.dumps(output_menu, ensure_ascii=False, indent=2))

    # write JSON
    with open(args.output, 'w', encoding='utf-8') as file:
        json.dump(output_menu, file, ensure_ascii=False, indent=2)

    print(f"Conversion completed. Output saved to {args.output}")

if __name__ == "__main__":
    main()