#!/bin/sh

echo "ExtractData.py --index arxiv --minfreq 0.3 --maxfreq 0.6 --numwords 500" > output/E4/MRK$1.txt
python3 ExtractData.py --index arxiv --minfreq 0.3 --maxfreq 0.6 --numwords 500
python3 GeneratePrototypes.py --nclust 20
echo "MRK MEANS with $1 cores: " >> output/E4/MRK$1.txt
python3 MRKmeans.py --ncores $1 >> output/E4/MRK$1.txt
echo "PROCESS RESULTS: " >> output/E4/MRK$1.txt
python3 ProcessResults.py >> output/E4/MRK$1.txt
