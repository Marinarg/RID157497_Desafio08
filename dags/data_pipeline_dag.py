from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import os

# Diretórios para as camadas
BASE_PATH = os.path.join(os.getcwd(), "data")
BRONZE_PATH = os.path.join(BASE_PATH, "bronze")
SILVER_PATH = os.path.join(BASE_PATH, "silver")
GOLD_PATH = os.path.join(BASE_PATH, "gold")

# Função para carregar dados brutos na camada Bronze
def upload_raw_data_to_bronze():
    raw_data_path = os.path.join(BASE_PATH, "raw_data.csv")
    df = pd.read_csv(raw_data_path)
    
    # Salvando os dados brutos na camada Bronze
    os.makedirs(BRONZE_PATH, exist_ok=True)
    bronze_file = os.path.join(BRONZE_PATH, "bronze_data.csv")
    df.to_csv(bronze_file, index=False)
    print(f"Dados brutos carregados na camada Bronze: {bronze_file}")

# Função para limpar os dados da camada Bronze e salvar na camada Prata
def process_bronze_to_silver():
    bronze_file = os.path.join(BRONZE_PATH, "bronze_data.csv")
    df = pd.read_csv(bronze_file)
    
    # Remover registros com campos nulos
    df = df.dropna(subset=["name", "email", "date_of_birth"])
    
    # Corrigir formatos de emails inválidos (e-mails precisam conter "@")
    df["email"] = df["email"].apply(lambda x: x if "@" in str(x) else x.replace("example", "@example"))
    
    # Calcular idade dos usuários
    df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], errors="coerce")
    current_date = datetime.now()
    df["age"] = df["date_of_birth"].apply(lambda dob: current_date.year - dob.year if pd.notnull(dob) else None)
    
    # Remover registros com datas de nascimento inválidas
    df = df.dropna(subset=["date_of_birth"])
    
    # Salvar dados limpos na camada Prata
    os.makedirs(SILVER_PATH, exist_ok=True)
    silver_file = os.path.join(SILVER_PATH, "silver_data.csv")
    df.to_csv(silver_file, index=False)
    print(f"Dados limpos processados na camada Prata: {silver_file}")

# Função para transformar os dados da camada Prata e salvar na camada Ouro
def process_silver_to_gold():
    silver_file = os.path.join(SILVER_PATH, "silver_data.csv")
    df = pd.read_csv(silver_file)
    
    # Classificar os usuários em faixas etárias
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ["0-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100"]
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)
    
    # Agregar dados: número de usuários por faixa etária e status
    aggregated_df = (
        df.groupby(["age_group", "subscription_status"])
        .size()
        .reset_index(name="user_count")
    )
    
    # Salvar dados transformados na camada Ouro
    os.makedirs(GOLD_PATH, exist_ok=True)
    gold_file = os.path.join(GOLD_PATH, "gold_data.csv")
    aggregated_df.to_csv(gold_file, index=False)
    print(f"Dados transformados salvos na camada Ouro: {gold_file}")

# Default arguments para a DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Definição da DAG
with DAG(
    dag_id="bronze_to_gold_dag",
    default_args=default_args,
    description="Pipeline completo de dados para camadas Bronze, Prata e Ouro",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 11, 17),
    catchup=False,
) as dag:

    # Task 1: Carregar dados brutos na camada Bronze
    upload_to_bronze = PythonOperator(
        task_id="upload_raw_data_to_bronze",
        python_callable=upload_raw_data_to_bronze,
    )

    # Task 2: Limpar dados da camada Bronze e salvar na camada Prata
    bronze_to_silver = PythonOperator(
        task_id="process_bronze_to_silver",
        python_callable=process_bronze_to_silver,
    )

    # Task 3: Transformar dados da camada Prata e salvar na camada Ouro
    silver_to_gold = PythonOperator(
        task_id="process_silver_to_gold",
        python_callable=process_silver_to_gold,
    )

    # Orquestração
    upload_to_bronze >> bronze_to_silver >> silver_to_gold

