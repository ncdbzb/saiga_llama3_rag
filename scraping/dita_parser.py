import os
import re
import fnmatch
import zipfile
import xml.etree.ElementTree as Et
from logs.console_logger import console_logger


def parse_dita(dita_path) -> list[str] | None | str:
    if os.path.splitext(dita_path)[-1] == '.zip':
        with zipfile.ZipFile(dita_path, 'r') as zip_ref:
            extract_path = os.path.splitext(dita_path)[0]
            zip_ref.extractall(extract_path)
            console_logger.info(f'{dita_path} was extracted to {extract_path}')
            os.remove(dita_path)
            console_logger.info(f'{dita_path} was removed')
            dita_path = extract_path

    def get_dita_paths(directory_path: str) -> list[str]:
        dita_paths = []
        for root, dirs, files in os.walk(directory_path):
            for file in fnmatch.filter(files, '*.dita'):
                file_path = os.path.join(root, file)
                dita_paths.append(file_path)
        return dita_paths

    def extract_text_from_xml(xml_file_path: str) -> str:
        tree = Et.parse(xml_file_path)
        root = tree.getroot()

        def get_text(element) -> str:
            extracted_text = element.text if element.text else ''
            for child in element:
                extracted_text += get_text(child)
                if child.tail:
                    extracted_text += child.tail
            return extracted_text

        text = get_text(root)
        # Удаляем повторяющиеся символы переноса строки
        cleaned_text = re.sub(r'\n\s*\n', '\n', text)

        return cleaned_text

    dita_paths_list = get_dita_paths(dita_path)

    if not dita_paths_list:
        return

    # parsed_from_xml_list = list(map(lambda x: extract_text_from_xml(x), dita_paths_list))
    # Парсим текст из каждого .dita файла и собираем в одну большую строку
    very_long_string = ''.join([extract_text_from_xml(path) for path in dita_paths_list])

    # Создаем из строки список, используя перенос строки, как разделитесь, удаляем пустые элементы и лишнии пробелы
    very_long_list = list(map(lambda x: ' '.join(x.split()), filter(None, very_long_string.split('\n'))))

    # Возвращаем обратно строку с переносами строк в нужных местах
    very_long_string = '\n '.join(very_long_list)
    # print(list(filter(lambda x: x not in ('', ' '), very_long_string.split('\n'))))
    return very_long_string


