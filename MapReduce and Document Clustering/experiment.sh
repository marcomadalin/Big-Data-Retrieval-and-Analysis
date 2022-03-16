#!/bin/sh

echo "ExtractData.py --index $1 --minfreq $2 --maxfreq $3 --numwords $4" > output/E1/MRK$5.txt
python3 ExtractData.py --index $1 --minfreq $2 --maxfreq $3 --numwords $4
python3 GeneratePrototypes.py --nclust 20
echo "MRK MEANS: " >> output/E1/MRK$5.txt
python3 MRKmeans.py >> output/E1/MRK$5.txt
echo "PROCESS RESULTS: " >> output/E1/MRK$5.txt
python3 ProcessResults.py >> output/E1/MRK$5.txt
