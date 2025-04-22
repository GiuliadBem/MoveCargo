import re

def validar_cpf(cpf: str) -> bool:
    
    #Valida se o CPF está no formato '000.000.000-00'.
    padrao = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
    return bool(re.fullmatch(padrao, cpf))