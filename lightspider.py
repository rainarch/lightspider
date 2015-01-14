import sys,os
import re
import time
import random
import requests
from BeautifulSoup import BeautifulSoup

if(len(sys.argv) != 1):
    print "Usage: python2 this.py config.file"
    exit;

config_filename = sys.argv[1]
print "Loading config.file="+config_filename
configfp =  open(config_filename, 'r', 0)

configfp.close()
site = "http://www.newsmth.net"
url = "http://www.newsmth.net/nForum/board/Joke"
#url = site+"/nForum/board/Joke?p=2"



###################
#Fucntions Zone
###################

def getPage(url):
    sec = 1;
    while True:
        try:
            response = requests.get(url)
            print "Status Code="+str(response.status_code)
            break;
        except Exception,e:
            print e
            if e > 3600:
                break;
            print "ERROR in request and sleep " + str(sec) +" seconds..."
            time.sleep(sec)
            sec += 5;
    #had a page
    try:
        # parse html
        page = str(BeautifulSoup(response.content))
    except Exception,e:
        print e
        page = "ERROR in parsing the page!"
    return page   

def getURL(page):
    """

    :param page: html of web page (here: Python home page) 
    :return: urls in that page 
    """
    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url, end_quote

def getAllURL(page):
    global urlID
    global added_urls
    global logfp
    add_n = 0;
    while True:
      url, n = getURL(page)
      page = page[n:]
      if url :
          if checkURL(url) == 1:
              if  url not in added_urls:
                urls[urlID] = url
                added_urls[url] = urlID
                logfp.write("NEWURL "+str(urlID)+" "+url+"\r\n")
                urlID += 1
                add_n+=1    
          #print url
      else:
          break
    print "New "+str(add_n)+" urls added!"

def checkURL(url):
    if url.find("Joke") == -1:
        return 0
    if url.find("post") >-1:
        return 0
    if url.find("mail") >-1:
        return 0
    if url.find("reply") >-1:
        return 0
    if url.find("ajax") >-1:
        return 0
    return 1

def writePage(url,page, urlID):
    filename = "pages/page_"+str(urlID);
    fp = open(filename, 'w')
    fp.write(url+"\r\n")
    fp.write(page)
    fp.close( )            
#################
#Main Zone
#################
logfp = open("log.txt", 'w', 0)
urlID = 0;
urls = {}
added_urls = {};
urls[urlID] = url;
added_urls[url] = urlID
urlID += 1
runID = 0;
while True:
    if(runID >= len(urls)):
        break
    next_url = urls[runID];
    if not re.match("http:", next_url):
        next_url = site+next_url
    print "Fetching "+str(runID)+"/"+str(len(urls))+ " page:"+next_url
    page = getPage(next_url)
    writePage(next_url, page, runID)
    logfp.write("GotPAGE "+next_url+" "+str(runID)+"/"+str(len(urls))+"\r\n")
    runID += 1
    print "Done"
    getAllURL(page)
    sec = random.randint(0, 5)
    print "Waiting for "+str(sec)+" seconds..."
    time.sleep(sec)

logfp.close()
print "The END! Let's party!"
