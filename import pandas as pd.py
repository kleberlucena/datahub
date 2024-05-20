import pandas as pd
import fsspec

# Carregar o arquivo Excel
df = pd.read_excel('C:\Users\klebe\Documents\projetos\COINT\DADOS\OCORRÊNCIAS (respostas).xlsx', sheet_name='Respostas ao formulário 1')

# Extrair os dados da coluna desejada
coluna_original = df['Algum NI prestou apoio nessa ocorrência além do já mencionado no item anterior? Quais?']

# Criar uma nova lista para armazenar os dados modificados
nova_coluna = []

# Iterar sobre cada item na coluna original
for item in coluna_original:
    # Dividir os itens com base na vírgula
    itens_divididos = item.split(', ')
    # Adicionar cada item individual à nova coluna
    nova_coluna.extend(itens_divididos)

# Criar um novo DataFrame com a nova coluna
novo_df = pd.DataFrame(nova_coluna, columns=['Nova Coluna'])

# Salvar o novo DataFrame em um novo arquivo Excel
novo_df.to_excel('apoio.xlsx', index=False)
