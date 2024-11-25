from datetime import datetime, timedelta
import re

vencimentos = {
    "16404287063580": 60, # Suzano
    "11174306000180": 3, # Sisa
    "02116946000143": 35, # JFM
    "89724447001601": 60 # Bettanin 
}

# Função para calcular a data de vencimento com base no CNPJ e data de emissão
def calcular_vencimento(cnpj, data_emissao):
    dias_vencimento = vencimentos.get(cnpj)
    if dias_vencimento is None:
        return "Vencimento não definido para esse CNPJ."
    
    data_vencimento = data_emissao + timedelta(days=dias_vencimento)
    return data_vencimento.strftime("%d%m%Y")
