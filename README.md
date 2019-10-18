# Time 16 - DeepHack 2019

(*PT-BR*)

Repositório do time #16, composto por @gustavoem e @atgmello, destinado ao DeepHack Hackfest 2019. Disponibilizamos neste repositório nossas análises e insights criados a partir da aplicação de Data Science a dados públicos. Esperamos que esses resultados possam ser úteis para o TCE-SP na identificação do comprometimento do Estado e Municípios com os Objetivos de Desenvolvimento Sustentável da ONU. Mais especificamente, focamos na análise de dados relacionados ao Objetivo 11: Cidades e comunidades sustentáveis.

# Organização do repositório

A maior parte dos arquivos nesse repositório se encontram nas pastas `src` ou `notebooks`.
Em `src`:
* `balanco_municipal_tce` - contém um módulo Python para recuperação, agrupamento e análise de dados do [transparencia.tce.sp.gov.br](site do TCE). Com esse pacote é possível obter despesas por cidade e por ano, agrupado pelo tipo de despesa; tambm é possível agrupar dados históricos para analisar como gastos de uma cidade evolui ao longo dos anos.
* `cdhudf` - módulo Python para recuperação, agrupamento e análise de dados da [https://servicodados.ibge.gov.br/api/docs](API do IBGE). Mais especificamente, por enquanto apenas foi implementado a recuperação de dados de Pesquisas.
* `ibgedf` - módulo Python para recuperação, agrupamento e análise de dados do [www.cdhu.sp.gov.br](site do CDHU).

Em `notebooks`:
* `exploracao_inicial.ipynb` - compilação de links úteis relacionados ao Objetivo 11 e bases de dados online que foram inicialmente consideradas.
* `first_look_andre.ipynb` e `first_look_gustavo.ipynb` - notebooks para "aquecimento", ambos contendo uma exploraço simples de alguns dados públicos.
* `*_examples.ipynb` - notebooks contendo exemplos de uso dos diferentes módulos desenvolvidos.
* `classifying_expenses.ipynb` - is an example of application of machine learning using data fetched by `balanco_municipal_tce` - nesse notebook utilizamos processamento de linguagem natural, mais especificamente o framework ```fasttext```, para criar um procedimento de aprendizado supervisionado que permite a classificação dos temas dos gastos de um município.
* `cross_report.ipynb` - esse notebook contém uma análise de dados exploratória através do cruzamento das diferentes bases de dados suportadas pelos módulos desenvolvidos.

Note que os notebooks mais importantes, portanto, são: `cross_report.ipynb` e `classifying_expenses.ipynb`, seguidos dos `*_examples.ipynb`. Os demais notebooks contam com uma exploração menos estruturada dos dados. 

Para facilitar o acesso e visualização dos notebooks, recomendamos a tulizaço do Nbviewer, através do link:
https://nbviewer.jupyter.org/github/atgmello/deephack-ods11/tree/master/notebooks/

---

(*EN*)

Repository for the DeepHack Hackfest 2019, team #16 composed by @gustavoem and @atgmello. In this repository we will use data science to analyze and create insights that might help TCE-SP to identify aspects of the susteinable development goals (SDG) in the state of São Paulo. In this work, we are focused on analyzing data related to the 11-th goal: sustainable cities and communities.

# Repository organization
Most files of this repository are present either on `src` or `notebooks` directory. 
On the `src` directory:
* `balanco_municipal_tce` - contains a Python module that is able to retrieve, group and analyze data from [transparencia.tce.sp.gov.br](tce website). With this package, one can get expenses of a city in an specific year, grouped by
the type of expense; one can also group historical data to analyze how expenses of a city evolve through years.


On the `notebooks` directory:
* `exploracao_inicial.ipynb` - contains a compilation of useful links describing SGD and online databases that we considered related to our goal, initially.
* `first_look_andre.ipynb` and `first_look_gustavo.ipynb` - are "warm-up" notebooks, both containing simple exploration of some public data.
* `balancomunicipal_examples.ipynb` - contains examples of calls to the `balanco_municipal_tce` module.
* `classifying_expenses.ipynb` - is an example of application of machine learning using data fetched by `balanco_municipal_tce`. In this notebook, we use natural language processing and more specifically ```fasttext``` to create a supervised learning procedure that allows one to classify the theme of expenses of a city.
