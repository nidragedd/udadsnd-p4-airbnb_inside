# Udacity DataScience nanodegree project - Write a data blog post
## CONTEXT - OBJECTIVES
### Context
This project is only for educational purposes. I did it while I was following the `Udacity DataScience nanodegree`.  
Within the course, in order to develop our communication skills as DataScientist, we are asked to pick a dataset
available on the Internet. There are suggestions but we can take any dataset as soon as we explore it and follow the 
CRISP-DM process:
* Business Understanding
* Data Understanding
* Data Preparation
* Modeling
* Evaluation
* Deployment

### Objectives
There are 2 main objectives to reach in this project:
* create a Github code repository to share code, scripts, notebooks and documentation about data wrangling/modeling
 techniques, with a technical audience in mind
* write a blog post accessible to non-technical people in order to share our questions, insights, findings, thoughts
 and conclusions.

I chose to use datasets from **Airbnb** and, as a french people, I chose **Paris** as the city to analyze.

---
## DEPENDENCIES - INSTALLATION
### Create your CONDA virtual environment
Easiest way is to create a virtual environment through **[conda](https://docs.conda.io/en/latest/)**
and the given `environment.yml` file by running this command in a terminal (if you have conda, obviously):
```
conda env create -f environment.yml
```

If you do not have/want to use conda for any reason, you can still setup your environment by running some `pip install`
commands. Please refer to the `environment.yml` file to see what are the dependencies you will need to install.  
Basically, this project requires **Python 3.7** in addition to common datascience packages (such as 
[numpy](https://www.numpy.org/), [pandas](https://pandas.pydata.org/), 
[sklearn](https://scikit-learn.org/stable/), [matplotlib](https://matplotlib.org/), 
[seaborn](https://seaborn.pydata.org/) and so on).

For modeling, this project is using [xgboost](https://xgboost.readthedocs.io/en/latest/).  

NB: I made a NLP try on reviews, that is why there are those additional packages:
* [gensim](https://radimrehurek.com/gensim/): used for topic modeling
* [wordcloud](https://pypi.org/project/wordcloud/): used to generate some tag clouds
* [spacy](https://spacy.io/): NLP package for easy lemmatization
* [pyLDAvis](https://pyldavis.readthedocs.io/en/latest/): great tool to visualize the topics with LDA (Latent Dirichlet Allocation)

Feel free to skip them as for the moment the NLP part is not complete so not available in this repository.

---
### Directory & code structure
Here is the structure of the project:
```
    project
      |__ assets    (contains images displayed in notebooks)
      |__ config    (configuration section, so far it contains only the stop words list file - used only for NLP try)
      |__ data      (raw data downloaded from its source on the Internet)
            |__ clean  (data processed saved locally)
      |__ notebook  (contains all notebooks)
      |__ src       (python modules and scripts)
```

---
## WHAT YOU WILL FIND IN THIS PROJECT
Based on the data my approach for this project was to put myself in the shoes of a tourist who would love to come and visit Paris !

> As a tourist/foreigner and a user of Airbnb service and as I absolutely do not know Paris, I would like to know what is the best period or the best place (or both) in
order to plan my visit/holidays. 

> I would like to have a pretty good idea of the cost variation depending on location place and the dates and, obviously, I would be glad to know what are the odds to find something available for a given period so that perhaps I can adapt my holidays accordingly to places availabilities
(there is an alternative for the homeowner who would like be sure to rent at the best time that will maximize the profit and so maybe adapt the location availability depending on the market as well).

> Is it possible to find representative themes per places so that the service can help me and guide me in my choice (perhaps by asking me few questions) ?

Some questions may be answered by analyzing data and providing graph plots. For the price prediction, I will try to find whether it is possible to predict price and if yes what are the most
important elements that play a role in its value. So that, still with the "questioning the service user" scenario, we can give a pretty accurate estimation of the cost.
Does the place matter ? And what about the number of beds available ? Or perhaps it is just something else you are not even thinking about...

You will find several notebooks, one for each part of the CRISP-DM process. Start by this [one](notebook/0_Introduction.ipynb)
to enter the process.  
Or you can directly go to the section you are most interested in:
1. `Data Understanding`: [here](notebook/1_Data_Understanding.ipynb)
2. `Business Understanding`: [here](notebook/2_Business_Understanding.ipynb)
3. `Data Preparation`: [here](notebook/3_Data_Preparation.ipynb)
4. `Modeling` and `Evaluation`: [here](notebook/4_Modeling.ipynb)
5. Tuning models and Evaluation [here](notebook/4b_Modeling_Tuning_xgboost.ipynb)

An additional notebook with further Data Exploration is also provided [here](notebook/APPENDIX_Bonus_Exploratory_Data.ipynb).

Or, in the end, you can read the blog post here (**TODO**: put the link once it is written). It corresponds to the `Deployment` (or `Exposition`) phase.

---
## ACKNOWLEDGEMENT
This dataset is part of Airbnb Inside, and the original source can be found [here](http://insideairbnb.com/get-the-data.html)