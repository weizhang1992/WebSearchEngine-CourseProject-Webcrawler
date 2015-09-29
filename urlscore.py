import urllib2,socket
import re,collections
from bs4 import BeautifulSoup

def url_score_base(url,thequery):
    score={}
    try:
        response=urllib2.urlopen(url,timeout = 3)
    except urllib2.URLError,e:
        return 0,0,False,e.reason,None
    except socket.timeout as e: # <-------- this block here
        return 0,0,False,e[0],None  
    except urllib2.HTTPError,e: 
        return 0,0,False,e.getcode(),None

    try:
        data = response.read()
    except:
        return 0,0,False,"slow",None
    
    try:
        pageHeaders = response.headers
        contentType = pageHeaders.getheader('content-type')
        contenttype=contentType
    except:
        contenttype=None
    
    soup = BeautifulSoup(data,"lxml")    
    a = soup.get_text().lower()
    
    b = thequery.lower().split()
    score_of_url=0
    
    for item in b:

        query_count = collections.Counter(re.findall(item,a))
        if query_count[item]>0:
            score[item]=query_count[item]
        score_of_url=score_of_url+a.count(item)
    score_of_url=score_of_url*(len(score)**2)
    
    return score_of_url,data,True,response.getcode(),contenttype

def url_score(url,thequery,basescore):
    score={}
    b = thequery.lower().split()
    a= url.lower()
    
    for item in b:
        query_count = collections.Counter(re.findall(item,a))
        if query_count[item]>0:
            score[item]=query_count[item]
    if len(score)==0:
        scoreurl=basescore/len(b)
    else:
        scoreurl=basescore+(basescore/len(b))*(len(score)**2)
    
    return scoreurl
#  
# if __name__ == "__main__":
#     print url_score_base("http://twitter.com/nyupoly/lists","nyu poly")[2]
