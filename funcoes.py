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