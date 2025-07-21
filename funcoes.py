import pandas as pd

def extrair_elementos(nome_ficheiro):
    if not isinstance(nome_ficheiro, str) or nome_ficheiro.strip() == "":
        return "Desconhecido", "Desconhecido", "Desconhecido"

    # Remove a extensão do arquivo
    nome_base = nome_ficheiro.replace(".csv", "").strip()

    partes = nome_base.split("_")
    if len(partes) != 3:
        return "Desconhecido", "Desconhecido", "Desconhecido"

    marca, intervalo, tipo = partes
    return marca, intervalo, tipo

# Criar coluna para categoria do influencer
def atribuir_influ_category(total_connections):
    if total_connections <= 10000:
        return "Nano"
    elif total_connections <= 200000:
        return "Micro"
    elif total_connections <= 800000:
        return "Mid"
    elif total_connections <= 2999999:
        return "Macro"
    else:
        return "Hero"
