# 🚀 Pipeline de Processamento de Dados com Apache Airflow
Este repositório contém um pipeline de dados orquestrado pelo Apache Airflow, desenvolvido para transformar dados brutos em insights valiosos. O pipeline segue a arquitetura de camadas com Bronze, Prata e Ouro, realizando limpeza, transformação e agregação de dados.

## 🛠 Tecnologias Utilizadas
- **Apache Airflow:** Orquestração de tarefas e gerenciamento do fluxo de trabalho.
- **Docker:** Contêinerização do Airflow para um ambiente controlado e portátil.
- **Pandas:** Manipulação e transformação de dados.

## 📦 Estrutura do Projeto
O projeto é composto pelas seguintes pastas e arquivos principais:

```console
├── dags/
│   └── data_pipeline_dag.py   # Definição da DAG que orquestra o pipeline de dados
│── data/
│   ├── raw_data.csv           # Arquivo de dados brutos
│   ├── bronze/                # Dados carregados e armazenados sem modificações
│   ├── silver/                # Dados limpos e preparados para análise
│   └── gold/                  # Dados transformados e prontos para decisões estratégicas
├── logs/                      # Pasta destinada para salvar os logs do Airflow
├── plugins/                   # Pasta destinada para salvar os plugins do Airflow
├── docker-compose.yml         # Arquivo para inicializar o Airflow via Docker
└── README.md                  # Este arquivo
```


## ⚙️ Como Executar o Projeto
### 1. Configuração do Ambiente
Para rodar o pipeline localmente, você precisa ter o Docker instalado. Caso não tenha, instale o Docker Desktop.

### 2. Iniciar o Apache Airflow com Docker
Após clonar este repositório, navegue até a pasta do projeto e execute os seguintes comandos no terminal para iniciar o Apache Airflow via Docker:

```console
docker-compose up -d
```

Isso iniciará os serviços necessários para o Apache Airflow. Você poderá acessar o Airflow Webserver no endereço: http://localhost:8080.

### 3. Acessar a Interface Web do Airflow
- Abra o navegador e vá para http://localhost:8080.
- O usuário e senha padrão para login são:
    - Username: `admin`
    - Password: `admin`

### 4. Rodar a DAG
Após acessar a interface do Airflow, localize a DAG `data_pipeline_dag` na lista de DAGs e clique para executá-lo.

### 5. Verificar os Resultados
Os resultados do processamento podem ser verificados nas pastas `bronze`, `silver` e `gold` dentro da pasta `data`. Cada etapa do pipeline irá salvar os dados transformados na respectiva pasta.

## 📝 Transformações Realizadas
### 1. Carregamento de Dados (Camada Bronze)
Os dados brutos do arquivo `data/raw_data.csv` são carregados para a camada Bronze sem transformações. O arquivo original contém dados de usuários com algumas inconsistências que precisam ser corrigidas nas etapas subsequentes.

### 2. Limpeza de Dados (Camada Prata)
Na camada Prata, os seguintes processos de limpeza e validação são realizados:

- **Remoção de registros inválidos:** Remoção de registros com campos obrigatórios nulos, como nome, email e data de nascimento.
- **Correção de emails:** Se o email de um usuário não contém o caractere `@`, ele será corrigido substituindo a parte `example` por `@example` para garantir que o email seja válido.
- **Cálculo de Idade:** A idade dos usuários é calculada com base na data de nascimento e no dia atual.

### 3. Transformação de Dados (Camada Ouro)
Na camada Ouro, as transformações incluem:

- **Agregação por Faixa Etária e Status:** Os dados são agregados por faixa etária (0-10, 11-20, 21-30 anos, etc.) e pelo status (ativo ou inativo), permitindo uma análise mais detalhada sobre o perfil dos usuários.
- **Resultado:** O resultado é armazenado na pasta `gold/`, pronto para análises mais profundas e decisões estratégicas.

📚 Referências
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
