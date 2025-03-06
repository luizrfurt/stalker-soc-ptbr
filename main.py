import os
import xml.etree.ElementTree as ET
import shutil

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
            
            # Verifica se o arquivo import não está vazio
            if os.path.exists(import_path) and os.path.getsize(import_path) > 0:
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

def copy_xml_from_import(source_dir, target_dir):
    # Create target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Iterate through files in source directory
    for filename in os.listdir(source_dir):
        # Check if file is a text file with "_import" in the name
        if filename.endswith('.txt') and '_import' in filename:
            import_path = os.path.join(source_dir, filename)
            
            # Check if file exists and is not empty
            if os.path.exists(import_path) and os.path.getsize(import_path) > 0:
                # Construct corresponding XML filename
                xml_filename = filename.replace('_import.txt', '.xml')
                source_xml_path = os.path.join(source_dir, xml_filename)
                
                # Check if corresponding XML exists
                if os.path.exists(source_xml_path):
                    # Construct target path
                    target_xml_path = os.path.join(target_dir, xml_filename)
                    
                    try:
                        # Copy XML to target directory, replacing if it exists
                        shutil.copy2(source_xml_path, target_xml_path)
                        print(f"Copied: {xml_filename} to {target_dir}")
                    except Exception as e:
                        print(f"Error copying {xml_filename}: {str(e)}")
                else:
                    print(f"XML not found for: {filename}")
            else:
                print(f"Skipping empty or non-existent file: {filename}")

def remove_accents_and_cedilla(directory):
    """Remove acentos e substitui 'ç' por 'c' em todos os arquivos _import.txt."""
    for filename in os.listdir(directory):
        if filename.endswith("_import.txt"):
            import_path = os.path.join(directory, filename)
            
            # Verifica se o arquivo existe e não está vazio
            if os.path.exists(import_path) and os.path.getsize(import_path) > 0:
                # Lê o conteúdo do arquivo
                with open(import_path, "r", encoding="utf-8") as file:
                    content = file.read()
                
                # Remove acentos e substitui 'ç' por 'c'
                new_content = normalize('NFKD', content).encode('ASCII', 'ignore').decode('ASCII')
                new_content = new_content.replace('ç', 'c').replace('Ç', 'C')
                
                # Escreve o conteúdo modificado de volta no arquivo
                with open(import_path, "w", encoding="utf-8") as file:
                    file.write(new_content)
                print(f"Caracteres processados em: {filename}")
            else:
                print(f"Arquivo vazio ou inexistente, pulando: {filename}")

if __name__ == "__main__":
    # Altere para o diretório correto
    source_directory = "./release/Stalker Shadow Of Chernobyl — Tradução Pt-Br/gamedata/config/text/eng"
    target_directory = "C:/Program Files (x86)/Steam/steamapps/common/STALKER Shadow of Chernobyl/gamedata/config/text/eng"

    # delete txts
    # delete_txt_files(source_directory)

    # process xmls
    process_xml_files(source_directory)

    # Nova etapa: remover acentos e cedilha dos arquivos _import.txt
    # remove_accents_and_cedila(source_directory)

    # update xmls
    # update_xml_from_import(source_directory)

    # copy xmls
    # copy_xml_from_import(source_directory, target_directory)