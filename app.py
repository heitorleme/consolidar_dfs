import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from funcoes import extrair_elementos
from io import BytesIO

uploaded_files = st.file_uploader("Faça o upload dos arquivos CSV", type="csv", accept_multiple_files=True)

if uploaded_files is not None:
    intervalos = [extrair_elementos(f.name)[1] for f in uploaded_files]
    
    for intervalo in intervalos:
        publi = pd.DataFrame()
        geral = pd.DataFrame()

        for file in uploaded_files:
            if intervalo not in file.name:
                continue
            
            marca = extrair_elementos(file.name)[0]

            try:
                file.seek(0)
                df_temporario = pd.read_csv(file, header=0)
                if df_temporario.empty:
                    st.warning(f"⚠️ Arquivo '{file.name}' não possui dados.")
                    continue
                        
                df_temporario.columns = df_temporario.columns.str.replace('"', '')  # Limpa espaços e aspas
                df_temporario["marca"] = marca

                st.write("Prévia do arquivo {}:".format(file.name), df_temporario.head())

                if "publi" in file.name:
                    df_temporario["publi"] = "Publi"
                    publi = pd.concat([publi, df_temporario])
                else:
                    df_temporario["publi"] = "UGC"
                    geral = pd.concat([geral, df_temporario])
            except Exception as e:
                st.error(f"Erro ao ler '{file.name}': {e}")
                continue
        
        concatenado = pd.concat([geral, publi], ignore_index=True)

        # Agrupar por 'Main Channel Name' e aplicar lógica de subtração
        if "Main Channel Name" in concatenado.columns and "Matched Posts" in concatenado.columns:
            # Separar os dois tipos
            df_publi = concatenado[concatenado["publi"] == "Publi"]
            df_ugc = concatenado[concatenado["publi"] == "UGC"]

            # Agrupar Publi por canal e somar os valores
            publi_sum = df_publi.groupby("Main Channel Name")["Matched Posts"].sum()

            # Aplicar subtração nos UGC
            def subtrai_matched(row):
                canal = row["Main Channel Name"]
                if canal in publi_sum:
                    novo_valor = row["Matched Posts"] - publi_sum[canal]
                    return max(novo_valor, 0)
                return row["Matched Posts"]

            df_ugc["Matched Posts"] = df_ugc.apply(subtrai_matched, axis=1)

            # Remover linhas com 'Matched Posts' == 0
            df_ugc = df_ugc[df_ugc["Matched Posts"] > 0]

            # Juntar novamente
            concatenado_final = pd.concat([df_ugc, df_publi], ignore_index=True)

            buffer = BytesIO()
            concatenado_final.to_excel(buffer, index=False, engine='openpyxl')
            buffer.seek(0)
            st.download_button(
            label="📥 Excel consolidado para o período de {}".format(intervalo),
            data=buffer,
            file_name="consolidado_{}.xlsx".format(intervalo),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            id = {}.format(intervalo)
            )

        else:
            st.warning("Os arquivos precisam conter as colunas 'Matched Posts' e 'Main Channel Name'. Extraia novamente os arquivos a partir do CIQ")
