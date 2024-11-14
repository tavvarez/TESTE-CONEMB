from datetime import datetime, timedelta
import re

vencimentos = {
    "16404287063580": 60,
    "35285109000288": 35,
    "35285109000369": 15
}

# Função para calcular a data de vencimento com base no CNPJ e data de emissão
def calcular_vencimento(cnpj, data_emissao):
    dias_vencimento = vencimentos.get(cnpj)
    if dias_vencimento is None:
        return "Vencimento não definido para esse CNPJ."
    
    data_vencimento = data_emissao + timedelta(days=dias_vencimento)
    return data_vencimento.strftime("%d%m%Y")
