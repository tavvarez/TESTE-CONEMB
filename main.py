import datetime
from datetime import date, datetime
import xml.etree.ElementTree as ET
import re
from src.services import filial
from src.services import vencimentos


def parse_cte_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = {'ns': 'http://www.portalfiscal.inf.br/cte'}
    data = []

    for ide in root.findall('.//ns:ide', namespaces=ns):
        try:
            # Verifica se o campo `dhEmi` existe
            data_emissao_node = root.find('.//ns:ide/ns:dhEmi', namespaces=ns)
            if data_emissao_node is None or data_emissao_node.text is None:
                raise ValueError("Campo 'dataEmissao' não encontrado no XML.")

            # Converte a data de emissão para verificar o formato
            data_emissao = datetime.strptime(data_emissao_node.text, "%Y-%m-%dT%H:%M:%S%z")

            # Cria o item com os campos esperados
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
                "dataEmissao": data_emissao_node.text,
                "numCte": ide.find('./ns:nCT', namespaces=ns).text,
                "serieCte": ide.find('./ns:serie', namespaces=ns).text,
                "remetente": root.find('.//ns:rem/ns:CNPJ', namespaces=ns).text,
                "destinatario": root.find('.//ns:dest/ns:CNPJ', namespaces=ns).text,
            }

            # identificação de filial
            cnpj = re.sub(r'\D', '', item["cnpjBialog"])
            filial_resultado = filial.identificar_filial(cnpj)
            item["codigo_filial"] = filial_resultado

            # identificação do vencimento
            cnpjTomador = re.sub(r'\D', '', item["cnpjTomador"])
            vencimento_resultado = vencimentos.calcular_vencimento(cnpjTomador, data_emissao)
            item["vencimento"] = vencimento_resultado

            data.append(item)

        except Exception as e:
            print(f"Erro ao processar item: {e}")
            continue

    return data


# Variáveis de configuração
tipoDoc = "CTE"
tipoCobranca = "BCO"
idDeRegistro = {"000": "000", "350": "350", "351": "351", "352": "352", "353": "353", "354": "354", "355": "355"}
banco = "BANCO COOPERATIVO SICREDI ARACAJU  2102 11535     5 I"

def format_conemb_line(data):
    linhas = []
    for index, item in enumerate(data):
        try:
            # validação da data de emissão presente
            if 'dataEmissao' not in item:
                raise ValueError(f"Item na posição {index} não contém 'dataEmissao'.")

            # formatação da data de emissão
            data_emissao = datetime.strptime(item['dataEmissao'], "%Y-%m-%dT%H:%M:%S%z")
            data_formatada = data_emissao.strftime("%d%m%y%H%M")
            somente_data = data_emissao.strftime("%d%m%y")

            linhas.append(f"{idDeRegistro['000']}{item['bialog'].ljust(37)}{item['tomador'].ljust(50)}{data_formatada}COB{data_formatada}9")
            linhas.append(f"{idDeRegistro['350']}COBRA{data_formatada}")
            linhas.append(f"{idDeRegistro['351']}{item['cnpjBialog'].zfill(14)}{item['bialog'].ljust(113)}")
            linhas.append(f"{idDeRegistro['352']}{item['cnpjBialog'].ljust(14)}{tipoDoc}{item['numCte'].zfill(10)}{somente_data}{item['valReceber'].zfill(13)}{tipoCobranca}")
            linhas.append(f"{banco.ljust(91)}")
            linhas.append(f"{idDeRegistro['353']}{item['codigo_filial'].ljust(10)}{item['serieCte'].ljust(6)}{somente_data}{item['cnpjTomador'].zfill(14)}")
            linhas.append(f"{idDeRegistro['354']} {item['chaveNf'][-8:]}{somente_data}{item['peso'].zfill(8)}{item['valMercadoria'].zfill(10)}")
            linhas.append(f"{idDeRegistro['355']}0{item['valReceber'].zfill(13)}")

        except Exception as e:
            print(f"Erro ao processar item {index}: {e}")
            continue

    return linhas


def generate_conemb(data):
    dataAtual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    for item in data:
        nomeTomador = re.sub(r'[^a-zA-Z0-9]', '_', item["tomador"])
        output_path = f"DOCCOB_{nomeTomador}_{dataAtual}.txt"

        with open(output_path, "w", encoding="utf-8") as file:
            linhas_formatadas = format_conemb_line(data)
            for linha in linhas_formatadas:
                file.write(linha + "\n")


def main():
    xml_file = "./XML/CTE 19082.xml"
    data = parse_cte_xml(xml_file)
    generate_conemb(data)
    print(f"Arquivo EDI gerado com sucesso!")


if __name__ == "__main__":
    main()
