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