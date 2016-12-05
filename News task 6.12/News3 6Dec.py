import urllib.request
import re
import html
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'

def getlinks():
    file = open('links.txt','r', encoding = 'utf-8')
    links = file.readlines()
    file.close()
    
    j = 1
    for i in links:
        reqq = urllib.request.Request(i, headers={'User-Agent':user_agent})
        with urllib.request.urlopen(reqq) as response:
            texthtml = response.read().decode('utf-8')
            file = open('texthtml'+str(j)+'.html','w',encoding = 'utf-8')
            file.write(html.unescape(texthtml))
            file.close()
            j += 1
        
def TXT1():
    file = open('texthtml1.html','r',encoding = 'utf-8')
    texthtml = file.read()
    reglink = re.compile(r'<div class=\"newstext\">(.*?)</div>' ,flags = re.DOTALL)
    text = reglink.search(texthtml).group(1)
    text = re.sub('<.*?>|\t|\n','',text)
    text = re.sub('\.|\,|\"|\«|\»|\:',' ',text)

    textset = set(text.lower().split(' '))
    #print(textset)
    return textset
    file.close()
    

def TXT2():
    file = open('texthtml2.html','r', encoding  = 'utf-8')
    texthtml = file.read()
    reglink = re.compile(r'<div class=\"news_body\" data-id=\"2211264\">(.*?)</div>', flags = re.DOTALL)
    text = reglink.search(texthtml).group(1)
    #print(text)
    text = re.sub('<.*?>|\t|\n','',text)
    text = re.sub('\.|\,|\"|\«|\»|\:',' ',text)
    textset = set(text.lower().split(' '))
    #print(textset)
    return textset
    file.close()

def TXT3():
    file = open('texthtml3.html','r',encoding = 'utf-8')
    texthtml = file.read()
    reglink = re.compile(r'<p class="lid">(.*?)<div class=\"article__incut\">', flags = re.DOTALL)
    text = reglink.search(texthtml).group(1)
    text = re.sub('<.*?>|\t|\n','',text)
    text = re.sub('\.|\,|\"|\«|\»|\:',' ',text)
    textset = set(text.lower().split(' '))
    #print(textset)
    return textset
    file.close()

def TXT4():
    file = open('texthtml4.html','r',encoding = 'utf-8')
    texthtml = file.read()
    reglink = re.compile(r'<div itemprop=\"articleBody\">(.*?)<div data-type=\"Incut. By wide\" class=\"b-read-more b-read-more_wide\">', flags = re.DOTALL)
    text = reglink.search(texthtml).group(1)
    text = re.sub('<.*?>|\t|\n','',text)
    text = re.sub('\.|\,|\"|\«|\»|\:',' ',text)
    textset = set(text.lower().split(' '))
    #print(textset)
    return textset
    file.close()

def compare():
    reslist = []
    first = TXT1()
    second = TXT2()
    third = TXT3()
    fourth = TXT4()
    res = first.intersection(second,third,fourth)
    file = open('intersection.txt','w',encoding = 'utf-8')
    for els in sorted(res):
        intrsec = reslist.append(els)
    reslist = [item for item in reslist if not item.isdigit()]
    file.write('\n'.join(reslist))
    file.close()
    

    
def contrast():
    reslist = []
    first = TXT1()
    second = TXT2()
    third = TXT3()
    fourth = TXT4()
    resAB = first.symmetric_difference(second)
    resBC = resAB.symmetric_difference(third)
    resCD = resBC.symmetric_difference(fourth)
    file = open('symdif.txt','w', encoding = 'utf-8')
    for els in sorted(resCD):
        common = reslist.append(els)
    reslist = [item for item in reslist if not item.isdigit()]
    file.write('\n'.join(reslist))
    file.close()
    
    
getlinks()
compare()
contrast()
    
