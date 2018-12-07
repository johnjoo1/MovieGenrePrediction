#!/bin/bash

wget -c "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"
gunzip GoogleNews-vectors-negative300.bin.gz
mv GoogleNews-vectors-negative300.bin /mnt/data/external/GoogleNews-vectors-negative300.bin