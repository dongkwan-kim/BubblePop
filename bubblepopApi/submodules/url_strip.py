

def url_strip(url):
    idx =  url.find('?')
    if(idx==-1):
        return url
    return url[:idx]



