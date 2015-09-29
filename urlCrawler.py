from __future__ import print_function
from urlinitials import gbaseurl
from urlscore import url_score,url_score_base
from urlcheck import CheckLink
from urlfilter import FilterMIME
from urlrobot import accessRight
from urllinks import Get_link
from urllib2 import URLError
import time,heapq,os

#set you query and maxpage at here:
thequery="nyu poly"
maxpage=20 

save = "/Users/vee/space_python/Webcrawler/result_file/"+thequery+"/"   

def savePage(dataread,pageID):   
    try:
        path=save +"url_download/"+"page_"+str(pageID)+".html"
        output = open(path,'wb')
        output.write(dataread)
        output.close()
    except URLError, e:
        print ("download error:",e.reason)
        
def part(url):   
    if "https" in url:
        return url[5:]
    else:
        return url[4:]
            
def appendlist(Crawled,tempList,time,size,feedback,urlcode):   
    tempList.append(time)            #Time_stamp
    tempList.append(size)                      #length
    tempList.append(feedback)       # error/feedback
    tempList.append(urlcode)       # error/feedback
    Crawled[tempList[0]]=tempList



def WebCrawl( initial_urls,thequery, max_pages):   # get Top N results from google, set max depth and max pages you need 
    heapinserted=0
    urlheap=[]              # BFS uses a queue here
    for item in initial_urls:
        heapinserted+=1
        score,data,status,code,contenttype=url_score_base(item,thequery)
        print ('scoring links:','score:',score,',','Code:',code,',''url:',item )
        heapq.heappush(urlheap, (score, item, 0,data,status,code,contenttype))
    starttime = time.time()
    Crawled = {}                  # make a List which can store info about visited urls in visiting order.  
    CrawledSuccessful = {}        # make a Dict which can store Key(url) and Value(depth,timestamp,size,feedback);  
    PageID = 0
    depth=0
    
    while len(urlheap)> 0 and len(CrawledSuccessful) < max_pages and depth<10:

        heapq._heapify_max(urlheap)
        PageID=PageID+1
         
        top=heapq.heappop(urlheap)
        currentURL=top[1]
        depth=top[2]
        score,dataread,Status,urlcode,contenttype=url_score_base(currentURL,thequery)
        
        while score==0:
            top=heapq.heappop(urlheap)
            currentURL=top[1]
            depth=top[2]
            score,dataread,Status,urlcode,contenttype=url_score_base(currentURL,thequery)
            
        Status,URL = CheckLink(currentURL,Status)
        
        if dataread==0:
            print ('ID:',PageID,',','Time:',time.strftime('%l:%M%p %b%d %Y'),',','score:',score,',','Depth:', depth,',','Access:',accessRight(currentURL),',','Code:',urlcode,',','Size',0,',','url:', currentURL)    
            print ('ID:',PageID,',','Time:',time.strftime('%l:%M%p %b%d %Y'),',','score:',score,',','Depth:', depth,',','Access:',accessRight(currentURL),',','Code:',urlcode,',','Size',0,',','url:', currentURL,file=flog)
        else:
            print ('ID:',PageID,',','Time:',time.strftime('%l:%M%p %b%d %Y'),',','score:',score,',','Depth:', depth,',','Access:',accessRight(currentURL),',','Code:',urlcode,',','Size',str(len(dataread)/1000)+'KB',',','url:', currentURL)    
            print ('ID:',PageID,',','Time:',time.strftime('%l:%M%p %b%d %Y'),',','score:',score,',','Depth:', depth,',','Access:',accessRight(currentURL),',','Code:',urlcode,',','Size',str(len(dataread)/1000)+'KB',',','url:', currentURL,file=flog)
        
        tempList = [currentURL,score,depth]  
        if Status == False or accessRight(currentURL) == False or FilterMIME(contenttype)== False:# if an invalid or forbidden page or disallowed MIME type , skip it
            appendlist(Crawled,tempList,time.strftime('%l:%M%p, %b %d, %Y'),0,'Failure',urlcode)
            continue       
        else:           
            try:    
                             
                lengthOfPage = len(dataread)
                
                if heapinserted<3*max_pages:  
                    links=Get_link(dataread)
                    i=0
                    for link in links:  # normalize the urls (e.g. relative path)
                        i=i+1
                        if link.startswith('/'):
                            link = 'http://' + URL[1] + link
                        elif link.startswith('#'):
                            link = 'http://' + URL[1] + URL[2] + link
                        elif not link.startswith('http'):
                            link = 'http://' + URL[1] + '/' + link
                        if part(link) not in [part(k) for k in Crawled.keys()] and part(link) not in  [part(s[1]) for s in urlheap]:
                            if part(link)!=part(currentURL):
                                if not link.count("#"):
                                    heapinserted+=1
                                    if heapinserted>3*max_pages:
                                        break
                                                        
                                    linkgrade=url_score(link,thequery,score)
                                     
                                    heapq.heappush(urlheap, (linkgrade,link,depth+1))                                    
                                    if i>100:
                                        break                        
                savePage(dataread,PageID)
                appendlist(Crawled,tempList,time.strftime('%l:%M%p, %b %d, %Y'),lengthOfPage,'Success',urlcode)
                CrawledSuccessful[currentURL]=tempList   # create a new (key,value) pair in the dict
            except:
                appendlist(Crawled,tempList,time.strftime('%l:%M%p, %b %d, %Y'),0,'Failure',urlcode)
                continue
    endtime = time.time()
    totaltime = endtime - starttime   
    return Crawled, CrawledSuccessful,totaltime

def showTotalSize(CrawledSuccessful):
    totalsize = 0
    for item in CrawledSuccessful.values():
        totalsize = totalsize + item[4]
    return totalsize/1000000

#########################################################################################################################    

if __name__ == '__main__':
    if not os.path.exists(save):
        os.makedirs(save)
    if not os.path.exists(save+"url_download/"):
        os.makedirs(save+"url_download/")
    pathlog=save +"crawled_log.txt"
    flog=open(pathlog,'w')
            
    initial_urls = gbaseurl(thequery)  # Top 10 results
    crawled,crawled_successful,total_time = WebCrawl(initial_urls, thequery, maxpage)
    print ('##############################################################################################################')
    print ('##############################################################################################################',file=flog)
    print ('The total number of crawled pages: ', len(crawled),file=flog)
    print ('The total number of crawled pages: ', len(crawled))

    print ('##############################################################################################################',file=flog)
    print ('The total number of successful pages: ', len(crawled_successful),file=flog)
    print ('The total number of successful pages: ', len(crawled_successful))
 
    print ('##############################################################################################################',file=flog)
    print ('The total size of successful pages: ',showTotalSize(crawled_successful),file=flog)
    print ('The total size of successful pages: ',showTotalSize(crawled_successful),'MB')
 
    print ('##############################################################################################################',file=flog)
    print ('The total time: ',total_time,file=flog)
    print ('The total time: ',total_time)
    
    flog.close()

        
  
    
