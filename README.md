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
RUN pip install --ignore-installed imdbpy wget tmdbsimple tensorflow gensim stop_words wordcloud
RUN pip install git+https://github.com/dominodatalab/python-domino.git
RUN echo 'if [ -z ${PYTHONPATH+x} ]; then export PYTHONPATH=${DOMINO_WORKING_DIR}; else export PYTHONPATH=${DOMINO_WORKING_DIR}:${PYTHONPATH}; fi' >> /home/ubuntu/.domino-defaults
RUN R --no-save -e "install.packages(c('flexdashboard', 'rmarkdown'))"
```

### TMDB_API_KEY
f18f986c449c9585986f07ecbd535291


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
