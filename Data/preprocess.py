import json
import os
import pandas as pd

# https://github.com/dwyl/english-words/blob/master/words_dictionary.json

path = os.path.split(__file__)[0]

with open(path + "\\words_dictionary.json", "r+") as f:
    words = json.loads(f.read().replace("\n", ""))
    
# pandaboi
df = pd.DataFrame(list(words.keys()), columns=['w'])
df = df[df['w'].str.len() > 3] # maybe implement max length, depending on solving larger boards

print(df["w"])