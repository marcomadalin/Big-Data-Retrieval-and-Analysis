import matplotlib.pyplot as plt
import os


def parseNumWords(line):
    return int(line.split()[0])

path = './results/indexTokens'
files = os.listdir(path)

eje_x = ['classic', 'letter_snowball', 'letter_stop', 'letter', 'standard', 'whitespace']

eje_y = []
for f in files:
    with open(path+'/'+f, "r") as f:
        lines = f.readlines()
    eje_y.append(parseNumWords(lines[-1]))

plt.figure(figsize=(15,6))
plt.bar(eje_x, eje_y)
plt.xlabel('Index')
plt.ylabel('Number of Words')
plt.show()
plt.savefig( './results/numWordsIndex.png')
