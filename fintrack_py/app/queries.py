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


def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    # return mysql.connector.connect(**DB_CONFIG)
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Falha na conexão com banco: '{DB_CONFIG['database']}': {err}")
        return None


def get_custom_query(query):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results


def get_accounts():
    """Consulta as contas ativas e retorna uma lista de dicionários."""

    query = (
        "SELECT id_account, account_name "
        "FROM account "
        "WHERE situation = 'A';"
    )

    results = get_custom_query(query)

    return results  # Returns a list of dictionaries


def get_transaction_types():
    """Generate a list with all transaction types"""
    query = (
        "SELECT id_transaction_type, transaction_type_name "
        "FROM transaction_type"
        "WHERE situation = 'A';"
    )

    results = get_custom_query(query)

    return results  # Returns a list of dictionaries


def get_categories():
    """Generate a list with all categories"""
    query = (
        "SELECT id_category, category_name"
        "FROM category WHERE situation = 'A';"
    )

    results = get_custom_query(query)

    return results  # Returns a list of dictionaries


def get_subcategories():
    """Generate a list with all subcategories"""
    query = (
        "SELECT id_subcategory, subcategory_name"
        "FROM subcategory WHERE situation = 'A';"
    )
    results = get_custom_query(query)

    return results  # Returns a list of dictionaries


def insert_launch(dict_nfe):
    df_store = dict_nfe["df_store"]
    df_ticket = dict_nfe["df_ticket"]

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            for index, row in df_store.iterrows():
                # Inserir a transação e obter o ID gerado
                sql_transaction = """
                INSERT INTO transaction (
                    store_name, store_address,
                    dt_ticket, hour_ticket, url_nfe,
                    fk_id_account, fk_id_category,
                    fk_id_subcategory, fk_id_transaction_type
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """
                values_transaction = (
                    row["store_name"], row["store_address"], row["dt_ticket"],
                    row["hour_ticket"], row["url_nfe"], row["account"],
                    row["category"], row["subcategory"],
                    row["transaction_type"]
                )
                cursor.execute(sql_transaction, values_transaction)

                # Obter o ID da transação recém-inserida
                transaction_id = cursor.lastrowid

                # Inserir os tickets relacionados
                for index_ticket, row_ticket in df_ticket.iterrows():
                    sql_ticket = """
                    INSERT INTO ticket (
                        cod_product, name_product, quantity, measure, price,
                        total_value, fk_id_transaction
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    values_ticket = (
                        row_ticket["cod_product"], row_ticket["name_product"],
                        row_ticket["quantity"], row_ticket["measure"],
                        row_ticket["price"], row_ticket["total_value"],
                        transaction_id
                    )
                    cursor.execute(sql_ticket, values_ticket)

        connection.commit()
        print("Dados inseridos com sucesso!")

    except Exception as e:
        connection.rollback()
        print(f"Erro ao inserir dados no MySQL: {e}")

    finally:
        connection.close()
