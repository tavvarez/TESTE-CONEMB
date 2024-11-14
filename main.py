import datetime
from datetime import datetime
from datetime import date
from src.services import filial 
from src.services import vencimentos 
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
            "cnpjTomador": root.find('.//ns:rem/ns:CNPJ', namespaces=ns).text,
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
            "destinatario": root.find('.//ns:dest/ns:CNPJ', namespaces=ns).text,
        }
        data.append(item)

        quantidade_cte = str(item["numCte"])
        item["qtdRegistros"] = quantidade_cte.count(item["numCte"])

        cnpj = re.sub(r'\D', '', item["cnpjBialog"])
        filial_resultado = filial.identificar_filial(cnpj)
        item["codigo_filial"] = filial_resultado
        cnpjTomador = re.sub(r'\D', '', item["cnpjTomador"])
        data_emissao = datetime.strptime(item["dataEmissao"], "%Y-%m-%dT%H:%M:%S%z")
        vencimento_resultado = vencimentos.calcular_vencimento(cnpjTomador, data_emissao)
        item["vencimento"] = vencimento_resultado
    return data

#Usar ljust() para preencher com brancos

# Variáveis úteis
tipoNota = "0"
tipoDoc = "CTE"
tipoCobranca = "BCO"
idDeRegistro0 = "000"
idDeRegistro00 = "350"
idDeRegistro1 = "351"
idDeRegistro2 = "352"
idDeRegistro3 = "353"
idDeRegistro4 = "354"
idDeRegistro5 = "355"
idDeInterCambio = "COB"
idDeDocumento = "COBRA"
banco = "BANCO COOPERATIVO SICREDI ARACAJU  2102 11535     5 I"


def format_conemb_line(data):
    arrayDeContent = []
    for item in data:
        data_emissao = datetime.strptime(item['dataEmissao'], "%Y-%m-%dT%H:%M:%S%z")
        data_formatada = data_emissao.strftime("%d%m%y%H%M")
        somente_data = data_emissao.strftime("%d%m%y")
        linhaTeste = (
                      f"{item['bialog'].zfill(37)}" + " " +
                      f"{item['tomador'].zfill(11)}" + "                     " +
                      f"{data_formatada}"
                      + idDeInterCambio +
                      f"{data_formatada}" + "9" + "\n" 
                      + idDeRegistro00 + idDeDocumento +
                      f"{data_formatada}" + "\n" + "0"
                      + idDeRegistro1 + f"{item['cnpjBialog'].zfill(14)}"
                      f"{item['bialog'].zfill(34).ljust(113)}" + "\n"
                      + idDeRegistro2 +
                      f"{item['codigo_filial'].ljust(14)}"
                      + tipoDoc + f"{item['numCte'].zfill(10)}" +
                      f"{somente_data}" +
                      f"{item["vencimento"]}"
                      f"{item['valReceber'].zfill(13)}"
                      f"{tipoCobranca.zfill(5)}"
                      f"{item['icms']}" + "\n"
                      f"{banco.zfill(91)}" + "\n"
                      + idDeRegistro3 +
                      f"{item["codigo_filial"].ljust(10)}"
                      f"{item['serieCte'].ljust(6)}" + 
                      f"{somente_data.zfill(23)}" + 
                      f"{item["cnpjTomador"]}"
                      f"{item["destinatario"]}"
                      f"{item["cnpjBialog"]}" + "\n"
                      + idDeRegistro4.ljust(5) + f"{item["chaveNf"][26:34]}"
                      f"{somente_data}"
                      f"{item['peso']}"
                      f"{item['valMercadoria']}"
                      f"{item["cnpjTomador"]}" + "\n"
                      + idDeRegistro5 + "0" +
                      f"{item["qtdRegistros".zfill(8)]}"
                      f"{item['valReceber'].zfill(13)}"
                      )
    arrayDeContent.append(linhaTeste)

    return arrayDeContent

dataAtual = date.today()
def generate_conemb(data, output_path=None):
    for item in data:
        nomeTomador = item["tomador"]
    if output_path is None:
        output_path = f"DOCCOB{nomeTomador}_{dataAtual}.txt"
    with open(output_path, "w") as file:
        linhas_formatadas = format_conemb_line(data)
        for linha in linhas_formatadas:
            file.write(linha + "\n")

def main():
    xml_file = "./XML/CTE 45143.xml"
    data = parse_cte_xml(xml_file)
    generate_conemb(data)
    print(f"Gerado o EDI em {dataAtual}")

if __name__ == "__main__":
    main()
