from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re,os,shutil,string
import pandas as pd
import numpy as np

if os.path.exists('index'):
    shutil.rmtree('index')
os.makedirs('index')

stemmer=SnowballStemmer('italian')
A=pd.DataFrame({'words':[],'post_list':[]})
i=0
for folder in os.listdir('documents/'):
    for doc in os.listdir('documents/'+folder+'/'):
        print doc
        i+=1
        f=open('documents/'+str(folder)+'/'+str(doc))
        text=f.read()
        f.close()
        TEXT=[]
        #split
        text=re.sub("[^\w]"," ",text).split()
        #normalize
        for word in text:
            if word.decode('utf-8') not in stopwords.words('italian'):
                TEXT.append(stemmer.stem(word))
        #put the word in vocabulary
        for word in TEXT:
            a=pd.DataFrame({'words':[word],'post_list':[str(i)]})
            A=A.append(a, ignore_index=True)

if os.path.exists('index'):
    shutil.rmtree('index')
os.makedirs('index')
A=A.sort('words')
grouped=A.groupby('words')
G=grouped.agg(string.join)

fvoc=open('index/vocabulary.txt','w')
fpos=open('index/postings.txt','w')
i=0
for word in G.index:
    i+=1
    fvoc.write(str(i)+'\t'+word+'\n')
    fpos.write(str(i)+'\t'+string.join(G.loc[word]['post_list'].split(),sep='\t')+'\n')
fvoc.close()
fpos.close()


   





            
    


