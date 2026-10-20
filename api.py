import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Puxa as credenciais de forma segura do ambiente
USUARIO = os.getenv("DB_USER")
SENHA = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORTA = os.getenv("DB_PORT")
BANCO = os.getenv("DB_NAME")

url = "https://api.api-onepiece.com/v2/fruits/en"
resposta = requests.get(url)

if resposta.status_code == 200:
    dados = resposta.json()
    df = pd.DataFrame(dados)

    df.to_csv("dados_api.csv", index=False, encoding="utf-8-sig")
    print("DataFrame criado com sucesso! Primeiras linhas:")
    print(df.head())

    # Monta a engine usando as variáveis seguras
    engine = create_engine(f'postgresql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}')

    NOME_DA_TABELA = 'list_fruits'

    df.to_sql(
        name=NOME_DA_TABELA,
        con=engine,
        if_exists="replace",
        index=False,
        schema='onepiece'
    )

    print(f"Dados enviados com sucesso para a tabela '{NOME_DA_TABELA}'!")

else:
    print(f"Erro ao acessar a API: {resposta.status_code}")