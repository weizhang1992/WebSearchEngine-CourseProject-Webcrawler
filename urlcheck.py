import urlparse

URLEnd = ['main.html','index.html','index.jsp','main.htm','index.htm'] 

def RemoveURLEnd(normalLink):
    for endstr in URLEnd:
        if endstr in normalLink:
            startpos = normalLink.find(endstr)
            beforeStr = normalLink[0:startpos]
            if len(normalLink[startpos:]) > len(endstr):
                if normalLink[startpos+len(endstr)] == '/':
                    afterStr = normalLink[startpos+len(endstr)+1:-1]
                else:
                    afterStr = normalLink[startpos+len(endstr):-1]
                return beforeStr + afterStr
            else:
                return beforeStr
    return normalLink                                 

def CheckLink(currentLink,status):
    url = urlparse.urlparse(currentLink)
    url = RemoveURLEnd(url)
    if status==True:
        if url[0] not in ['http','https']:   # skip other protocols like ftp://
            return False,url
        if 'cgi-bin' in url[2]:    #skip the url which includes 'cgi-bin'
            return False,url
    return True,url
    
    

