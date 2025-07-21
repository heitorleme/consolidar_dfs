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

def consolidar_tabela(df):
    # Agrupamento por marca e publi, somando os "Matched Posts"
    tabela = df.groupby(['marca', 'publi'])['Matched Posts'].sum().unstack(fill_value=0)

    # Garante que as colunas "Publi" e "UGC" existam
    for col in ['Publi', 'UGC']:
        if col not in tabela.columns:
            tabela[col] = 0

    # Calcula a porcentagem de UGC sobre o total
    tabela['% UGC'] = tabela['UGC'] / (tabela['UGC'] + tabela['Publi']) * 100
    tabela['% UGC'] = tabela['% UGC'].fillna(0).map(lambda x: f"{x:.2f}%")
    tabela['Total'] = tabela['UGC'] + tabela['Publi']

    # Reorganiza as colunas na ordem desejada
    tabela = tabela[['Publi', 'UGC', 'Total', '% UGC']]
    tabela.rename_axis("Marca")
    tabela.sort_values(by="Total", inplace=True, ascending=False)

    # Opcional: resetar índice se quiser que 'marca' vire uma coluna
    # tabela = tabela.reset_index()

    return tabela
