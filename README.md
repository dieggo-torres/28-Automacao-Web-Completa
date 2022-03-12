# [Profissional] Automação Web Completa

Este projeto é uma automação web completa para baixar uma base de dados da [Kaggle](https://www.kaggle.com/sakshigoyal7/credit-card-customers), analisá-la com o pandas e, por fim, enviar um relatório de indicadores para uma pessoa ou grupo de pessoas.

Ele envolve a execução dos seguintes passos:

1. Acessar o site especificado;
2. Clicar no botão para baixar a base de dados;
3. Escolher um método de login (e-mail neste caso);
4. Fazer login na conta da Kaggle;
5. Baixar a base de dados;
6. Localizar a pasta zipada que contém a base;
7. Extrair o arquivo e movê-lo para a mesma pasta do código;
8. Importar o arquivo com o pandas;
9. Calcular indicadores
   - Distribuição de clientes ativos e em disputa;
   - Distribuição de categorias de cartão para clientes ativos;
   - Tempo médio de permanência dos clientes;
   - Limite médio de cartão de crédito para as categorias de clientes
10. Enviar e-mail com os resultados obtidos.

## Bibliotecas Usadas

Neste projeto usei estas bibliotecas:

- json
- locale
- pandas
- pathlib
- selenium
- time
- yagmail
- zipfile
