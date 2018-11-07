MoviesGenrePrediction
==============================

Problem: 
Netflux is an online platform that enables users to watch movies on smart TVs, PCs, Macs, mobiles, tablets, and so on. They have people write overviews for each movie to show in the preview section. They need to make sure that the written overviews represent the genre(s) of the movie.
We need to predict the genre(s) of the movie given the written overview.


Solution:
- Data: Pulled using TMDB API
- Algorithm:
  - SVC with TF-IDF
  - Naive Bayes with Count Vectorizer
  - Neural Network with Word2Vec

Credits:
Materials from this project was heavily borrowed, if not straight copied, from Spandan Madan. http://dx.doi.org/10.5281/zenodo.830003 
Github: https://github.com/Spandan-Madan/DeepLearningProject

# Environment Dockerfile snippet (required for Domino 201)
```
RUN pip install imdbpy wget tmdbsimple tensorflow gensim stop_words
RUN pip install git+https://github.com/dominodatalab/python-domino.git
RUN echo 'if [ -z ${PYTHONPATH+x} ]; then export PYTHONPATH=${DOMINO_WORKING_DIR}; else export PYTHONPATH=${DOMINO_WORKING_DIR}:${PYTHONPATH}; fi' >> /home/ubuntu/.domino-defaults
RUN R --no-save -e "install.packages(c('flexdashboard', 'rmarkdown'))"
```

### TMDB_API_KEY
f18f986c449c9585986f07ecbd535291

Project Organization (WIP)
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks.
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │



--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
