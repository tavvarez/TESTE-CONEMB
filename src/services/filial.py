import re

filiais = {
    "filial_sp": "010101",
    "filial_se": "020202",
    "filial_sc": "030303"
}

def validar_cnpj(cnpj):
    pattern = r'^\d{14}$'
    return bool(re.match(pattern, cnpj))

def identificar_filial(cnpj):
    if not validar_cnpj(cnpj):
        return "CNPJ Inválido."

    for filial, cnpjBialog in filiais.items():
        if cnpjBialog == cnpj:
            return filial
    return "Filial não encontrada"

