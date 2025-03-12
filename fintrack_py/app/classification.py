import queries
import functions_app


def get_classification():

    account = get_account()
    transaction_type = get_transaction_type()
    category = get_category()
    subcategory = get_subcategory()
    region = get_region()

    dict_classification = {
        "account": account['id_account'],
        "transaction_type": transaction_type['id_transaction_type'],
        "category": category['id_category'],
        "subcategory": subcategory['id_subcategory'],
        "region": region
    }

    return dict_classification


def get_account():
    """Exibe contas e permite que o usuário escolha uma."""
    print("\n### ESCOLHA A CONTA ###")
    accounts = queries.get_accounts()
    account = functions_app.list_options(accounts)
    if account:
        print(f"\nConta selecionada: {account['account_name']}\n")

    return account


def get_transaction_type():
    """Exibe all transaction types"""
    print("### ESCOLHA O TIPO DE TRANSAÇÃO ###")
    transaction_types = queries.get_transaction_types()
    transaction_type = functions_app.list_options(transaction_types)
    if transaction_type:
        print(f"\nTipo selecionado: {transaction_type['transaction_type_name']}\n")

    return transaction_type


def get_category():
    """Exibe all transaction categories"""
    print("### ESCOLHA A CATEGORIA ###")
    categories = queries.get_categories()
    category = functions_app.list_options(categories)
    if category:
        print(f"\nCategoria selecionada: {category['category_name']}\n")

    return category


def get_subcategory():
    """Exibe all transaction categories"""
    print("### ESCOLHA A CATEGORIA ###")
    subcategories = queries.get_subcategories()
    subcategory = functions_app.list_options(subcategories)
    if subcategory:
        print(f"\nSubcategoria selecionada: {subcategory['subcategory_name']}\n")

    return subcategory


def get_region():
    """Exibe all states that is possible to read a URL of NFE"""
    print('\n### A NFE é PR ou SC? ###\n')
    print('1 - Paraná\n2 - Santa Catarina\n')
    region = input()

    return region
