import urllib.request
import re
import html
from pymystem3 import Mystem
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'

def getText():
    m = Mystem()
    cyrillic = 'абвгдеёжзиклмнопрстуфхцчшщъыьэюя'
    regTag = re.compile('<.*?>.*?', flags= re.DOTALL)
    regTag2 = re.compile('.&nbsp;', flags = re.DOTALL)

                
    req = urllib.request.Request('http://web-corpora.net/Test2_2016/short_story.html',headers={'User-Agent':user_agent})
    with urllib.request.urlopen(req) as response:
        texthtml = response.read().decode('utf-8')
        text = texthtml.split()
        for word in text:
            word = word.strip('\'\".,!?:;-—\(\)')
            newword = re.sub(regTag,'',word)
            newword = re.sub(regTag2,'',newword)

            if newword and newword.lower()[0] in cyrillic:
                    newword = newword.lower()
                    if newword and newword.startswith('с'):
                         #print(newword)
                        morph = m.analyze(newword)
                        #print(morph)
                        noAnalysis = 0
                        for item in morph:
                            try:
                                for parsing in item['analysis']:
                                    if parsing['gr'] and ('V' in parsing['gr']):
                                        print(array['text'])
                            except:
                                noAnalysis += 1
                                    
                                                                        
                
                
                
        

getText()

