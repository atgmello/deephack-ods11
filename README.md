# deephack-ods11
Repository for the DeepHack Hackfest, team #16 composed by @gustavoem and @atgmello. In this repository we will use data science to analyze and create insights that might help TCE-SP to identify aspects of the susteinable development goals (SDG) in the state of São Paulo. In this work, we are focused on analyzing data related to the 11-th goal: sustainable cities and communities.

# Repository organization
Most files of this repository are present either on `src` or `notebooks` directory. 
On the `src` directory:
* `balanco_municipal_tce` - contains a Python module that is able to retrieve, group and analyze data from [transparencia.tce.sp.gov.br](tce website). With this package, one can get expenses of a city in an specific year, grouped by
the type of expense; one can also group historical data to analyze how expenses of a city evolve through years.
* `cdhudf` - 
* `ibgedf` - 

On the `notebooks` directory:
* `exploracao_inicial.ipynb` - contains a compilation of useful links describing SGD and online databases that we considered related to our goal, initially.
* `first_look_andre.ipynb` and `first_look_gustavo.ipynb` - are "warm-up" notebooks, both containing simple exploration of some public data.
* `balancomunicipal_examples.ipynb` - contains examples of calls to the `balanco_municipal_tce` module.
* `classifying_expenses.ipynb` - is an example of application of machine learning using data fetched by `balanco_municipal_tce`. In this notebook, we use natural language processing and more specifically ```fasttext``` to create a supervised learning procedure that allows one to classify the theme of expenses of a city.
* `ibgedf_examples.ipynb` - 
