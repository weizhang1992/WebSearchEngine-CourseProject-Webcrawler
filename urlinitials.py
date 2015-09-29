import json
import urllib 
import urllib2
    
def gbaseurl(theQuery): 
    result=[]
    url = ('https://ajax.googleapis.com/ajax/services/search/web'
          '?v=1.0&q=%s&rsz=8&start=%s') % (urllib.quote(theQuery),0)
    url2 = ('https://ajax.googleapis.com/ajax/services/search/web'
          '?v=1.0&q=%s&rsz=2&start=%s') % (urllib.quote(theQuery),8)
    try:
        request1 = urllib2.Request(url, None, {'Referer':'http://www.nyu.edu'})
        request2 = urllib2.Request(url2, None, {'Referer':'http://www.nyu.edu'})
        response1 = urllib2.urlopen(request1)
        response2 = urllib2.urlopen(request2)

        results1 = json.load(response1)
        results2 = json.load(response2)
        info1 = results1['responseData']['results']
        info2 = results2['responseData']['results']
        
    except Exception,e:
        print "Google Api Error:", e
        
    for minfo1 in info1:
        result.append(minfo1['url'])
    for minfo2 in info2:
        result.append(minfo2['url'])
    print result
    return result

    
                
