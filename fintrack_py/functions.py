import os
import mysql.connector
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Configuração do banco de dados
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}


def create_database():
    """Cria o banco de dados se não existir."""
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
    )
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {
            DB_CONFIG['database']
        }")
        print(f"'{DB_CONFIG['database']}' created!")

    except mysql.connector.Error as err:
        print(f"Error ao criar/verificar o banco de dados: {err}")
    finally:
        cursor.close()
        conn.close()


def create_tables():
    """Cria as tabelas no banco de dados."""
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()

        TABLES = {
            "category": """
                CREATE TABLE IF NOT EXISTS category (
                    id_category INT AUTO_INCREMENT PRIMARY KEY,
                    category_name VARCHAR(255) NOT NULL,
                    situation ENUM('A', 'I') NOT NULL
                )
            """,
            "account": """
                CREATE TABLE IF NOT EXISTS account (
                    id_account INT AUTO_INCREMENT PRIMARY KEY,
                    account_name VARCHAR(255) NOT NULL,
                    situation ENUM('A', 'I') NOT NULL
                )
            """,
            "subcategory": """
                CREATE TABLE IF NOT EXISTS subcategory (
                    id_subcategory INT AUTO_INCREMENT PRIMARY KEY,
                    subcategory_name VARCHAR(255) NOT NULL,
                    situation ENUM('A', 'I') NOT NULL
                )
            """,
            "transaction_type": """
                CREATE TABLE IF NOT EXISTS transaction_type (
                    id_transaction_type INT AUTO_INCREMENT PRIMARY KEY,
                    transaction_type_name VARCHAR(255) NOT NULL,
                    situation ENUM('A', 'I') NOT NULL
                )
            """,
            "transaction": """
                CREATE TABLE IF NOT EXISTS transaction (
                    id_transaction INT AUTO_INCREMENT PRIMARY KEY,
                    store_name VARCHAR(255) NOT NULL,
                    store_address TEXT NOT NULL,
                    dt_ticket DATE NOT NULL,
                    hour_ticket TIME NOT NULL,
                    url_nfe VARCHAR(500) NULL,
                    date_up DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date_down DATETIME NULL,
                    fk_id_account INT NOT NULL,
                    fk_id_category INT NOT NULL,
                    fk_id_subcategory INT NOT NULL,
                    fk_id_transaction_type INT NOT NULL,
                    FOREIGN KEY (fk_id_account) REFERENCES account(id_account),
                    FOREIGN KEY (fk_id_category) REFERENCES
                    category(id_category),
                    FOREIGN KEY (fk_id_subcategory) REFERENCES
                    subcategory(id_subcategory),
                    FOREIGN KEY (fk_id_transaction_type) REFERENCES
                    transaction_type(id_transaction_type)
                )
            """,
            "ticket": """
                CREATE TABLE IF NOT EXISTS ticket (
                    id_ticket INT AUTO_INCREMENT PRIMARY KEY,
                    cod_product BIGINT NOT NULL,
                    name_product VARCHAR(255) NOT NULL,
                    quantity DECIMAL(10,2) NOT NULL,
                    measure VARCHAR(50) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    total_value DECIMAL(10,2) NOT NULL,
                    date_up DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date_down DATETIME NULL,
                    fk_id_transaction INT NOT NULL,
                    FOREIGN KEY (fk_id_transaction) REFERENCES
                    transaction(id_transaction)
                )
            """,
        }

        for table_name, table_sql in TABLES.items():
            try:
                cursor.execute(table_sql)
                print(f"Tabela '{table_name}' criada/verificada successfully!")
            except mysql.connector.Error as err:
                print(f"Erro ao criar a tabela '{table_name}': {err}")

        cursor.close()
        conn.close()

# Dados iniciais para inserção
INITIAL_DATA = {
    "category": [
        (1, "Moradia", "A"),
        (2, "Emprego", "A"),
        (3, "Relacionamento", "A"),
        (4, "Saúde", "A"),
        (5, "Pessoal", "A")
    ],
    "account": [
        (1, "Itau Conta Corrente", "A"),
        (2, "Bradesco Conta Corrente", "A"),
        (3, "Carteira", "A"),
        (4, "Cofrinho", "A"),
        (5, "VA - Vale Alimentação", "A"),
        (6, "VR - Vale Refeição", "A"),
    ],
    "subcategory": [
        (1, "Alimentação", "A"),
        (2, "Refeição", "A"),
        (3, "Salário", "A"),
        (4, "Água", "A"),
        (5, "Remédios", "A"),
        (6, "Marketing Digital", "A"),
        (7, "Gasolina", "A"),
        (8, "Estacionamento", "A"),
        (9, "Transporte", "A"),
        (10, "Reunião", "A"),
        (11, "Equipamento", "A"),
        (12, "Ajuste", "A")
    ],
    "transaction_type": [
        (1, "Despesa", "A"),
        (2, "Receita", "A"),
        (3, "Transferência", "A"),
    ],
}


def connect_to_db():
    """Conecta ao banco de dados."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print(f"{DB_CONFIG['database']}' successfully connected!")
        return conn
    except mysql.connector.Error as err:
        print(f"Error to connect to '{DB_CONFIG['database']}': {err}")
        return None


def insert_initial_data():
    """Insere os dados iniciais nas tabelas."""
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()

        # Inserindo os dados
        queries = {
            "category": (
                "INSERT IGNORE INTO category "
                "(id_category, category_name, situation) "
                "VALUES (%s, %s, %s)"
            ),
            "account": (
                "INSERT IGNORE INTO account "
                "(id_account, account_name, situation) "
                "VALUES (%s, %s, %s)"
            ),
            "subcategory": (
                "INSERT IGNORE INTO subcategory "
                "(id_subcategory, subcategory_name, situation) "
                "VALUES (%s, %s, %s)"
            ),
            "transaction_type": (
                "INSERT IGNORE INTO transaction_type "
                "(id_transaction_type, transaction_type_name, situation) "
                "VALUES (%s, %s, %s)"
            ),
        }

        for table, data in INITIAL_DATA.items():
            try:
                cursor.executemany(queries[table], data)
                conn.commit()
                print(f"'{table}' data successfully inserted!")
            except mysql.connector.Error as err:
                print(f"Error to insert data on: '{table}': {err}")

        cursor.close()
        conn.close()
