from flask import *
import json
import os
import re

app = Flask(__name__)

@app.route('/')
def database():
    if os.path.exists('questions.json'):
        with open('questions.json', 'r') as f_quest:
            quest = json.load(f_quest)
        if '' in [i[1] for i in quest] or len(quest) != len(set([q[1] for q in quest])):
            return redirect('/manage')            
    else:
        return redirect('/manage')
    
    if os.path.exists('database.json'):
        with open('database.json','r') as f_in:
            data = json.load(f_in)
    else: 
        data = {}
        for q in quest:
            data[q[1]] = []
    
    for key in request.args:
        data[key].append(request.args[key])

    f_out = open('database.json', 'w')
    json.dump(data, f_out, ensure_ascii=False)
    f_out.close()
    
    return render_template('front_page.html', quest=quest, num=len(quest)) 

    
@app.route('/stats')
def stats():
    if os.path.exists('database.json'):
        with open('database.json','r') as sta_f:
            stat = json.load(sta_f)
        num = None
    else:
        stat = {}
        num = 0
        
    if os.path.exists('questions.json'):
        with open('questions.json', 'r') as f_quest:
            quest = json.load(f_quest)
        if '' in [i[1] for i in quest] or len(quest) != len(set([q[1] for q in quest])):
            return redirect('/manage')
    else:
        return redirect('/manage')
        
    if num == None:
        num = len(stat[quest[0][1]])
    return render_template('stats.html', stat=stat, ind=quest, num=num)
    
@app.route('/manage/')
def manage():
    if os.path.exists('questions.json'):
        with open('questions.json', 'r') as f_quest:
            quest = json.load(f_quest)
    else:
        quest = [['', '', '']]
    namesbefore = [q[1] for q in quest]

    if request.args != {}:
        for i in range(len(quest)):
            quest[i][0] = request.args['qu' + str(i)]
            quest[i][1] = request.args['name' + str(i)]
            quest[i][2] = request.args['capt' + str(i)]
        for i in range(len(quest)):
            if 'del' + str(i) in request.args:
                quest[i] = None
        quest = [i for i in quest if i != None]
        if 'add' in request.args:
            quest.append(['', '', ''])
        elif 'deldb' in request.args or 'delall' in request.args or sorted(namesbefore) != sorted([q[1] for q in quest]):
            if os.path.exists('database.json'):
                os.remove('database.json')
            if 'delall' in request.args:
                quest = [['', '', '']]
                
        f_quest = open('questions.json', 'w')
        json.dump(quest, f_quest )
        f_quest.close()            
        
    if quest == [['', '', '']]:
        disc = 'Анкета не создана!'
    elif '' in [q[1] for q in quest]:
        disc = 'Необходимо ввести все внутренние имена!'
    elif len(quest) != len(set([q[1] for q in quest])):
        disc = 'Все внутренние имена должны быть уникальны!'
    else:
        disc = None
                
    return render_template('manage.html', quest=quest, num=len(quest), disc=disc)

@app.route('/search')
def search():
    if request.args != {}:
        arg = '?'
        for key in request.args:
            arg += key + '=' + request.args[key] + '&'
        return redirect('/results/' + arg[:-1])
    else:
        if os.path.exists('questions.json'):
            with open('questions.json', 'r') as f_quest:
                quest = json.load(f_quest)
            if '' in [i[1] for i in quest] or len(quest) != len(set([q[1] for q in quest])):
                return redirect('/manage')
        else:
            return redirect('/manage')
        return render_template('search.html', quest=quest)
    
@app.route('/results/')
def results():
    if request.args == {}:
        return redirect ('/search')
    else:
        if os.path.exists('database.json'):
            with open('database.json','r') as sta_f:
                stat = json.load(sta_f)
            num = None
        else:
            stat = {}
            num = 0
        query = request.args['q'].lower()
        res = []
        for key in request.args:
            if key == 'q' or request.args[key] == 'off': continue
            else:
                for d in range(len(stat[key])):
                    if d not in res and re.search(query, stat[key][d].lower()) != None:
                        res.append(d)
        num = len(res)
        if num != 0: res.sort()
        with open('questions.json', 'r') as f_quest:
            quest = json.load(f_quest)
        where = []
        for q in quest:
            if q[1] in request.args:
                where.append(q[2])
        return render_template('results.html', stat=stat, quest=quest, res=res, num=num, where=where, query=query)

@app.route('/json')
def givejson():
    if os.path.exists('database.json'):
        with open('database.json','r') as sta_f:
            stat = sta_f.read()
    else:
        stat = ''
    return stat
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)
