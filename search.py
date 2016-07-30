from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re,string
import numpy as np

def find_voc(word):
    f=open('index/vocabulary.txt','r')
    A=np.genfromtxt(f,dtype=str, delimiter='\t')
    f.close()
    for i in range(len(A)):
        if A[i,1]==word:
            return int(A[i,0])
    return 'not in vocabulary'
    
QUERY=raw_input('Search:')
stemmer=SnowballStemmer('italian')
query=[]
#split
QUERY=re.sub("[^\w]"," ",QUERY).split()
#normalize
for word in QUERY:
    if word.decode('utf-8') not in stopwords.words('italian'):
        query.append(stemmer.stem(word))
f=open('index/postings.txt')
lines=f.readlines()

mappa=[[],[],[]] #first list: terms, second list: termID, third list: posting list
for word in query:
    term_num=find_voc(word)
    if term_num=='not in vocabulary':
        print 'There are not documents containing your query'
        exit()
    mappa[0].append(word)
    mappa[1].append(term_num)
    mappa[2].append(re.sub("[^\w]"," ",lines[term_num-1]).split()[1:])
f.close()
    
result=[]
pointer=[0]*len(mappa[0])

finished=False
while (not finished):
    minDoc=min([mappa[2][i][pointer[i]] for i in range(len(mappa[0]))])
    val=True
    #evaluate query on minDoc
    for term in query:
        index=mappa[0].index(term)
        if minDoc not in mappa[2][index]:
            val=False
    if val==True:
        result.append(minDoc)
    
    
    for i in range(len(mappa[0])):
        if mappa[2][i][pointer[i]]==minDoc:
            pointer[i]+=1
    for i in range(len(mappa[0])):
        if pointer[i]==len(mappa[2][i]):
            finished=True

result=list(set(result))     
if result==[]:
    print 'There are not documents containing your query'
    exit()
result.sort()
for res in result:
    print 'Document number: '+res.zfill(6)
    a=1
    b=500
    n=int(res)
    while(not(a<=n and b>=n)):
        a+=500
        b+=500
    a,b=str(a),str(b)
    f=open('documents/documents-'+a.zfill(6)+'-'+b.zfill(6)+'/document-'+res.zfill(6)+'.txt')
    print string.join(re.split('\t',f.read())[:-1],'\n')
    f.close
    print '----------------------------'

            