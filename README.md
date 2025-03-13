# Fintrack

## Descrição

Fintrack é um sistema simples para gerenciar gastos e classificar compras. Os usuários podem registrar lançamentos manualmente ou importar dados automaticamente a partir de notas fiscais eletrônicas.

Ao fornecer a URL de uma nota fiscal eletrônica, o sistema utiliza um crawler para extrair e armazenar os detalhes da compra em um banco de dados local, garantindo praticidade e organização financeira.

## Tecnologias Utilizadas

Para o funcionamento do crawler, utilizamos as seguintes tecnologias:
- **Python**
- **Pandas**
- **BeautifulSoup**
- **MySQL**

O código Python segue os padrões de estilo definidos pelo **Flake8**.

## Instalação

Para instalar e rodar o Fintrack em seu computador, siga os passos abaixo:

1. Abra o prompt de comando (cmd, terminal ou PowerShell)
2. Execute o seguinte comando para instalar as dependências:
   ```sh
   pip install -r requirements.txt
   ```
3. Em seguida, execute o sistema:
   ```sh
   python project_up.py
   ```

Agora o Fintrack estará pronto para uso!

