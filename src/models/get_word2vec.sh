#!/bin/bash

# wget -c "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"
echo "Downloading the SLIMMED word2vec model..."
wget https://github.com/eyaler/word2vec-slim/raw/master/GoogleNews-vectors-negative300-SLIM.bin.gz
echo "Decompressing the model..."
gunzip -f -v GoogleNews-vectors-negative300-SLIM.bin.gz
echo "Decompressed. Moving..."
mv GoogleNews-vectors-negative300-SLIM.bin data/external/GoogleNews-vectors-negative300-SLIM.bin
echo "Move completed."
