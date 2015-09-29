import urllib2
import robotexclusionrulesparser

def accessRight(currentURL):
    try:
        rerp = robotexclusionrulesparser.RobotExclusionRulesParser()
        robotpath = findBase(currentURL) + '/robots.txt'
        rerp.fetch(robotpath)
        return rerp.is_allowed("*", currentURL)
    except:
        return False
    
def findBase(url):
    proto, rest = urllib2.splittype(url)  
    if proto is None:
        raise ValueError, "unknown URL type: %s" % url
    host, rest = urllib2.splithost(rest) 
    return 'http://' + host
