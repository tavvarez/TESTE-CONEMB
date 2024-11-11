import xml.etree.ElementTree as ET

def parse_cte_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {'ns': 'http://www.portalfiscal.inf.br/cte'}
 
    data = {
        "numero_cte": root.find('.//ns:ide/ns:nCT', namespaces=ns).text,
        
    }
    return data

def format_conemb_line(data):
    # Defina o layout específico para o CONEMB
    # Exemplo: linha formatada com tamanhos específicos
    linha = f"{data['numero_cte'].zfill(12)}"  # ajuste conforme layout
    # Adicione outros campos ao layout
    return linha

def generate_conemb(data, output_path="CONEMB.txt"):
    with open(output_path, "w") as file:
        file.write(format_conemb_line(data) + "\n")

def main():
    xml_file = "./XML/CTE 24379.xml"
    data = parse_cte_xml(xml_file)
    generate_conemb(data)
    # Repita para DOCCOB 5.0 com formatação específica

if __name__ == "__main__":
    main()
