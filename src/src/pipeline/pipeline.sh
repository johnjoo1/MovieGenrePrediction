#!/bin/bash

#python src/pipeline/domino_pipeline.py pipeline_cfg/full_retrain.cfg

python src/data/movie_list.py
python src/data/overviews.py
python src/data/cleaning_data.py
python src/features/feature_eng.py
sh src/models/get_word2vec.sh
python src/features/word2vec_features.py
