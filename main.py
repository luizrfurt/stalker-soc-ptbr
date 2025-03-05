import os
import xml.etree.ElementTree as ET

def process_xml_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            xml_path = os.path.join(directory, filename)
            export_path = os.path.join(directory, filename.replace(".xml", "_export.txt"))
            import_path = os.path.join(directory, filename.replace(".xml", "_import.txt"))
            
            extracted_lines = extract_text_lines(xml_path)
            write_to_file(export_path, extracted_lines)
            write_to_file(import_path, "")  # Inicialmente, o import será igual ao export

def extract_text_lines(xml_path):
    extracted_lines = []
    with open(xml_path, "r", encoding="windows-1251", errors="replace") as file:
        lines = file.readlines()
        real_line_number = 0  # Contador correto das linhas do arquivo

        for i, line in enumerate(lines):
            stripped_line = line.strip()
            real_line_number += 1  # Contabiliza todas as linhas, incluindo vazias
            
            if stripped_line.startswith("<text>"):
                extracted_lines.append(f"{real_line_number}|{stripped_line}")
    
    return extracted_lines

def write_to_file(file_path, lines):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

def update_xml_from_import(directory):
    for filename in os.listdir(directory):
        if filename.endswith("_import.txt"):
            xml_filename = filename.replace("_import.txt", ".xml")
            xml_path = os.path.join(directory, xml_filename)
            import_path = os.path.join(directory, filename)
            
            if os.path.exists(xml_path):
                apply_import_changes(xml_path, import_path)

def apply_import_changes(xml_path, import_path):
    # Lê as mudanças a partir do arquivo import.txt
    with open(import_path, "r", encoding="utf-8") as file:
        changes = [line.strip().split("|", 1) for line in file.readlines()]
    
    # Lê as linhas do XML
    with open(xml_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    # Para cada mudança, substituímos o conteúdo da tag <text> na linha correspondente
    for line_number, new_text in changes:
        line_number = int(line_number) - 1  # Ajusta para índice da lista
        
        if "<text>" in lines[line_number]:
            # Remove as tags <text> e </text> do new_text, se existirem
            if new_text.startswith("<text>") and new_text.endswith("</text>"):
                new_text = new_text[len("<text>"):len(new_text)-len("</text>")]
            
            # Encontra a posição da tag <text> e substitui apenas o conteúdo
            start = lines[line_number].find("<text>") + len("<text>")
            end = lines[line_number].find("</text>")
            lines[line_number] = lines[line_number][:start] + new_text + lines[line_number][end:]
    
    # Escreve de volta no XML com as mudanças aplicadas
    with open(xml_path, "w", encoding="utf-8") as file:
        file.writelines(lines)

def delete_txt_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            print(f"Excluído: {file_path}")

if __name__ == "__main__":
    # Altere para o diretório correto
    directory = "./release/Stalker Shadow Of Chernobyl — Tradução Pt-Br/gamedata/config/text/eng"

    # delete txts
    # delete_txt_files(directory)

    # process xmls
    process_xml_files(directory)

    # update xmls
    # update_xml_from_import(directory)
