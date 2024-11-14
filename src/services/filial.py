import re

filiais = {
    "35285109000105": "010101",
    "35285109000288": "020202",
    "35285109000369": "030303"
}

def validar_cnpj(cnpj):
    pattern = r'^\d{14}$'
    return bool(re.match(pattern, cnpj))

def identificar_filial(cnpj):
    if not validar_cnpj(cnpj):
        return "CNPJ Inválido."
    return filiais.get(cnpj, "Filial não encontrada")

