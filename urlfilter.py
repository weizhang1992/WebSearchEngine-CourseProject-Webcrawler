

AllowMIME=['text/html','text/plain','application/x-perl','application/x-asap']

def FilterMIME(contenttype):
    if contenttype==None:
        return False
    content_Type = contenttype
    for item in AllowMIME:
        if item not in content_Type:
            continue
        else:
            return True
    return False

