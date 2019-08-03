Copy and paste the following Dockerfile snippet into the Dockerfile section for a new environment:

```
RUN pip install --ignore-installed imdbpy wget tmdbsimple tensorflow gensim stop_words wordcloud
RUN pip install git+https://github.com/dominodatalab/python-domino.git
RUN echo 'if [ -z ${PYTHONPATH+x} ]; then export PYTHONPATH=${DOMINO_WORKING_DIR}; else export PYTHONPATH=${DOMINO_WORKING_DIR}:${PYTHONPATH}; fi' >> /home/ubuntu/.domino-defaults
RUN R --no-save -e "install.packages(c('flexdashboard', 'rmarkdown'))"
```
