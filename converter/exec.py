import os
from lxml import etree

# Função para ler o XML e extrair o conteúdo das tags <text>, os respectivos ids e os números das linhas.
def extract_text_and_ids(xml_file):
    tree = etree.parse(xml_file)
    root = tree.getroot()
    
    text_and_ids = []
    
    # Passa por todas as linhas do XML
    for elem in root.iter('string'):  # Iterando sobre as tags <string>
        text_elem = elem.find('text')  # Procuramos pela tag <text> dentro de <string>
        if text_elem is not None:
            text = text_elem.text
            string_id = elem.attrib.get('id')
            # Pegando o número da linha real do XML usando sourceline de <text>
            line_number = text_elem.sourceline
            text_and_ids.append((line_number, string_id, text))  # Incluindo o número da linha real
    
    return text_and_ids

# Função para exportar apenas o número da linha e o conteúdo do <text> do XML
def export_texts(xml_file, output_file):
    # Extrai o conteúdo do XML (número da linha e texto)
    xml_data = extract_text_and_ids(xml_file)
    
    # Abrir o arquivo de saída para escrever o resultado
    with open(output_file, 'w', encoding='utf-8') as f:
        # Para cada (line_number, id, text) do XML
        for line_number, string_id, text in xml_data:
            # Salva o número da linha e o texto no arquivo
            f.write(f"{line_number}|<text>{text}</text>\n")

# Função para procurar o id em dois XMLs e pegar o texto do terceiro XML
def compare_texts(first_xml_file, second_xml_file, third_xml_file, output_file):
    # Extrai o conteúdo do primeiro e segundo XMLs (id e texto)
    first_xml_data = extract_text_and_ids(first_xml_file)
    second_xml_data = extract_text_and_ids(second_xml_file)
    
    # Lê o terceiro XML para pegar o texto correspondente ao ID
    third_tree = etree.parse(third_xml_file)
    third_root = third_tree.getroot()
    
    # Abrir o arquivo de saída para escrever o resultado
    with open(output_file, 'w', encoding='utf-8') as f:
        # Para cada (line_number, id, text) do primeiro XML
        for first_line_number, first_id, first_text in first_xml_data:
            # Verifica se o ID do primeiro XML existe no segundo XML e se os textos são iguais
            second_text = None
            for second_line_number, second_id, second_text_candidate in second_xml_data:
                if first_id == second_id and first_text == second_text_candidate:
                    second_text = second_text_candidate
                    break
            
            # Se os textos forem iguais, procurar o id no terceiro XML
            if second_text is not None:
                found_in_third_xml = False
                for third_elem in third_root.iter('string'):
                    if third_elem.attrib.get('id') == first_id:
                        text_elem = third_elem.find('text')
                        if text_elem is not None:
                            third_text = text_elem.text
                            # Salva o número da linha e o texto do terceiro XML no arquivo
                            f.write(f"{first_line_number}|<text>{third_text}</text>\n")
                            found_in_third_xml = True
                        break
                
                if not found_in_third_xml:
                    f.write(f"{first_line_number}|<text>Texto não encontrado no terceiro XML</text>\n")
            else:
                # Mantém o texto original do XML 1 se não encontrar no XML 2
                f.write(f"{first_line_number}|<text>{first_text}</text>\n")

# Caminhos dos arquivos XML
first_xml = ".\\source\\zrp\\gamedata\\config\\text\\eng\\xml_name.xml"
second_xml = ".\\source\\nozrp\\gamedata\\config\\text\\eng-orig\\xml_name.xml"
third_xml = ".\\source\\nozrp\\gamedata\\config\\text\\eng\\xml_name.xml"  # Caminho para o terceiro XML

# Caminho para salvar o arquivo de exportação no diretório 'converter'
export_file = ".\\converter\\" + os.path.splitext(os.path.basename(first_xml))[0] + "_export.txt"

# Caminho para salvar o arquivo de importação no diretório 'converter'
import_file = ".\\converter\\" + os.path.splitext(os.path.basename(first_xml))[0] + "_import.txt"

# Comparar os XMLs e salvar no arquivo de importação
compare_texts(first_xml, second_xml, third_xml, import_file)

# Exportar o conteúdo do primeiro XML
export_texts(first_xml, export_file)
