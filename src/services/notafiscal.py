import re

tipo = {
    "chave": "0",
}

def validar_nota(nota):
    pattern = r'^\d{14}$'
    return bool(re.match(pattern, nota))

def identificar_nota(nota):
    if not validar_nota(nota):
        return "Não é uma Nota Fiscal."
    return tipo.get(nota, "Nota Fiscal não encontrada")

