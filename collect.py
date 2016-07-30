import requests, time 
import os, shutil
from bs4 import BeautifulSoup
BASE_URL='http://www.kijiji.it/case/vendita/roma-annunci-roma/'
MAX_PAGE=100

def add_ads(url,i):
    r=requests.get(url)
    content=r.content
    soup=BeautifulSoup(content)
    results=soup.find_all(class_='cta')
    for res in results:
        i+=1
        f=open('documents/document-'+str(i).zfill(6)+'.txt','w')
        title=res.h3.get_text().encode('utf-8')
        location=res.find('p','locale').get_text().encode('utf-8')
        price=res.h4.get_text().encode('utf-8')
        adurl=res['href'].encode('utf-8')
        description=res.find('p','description').get_text().encode('utf-8')
        f.write(title+'\t'+location+'\t'+price+'\t'+adurl+'\t'+description)
        f.close()
    return i
    
def process_pages(base_url,i,min_page=1,max_page=1,delay=2):
    for j in range(min_page,max_page+1):
        print 'Processing page: '+str(j)
        i=add_ads(base_url+'?p=j',i)
        
        time.sleep(delay)
    return i
        
if os.path.exists('documents'):
    shutil.rmtree('documents')
os.makedirs('documents')
i=0
i=process_pages(BASE_URL,i,1,MAX_PAGE)

for k in range(1,i+1,500):
        os.makedirs('documents/documents-'+str(k).zfill(6)+'-'+str(k+499).zfill(6))
        for j in range(k,k+500):
            if os.path.exists('documents/document-'+str(j).zfill(6)+'.txt'):
                shutil.move('documents/document-'+str(j).zfill(6)+'.txt','documents/documents-'+str(k).zfill(6)+'-'+str(k+499).zfill(6)+'/document-'+str(j).zfill(6)+'.txt')
    
    