import datetime
from datetime import datetime
from datetime import date
from src.services import filial 
import xml.etree.ElementTree as ET
import re

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
        cnpj = re.sub(r'\D', '', item["cnpjBialog"])
        filial_resultado = filial.identificar_filial(cnpj)
        item["codigo_filial"] = filial_resultado 
        
    return data

def format_conemb_line(data):
    arrayDeContent = []
    for item in data:
        data_emissao = datetime.strptime(item['dataEmissao'], "%Y-%m-%dT%H:%M:%S%z")
        data_formatada = data_emissao.strftime("%d%m%y%H%M")
        linhaTeste = (
                      f"{item['bialog'].zfill(37)}"
                      f"{item['tomador'].zfill(11)}" + "                     " +
                      f"{data_formatada}"
                      + "COB" +
                      f"{data_formatada}" + "9" + "\n"
                      f"{data_formatada}"
                      + f"COBRA" +
                      f"{data_formatada}" + "\n" + "0"
                      "351" + f"{item['cnpjBialog'].zfill(14)}"
                      f"{item['bialog'].zfill(34)}" + "\n" +
                      "352" + f"{item['codigo_filial']}" + "\n" +
                      f"{item['icms'].zfill(10)}" + "\n"
                      f"{item['valReceber'].zfill(10)}" + "\n"
                      f"{item['valPrestServ'].zfill(10)}" + "\n"
                      f"{item['valMercadoria'].zfill(10)}" + "\n"
                      f"{item['peso'].zfill(10)}" + "\n"
                      f"{item['chaveNf'].zfill(10)}" + "\n"
                      f"{data_formatada}" + "\n"
                      f"{item['numCte'].zfill(10)}" + "\n"
                      f"{item['serieCte'].zfill(10)}" + "\n"
                      f"{item['remetente'].zfill(10)}" + "\n"
                      )
    arrayDeContent.append(linhaTeste)

    return arrayDeContent
    
dataAtual = date.today()
def generate_conemb(data, output_path=f"DOCCOB{dataAtual}.txt"):
    with open(output_path, "w") as file:
        linhas_formatadas = format_conemb_line(data)
        for linha in linhas_formatadas:
            file.write(linha + "\n")
        # file.write(format_conemb_line(data) + "\n")

def main():
    xml_file = "./XML/CTE 24379.xml"
    data = parse_cte_xml(xml_file)
    generate_conemb(data)
    print(f"Gerado o EDI em {dataAtual}")
    # Repita para DOCCOB 5.0 com formatação específica

if __name__ == "__main__":
    main()
