import xml.etree.ElementTree as ET

def parse_cte_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {'ns': 'http://www.portalfiscal.inf.br/cte'}
 
<<<<<<< HEAD
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
=======
    data = []
    for ide in root.findall('.//ns:ide', namespaces=ns):
        item = {
            "numero_cte": ide.find('./ns:nCT', namespaces=ns).text,
            "bialog": root.find('.//ns:emit/ns:xNome', namespaces=ns).text,
            "tomador": root.find('.//ns:rem/ns:xNome', namespaces=ns).text,
            "cnpjBialog": root.find('.//ns:emit/ns:CNPJ', namespaces=ns).text,
            "icms": root.find('.//ns:Comp/ns:vComp', namespaces=ns).text,
            "valReceber": root.find('.//ns:vPrest/ns:vRec', namespaces=ns).text,
            "valPrestServ": root.find('.//ns:vPrest/ns:vTPrest', namespaces=ns).text,
            "valMercadoria": root.find('.//ns:infCarga/ns:vCarga', namespaces=ns).text,
            "peso": root.find('.//ns:infQ/ns:qCarga', namespaces=ns).text,
            "chaveNf": root.find('.//ns:infNFe/ns:chave', namespaces=ns).text,
            "dataEmissao": root.find('.//ns:ide/ns:dhEmi', namespaces=ns).text,
            "numCte": root.find('.//ns:ide/ns:nCT', namespaces=ns).text,
            "serieCte": root.find('.//ns:ide/ns:serie', namespaces=ns).text,
            "remetente": root.find('.//ns:rem/ns:CNPJ', namespaces=ns).text,
        }
        data.append(item)
    return data

def format_conemb_line(data):
    arrayDeContent = []
    for item in data:
        # linhaInicial = f"{item['bialog'].zfill(37)}" + " " + f"{item['tomador'].zfill(11)}" + "                     " + f"{item['numero_cte'].zfill(12)}"
        linhaTeste = f"{item['icms'].zfill(10)}{item['valReceber'].zfill(10)}{item['valPrestServ'].zfill(10)}{item['valMercadoria'].zfill(10)}{item['peso'].zfill(10)}{item['chaveNf'].zfill(10)}{item['dataEmissao'].zfill(10)}{item['numCte'].zfill(10)}{item['serieCte'].zfill(10)}{item['remetente'].zfill(10)}"
    # linha = f"{data['numero_cte'].zfill(12)}"
    # linha = f"{data['bialog'].zfill(37)}"
    arrayDeContent.append(linhaTeste)
>>>>>>> 79ba895 (incrementando o restante dos dados do xml)

def generate_conemb(data, output_path="CONEMB.txt"):
    with open(output_path, "w") as file:
<<<<<<< HEAD
        file.write(format_conemb_line(data) + "\n")
=======
        format = format_conemb_line(data)
        linhas_formatadas = format
        # for linhaInicial in linhas_formatadas:
        #     file.write(linhaInicial + "\n")
        for linhaTeste in linhas_formatadas:
            file.write(linhaTeste + "\n")
        # file.write(format_conemb_line(data) + "\n")
>>>>>>> 79ba895 (incrementando o restante dos dados do xml)

def main():
    xml_file = "./XML/CTE 24379.xml"
    data = parse_cte_xml(xml_file)
    generate_conemb(data)
    # Repita para DOCCOB 5.0 com formatação específica

if __name__ == "__main__":
    main()
