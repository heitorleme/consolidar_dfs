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
def atribuir_influ_category(df):
    df["influ_category"] = pd.cut(df["Total Connections"],
                                bins = [0, 10000, 200000, 800000, 2900000, float("Inf")],
                                labels = ["Nano", "Micro", "Mid", "Macro", "Hero"])
