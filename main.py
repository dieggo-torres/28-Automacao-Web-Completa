# Importa métodos da biblioteca selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Importa a biblioteca time
import time

# Importa a biblioteca json
import json

# Importa a bibliotca zipfile
import zipfile

# Importa um método da biblioteca pathlib
from pathlib import Path

# Importa a biblioteca pandas com o apelido pd
import pandas as pd

# Importa a biblioteca locale
import locale

# Importa a biblioteca yagmail
import yagmail

# Define as configurações locais
locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')

# Abre o arquivo JSON para leitura
with open('segredos.json') as segredos:
    dados_sensiveis = json.load(segredos)

# Obtém os dados de autenticação
usuario_email = dados_sensiveis['autenticacao_email']['usuario']
senha_email = dados_sensiveis['autenticacao_email']['senha']

# Cria uma instância do Google Chrome
navegador = webdriver.Chrome()

# Acessa o site especificado
navegador.get('https://www.kaggle.com/sakshigoyal7/credit-card-customers')


def clicar_elemento(seletor_css, i):
    '''Verifica se a lista de elementos tem pelo menos 1 elemento.

        Parâmetros:
            seletor_css (str): seletor css do elemento
            i (int): índice do elemento no qual se quer clicar
    '''

    # Aguarda 0.5s caso a lista não tenha pelo menos 1 elemento
    while len(navegador.find_elements(By.CSS_SELECTOR, seletor_css)) == 0:
        time.sleep(0.5)

    # Aguarda mais 1s
    time.sleep(1)

    # Clica no elemento
    navegador.find_elements(By.CSS_SELECTOR, seletor_css)[i].click()


def preencher_campo(seletor_css, i, texto):
    '''Preenche o campo que possui o seletor css especificado

        Parâmetros:
            seletor_css (str): seletor css do elemento
            i (int): índice do elemento que se quer preencher
            texto (str): texto para preencher o campo
    '''
    
    while len(navegador.find_elements(By.CSS_SELECTOR, seletor_css)) == 0:
        time.sleep(0.5)

    time.sleep(1)

    navegador.find_elements(By.CSS_SELECTOR, seletor_css)[i].send_keys(texto)


# Espera o botão de download da base de dados aparecer e depois clica nele
clicar_elemento('a.sc-htmcrh.emRwHY', 0)

# Espera a página de login carregar e depois clica no campo de login com e-mail
clicar_elemento('a.sc-jogDgT.hBPNLh', 1)

# Preenche o campo de e-mail
preencher_campo('input.mdc-text-field__input', 0, usuario_email)

# Preenche o campo de senha
preencher_campo('input.mdc-text-field__input', 1, senha_email)

# Clica no botão de login
navegador.find_element(By.CSS_SELECTOR, 'button.sc-cbeScs.HuzNs').click()

# Espera o botão de download da base de dados aparecer e depois clica nele
clicar_elemento('a.sc-htmcrh.emRwHY', 0)

# Espera 10s para a pasta ser baixada
time.sleep(10)

# Extrai o arquivo da pasta zipada para o diretório deste arquivo
with zipfile.ZipFile(r'C:\Users\diego\Downloads\archive.zip', 'r') as pasta_zipada:
    pasta_zipada.extractall(Path.cwd())

# Cria um dataframe
df_clientes = pd.read_csv('BankChurners.csv')

# Conta o número de clientes ativos e o número de clientes em disputa
resumo_status = df_clientes.groupby('Attrition_Flag')['Attrition_Flag'].count()

# Converte a tabela em uma string
resumo_status = resumo_status.to_string()

# Filtro de clientes ativos
filtro_clientes_ativos = df_clientes['Attrition_Flag'] == 'Existing Customer'

# Dataframe só com os clientes ativos
df_clientes_ativos = df_clientes[filtro_clientes_ativos]

# Conta o número de clientes ativos para cada categoria de cartão de crédito
resumo_categoria_cartao = df_clientes_ativos.groupby('Card_Category')['Card_Category'].count()

# Renomeia a coluna
resumo_categoria_cartao.index.names = ["Clientes Ativos por Categoria de Cartão"]

# Converte a tabela em uma string
resumo_categoria_cartao = resumo_categoria_cartao.to_string()

# Calcula o tempo médio de permanência dos clientes
tempo_medio_permanecia = df_clientes['Months_on_book'].mean()

# Valor médio de limite de todos os clientes
limite_todos_clientes = df_clientes['Credit_Limit'].mean()

# Formatação do valor monetário
limite_todos_clientes = locale.currency(limite_todos_clientes, grouping=True)

# Filtro de ex-clientes
filtro_ex_clientes = df_clientes['Attrition_Flag'] == 'Attrited Customer'

# Dataframe só com os ex-clientes
df_ex_clientes = df_clientes[filtro_ex_clientes]

# Valor médio de limite para ex-clientes
limite_ex_clientes = df_ex_clientes['Credit_Limit'].mean()

# Formatação do valor monetário
limite_ex_clientes = locale.currency(limite_ex_clientes, grouping=True)

# Cria uma instância do Gmail
usuario = yagmail.SMTP(user=usuario_email, password=senha_email)

# Campos do e-mail
destinatarios = dados_sensiveis['to']
copia = dados_sensiveis['cc']
copia_oculta = dados_sensiveis['bcc']

# Assunto do e-mail
assunto = 'Relatório de Clientes - Attrited Customers'

# Corpo do e-mail
mensagem = f'''
Olá! Tudo bem?

Conforme solicitado, levantei os principais indicadores de nossos clientes para ver o impacto dos attrited customers.

Atualmente, temos a seguinte divisão na base de clientes:

{resumo_status}

Com relação ao número de clientes ativos em cada categoria de cartão de crédito, verifiquei esta distribuição:

{resumo_categoria_cartao}

O tempo médio de permanência dos clientes é de {tempo_medio_permanecia:.1f} meses.

Por fim, verifiquei que o limite médio de crédito para cada categoria de cliente e descobri que a diferença era pouca.

- Limite geral (todos os clientes): {limite_todos_clientes}
- Limite ex-clientes: {limite_ex_clientes}

Segue em anexo o relatório completo para mais detalhes. Caso tenha alguma dúvida, entre em contato.

Att.,
Diego
'''

# Anexos
anexo = 'BankChurners.csv'

usuario.send(
    to=destinatarios,
    cc=copia,
    bcc=copia_oculta,
    subject=assunto,
    contents=mensagem,
    attachments=anexo
    )