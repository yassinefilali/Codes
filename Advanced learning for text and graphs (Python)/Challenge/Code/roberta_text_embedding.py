import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
import ast 
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.corpus import stopwords 
import re


model = SentenceTransformer('stsb-roberta-base')
pattern = re.compile(r'(,){2,}')
fw = open("abstracts_processed.txt","r",encoding="utf8")
f = open("paper_embeddingsnewtest.txt","w")
size = Path("abstracts_processed.txt").stat().st_size
i = 1
for l in fw:
    #auth_paps = [paper_id.strip() for paper_id in l.split(":")[1].replace("[","").replace("]","").replace("\n","").replace("\'","").replace("\"","").split(",")]
    #d[l.split(":")[0]] = auth_paps
    #id+"----"+abstract+"\n"
    s = l.split("----")
    sentence = s[1]
    tid = s[0]
    #print(tid,' ',sentence)
    f.write(str(tid)+":"+np.array2string(model.encode(sentence,show_progress_bar=False), formatter={'float_kind':lambda x: "%.8f" % x})+"\n")    
    i+=1
    print('iteration : ',i,'/',1056540)

f.close()
fw.close()


