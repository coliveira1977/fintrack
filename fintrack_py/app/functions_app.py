import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
# from functions_app import set_nfe_url
from datetime import datetime


def get_track_option():

    """
    Prompt user to choose between manual entry (M) or NFE launch (N).

    Displays instructions and validates
    input, ensuring only M or N is selected.

    Returns:
        str: User's validated choice ('M' or 'N')
    """
    print('### Para lançamento manual digite: M ###')
    print('### Para Lançamento de NFE digite: N ###')
    # type_launch = input()

    while True:
        choice = input("Digite M ou N: ").upper()
        if choice in ("M", "N"):
            return choice
        print("\nOps, opção errada! Você deve escolher somente M ou N.\n")


def list_options(dictionaries):
    if not dictionaries:
        print("Nenhum resultado encontrado.")

        return None

    for i, dictionary in enumerate(dictionaries, 1):
        dict_values = list(dictionary.values())
        print(f"{i}. {dict_values[1]}")

    while True:
        try:
            choice = int(input("\nDigite o número da conta desejada: "))
            if 1 <= choice <= len(dictionaries):
                choose = dictionaries[choice - 1]
                return choose
            else:
                print("\nNúmero inválido. Escolha um número da lista.\n")
                for i, dictionary in enumerate(dictionaries, 1):
                    dict_values = list(dictionary.values())
                    print(f"{i}. {dict_values[1]}")

        except ValueError:
            print("Entrada inválida. Digite um número válido.")


def set_nfe_url():
    print('### AGORA QUE ESTÁ TUDO CERTO, BASTA COLAR O LINK DO TICKET! ###\n')
    url_nfe = input()

    return url_nfe


def get_ticket_df(dict_classification):

    region = dict_classification["region"]

    # This dictionary contains the classes differences between regions
    region_classes_html = {
        '1': ['txtTit2', 'txtTit3 noWrap'],
        '2': ['txtTit', 'txtTit noWrap']
    }

    # Get the right class to soup
    region_class = region_classes_html.get(region)

    url_nfe = set_nfe_url()

    # Fazer requisição à página
    headers = {"User-Agent": "Mozilla/5.0"}  # Simula um navegador
    response = requests.get(url_nfe, headers=headers)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
    else:
        raise Exception("Erro ao acessar a URL da NFC-e")

    # Listas para armazenar os dados extraídos
    data = []

    # Encontrar todas as linhas de itens na tabela
    rows = soup.find_all("tr", id=lambda x: x and x.startswith("Item"))

    for row in rows:
        name_product = row.find("span", class_=region_class[0]).text.strip()

        cod_product = row.find("span", class_="RCod").text
        cod_product = re.sub(r"\s+", "", cod_product)
        cod_product = cod_product.strip().replace("(Código:", "")
        cod_product = cod_product.replace(")", "")

        quantity = row.find("span", class_="Rqtd").text
        quantity = quantity.replace("Qtde.:", "").strip()
        quantity = quantity.replace(",", ".")

        measure = row.find("span", class_="RUN")
        measure = measure.text.replace("UN:", "").strip()

        price = row.find("span", class_="RvlUnit").text
        price = price.replace("Vl. Unit.:", "").strip()
        price = price.replace(",", ".")

        total_value = row.find("td", class_=region_class[1])
        total_value = total_value.find("span", class_="valor").text
        total_value = total_value.strip().replace(",", ".")

        data.append([
            name_product,
            cod_product,
            quantity,
            measure,
            price,
            total_value
        ])

    # Criar um DataFrame pandas
    df_ticket = pd.DataFrame(data, columns=[
            "name_product",
            "cod_product",
            "quantity",
            "measure",
            "price",
            "total_value"
    ])

    # Extrair data e hora a partir de "Protocolo de Autorização"
    texto_infos = soup.find("div", id="infos").text
    match = re.search(r'(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2}:\d{2})', texto_infos)
    if match:
        # dt_ticket = match.group(1)
        dt_ticket = datetime.strptime(match.group(1), "%d/%m/%Y")
        hour_ticket = match.group(2)

    else:
        dt_ticket = "Não encontrado"
        hour_ticket = "Não encontrado"

    # Extrair informações do estabelecimento
    store_name = soup.find("div", class_="txtTopo").text.strip()
    store_address = " ".join([x.text.strip() for x in soup.find_all("div", class_="text")])
    # Remover "CNPJ:" e o número do CNPJ
    store_address = re.sub(r'CNPJ:\s*\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', '', store_address).strip()
    # Remover quebras de linha e espaços extras
    store_address = " ".join(line.strip() for line in store_address.splitlines() if line.strip())

    # Criar DataFrame do estabelecimento
    df_store = pd.DataFrame([[
        store_name,
        store_address,
        dt_ticket,
        hour_ticket,
        url_nfe,
        dict_classification['account'],
        dict_classification['category'],
        dict_classification['subcategory'],
        dict_classification['transaction_type']
        ]],
        columns=[
            "store_name",
            "store_address",
            "dt_ticket",
            "hour_ticket",
            "url_nfe",
            "account",
            "category",
            "subcategory",
            "transaction_type"
            ]
    )

    dict_nfe_pr = {
        "df_ticket": df_ticket,
        "df_store": df_store,
        "dt_ticket": dt_ticket,
        "hour_ticket": hour_ticket
    }

    return dict_nfe_pr
