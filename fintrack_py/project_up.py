from functions import create_database, create_tables, insert_initial_data

if __name__ == "__main__":
    create_database()  # Cria o banco de dados se não existir
    create_tables()    # Cria as tabelas dentro do banco
    insert_initial_data()  # Insere os dados iniciais
