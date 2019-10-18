# Time 16 - DeepHack 2019

(*PT-BR*)

Repositório do time #16, composto por @gustavoem e @atgmello, destinado ao DeepHack Hackfest 2019. Disponibilizamos neste repositório nossas análises e insights criados a partir da aplicação de Data Science a dados públicos. Esperamos que esses resultados possam ser úteis para o TCE-SP na identificação do comprometimento do Estado e Municípios com os Objetivos de Desenvolvimento Sustentável da ONU. Mais especificamente, focamos na análise de dados relacionados ao Objetivo 11: Cidades e comunidades sustentáveis.

# Organização do repositório

A maior parte dos arquivos nesse repositório se encontram nas pastas `src` ou `notebooks`.
Em `src`:
* `balanco_municipal_tce` - contém um módulo Python para recuperação, agrupamento e análise de dados do [site do TCE](transparencia.tce.sp.gov.br). Com esse pacote é possível obter despesas por cidade e por ano, agrupado pelo tipo de despesa; tambm é possível agrupar dados históricos para analisar como gastos de uma cidade evolui ao longo dos anos.
* `cdhudf` - módulo Python para recuperação, agrupamento e análise de dados da [API do IBGE](https://servicodados.ibge.gov.br/api/docs). Mais especificamente, por enquanto apenas foi implementado a recuperação de dados de Pesquisas.
* `ibgedf` - módulo Python para recuperação, agrupamento e análise de dados do [site do CDHU](www.cdhu.sp.gov.br).

Em `notebooks`:
* `exploracao_inicial.ipynb` - compilação de links úteis relacionados ao Objetivo 11 e bases de dados online que foram inicialmente consideradas.
* `first_look_andre.ipynb` e `first_look_gustavo.ipynb` - notebooks para "aquecimento", ambos contendo uma exploraço simples de alguns dados públicos.
* `*_examples.ipynb` - notebooks contendo exemplos de uso dos diferentes módulos desenvolvidos.
* `classifying_expenses.ipynb` - is an example of application of machine learning using data fetched by `balanco_municipal_tce` - nesse notebook utilizamos processamento de linguagem natural, mais especificamente o framework ```fasttext```, para criar um procedimento de aprendizado supervisionado que permite a classificação dos temas dos gastos de um município.
* `cross_report.ipynb` - esse notebook contém uma análise de dados exploratória através do cruzamento das diferentes bases de dados suportadas pelos módulos desenvolvidos.

Note que os notebooks mais importantes, portanto, são: `cross_report.ipynb` e `classifying_expenses.ipynb`, seguidos dos `*_examples.ipynb`. Os demais notebooks contam com uma exploração menos estruturada dos dados. 

Para facilitar o acesso e visualização dos notebooks, recomendamos a utilização do Nbviewer, através do link:
https://nbviewer.jupyter.org/github/atgmello/deephack-ods11/tree/master/notebooks/
