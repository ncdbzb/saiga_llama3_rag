def parse_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        content = file.read()

    return content
