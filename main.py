import xml.etree.ElementTree as ET

def parse_cte_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {'ns': 'http://www.portalfiscal.inf.br/cte'}
 
    data = []
    for ide in root.findall('.//ns:ide', namespaces=ns):
        item = {
            "numero_cte": ide.find('./ns:nCT', namespaces=ns).text,
            "bialog": root.find('.//ns:emit/ns:xNome', namespaces=ns).text,
            "tomador": root.find('.//ns:rem/ns:xNome', namespaces=ns).text,
        }
        data.append(item)
    return data

def format_conemb_line(data):
    arrayDeContent = []
    for item in data:
        linhaInicial = f"{item['bialog'].zfill(37)}" + " " + f"{item['tomador'].zfill(11)}" + "                     " + f"{item['numero_cte'].zfill(12)}"
    # linha = f"{data['numero_cte'].zfill(12)}"
    # linha = f"{data['bialog'].zfill(37)}"
    arrayDeContent.append(linhaInicial)

    return arrayDeContent
    

def generate_conemb(data, output_path="DOCCOB.txt"):
    with open(output_path, "w") as file:
        format = format_conemb_line(data)
        linhas_formatadas = format
        for linhaInicial in linhas_formatadas:
            file.write(linhaInicial + "\n")
        # file.write(format_conemb_line(data) + "\n")

def main():
    xml_file = "./XML/CTE 24379.xml"
    data = parse_cte_xml(xml_file)
    generate_conemb(data)
    # Repita para DOCCOB 5.0 com formatação específica

if __name__ == "__main__":
    main()
