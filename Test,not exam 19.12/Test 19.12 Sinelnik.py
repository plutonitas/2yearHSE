import re
import json
from flask import Flask
from flask import render_template, request, redirect, url_for

app = Flask(__name__)

def DicFile():
    dic = {}
    with open('dict.xdfx', 'r', encoding = 'utf-8') as fu:
        file = fu.read()
        Basqregex = '<k>(.*?)</k>'
        Engregex = '</k>\n(.*?)</ar>'
        basq = re.findall(Basqregex, file)
        eng = re.findall(Engregex, file)
        #print(len(basq),len(eng))
        for i in range(len(eng)-1):
            dic[basq[i]] = [eng[i]]
        #print(dic)
        basqEng = open('basqEng.json', 'w', encoding = 'utf-8')
        json.dump(dic, basqEng)
        basqEng.close() 
        inverteddic = {eng[0]:basq for basq, eng in dic.items()}
        for keys in inverteddic.keys():
            keys = list(keys)
        engBasq = open('engBasq.json','w', encoding = 'utf-8')
        json.dump(inverteddic, engBasq)
        
        engBasq.close()
## "английское слово ключ, а тайское(баскское) слово -- в значении
## (но в значении будет массив, потому что соответствия не взаимно однозначные)"
##Не очень понятно, как это делается с баскским словарём, если слово на баскском одно,
##а переводов на английский несколько.Тогда и получается, что массив может быть из нескольких
##англ слов, а из баскских нет (или у меня еррор в понимании)
@app.route('/')
def dicsearch():
    return render_template('search.html')

@app.route('/results')
def results():
    res = []
    with open('engBasq.json','r', encoding = 'utf-8') as f:
        newdic = json.loads(f.read())
        transSearch = request.args.get('engWord')
        for words in newdic:
            if transSearch == words:
                res.append([words, newdic[words]])
    return render_template('result.html', res=res, transSearch= transSearch)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
DicFile()
dicsearch()
results()


        
