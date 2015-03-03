# This Python file uses the following encoding: utf-8

from flask import Flask
app = Flask(__name__)

def listclassfromsoup(c,soup):
    div=soup.find_all('div',class_=c)
    contents=[BeautifulSoup(str(d)) for d in div]
    return [content.get_text() for content in contents]

def diadasemana(dia):
    d=dia.isoweekday()
    dias=["segunda","terça","quarta","quinta","sexta",unicode("sábado", 'utf-8'),"domingo"]
    return dias[d-1]

def agenda(entries):
    r=requests.get('http://www.fcporto.pt/pt/futebol/calendario/Pages/calendario.aspx')
    soup = BeautifulSoup(r.text)
    categorias = listclassfromsoup('cal_entry c_cat',soup)
    fases = listclassfromsoup('cal_entry c_fase',soup)
    datas = listclassfromsoup('cal_entry c_data',soup)
    horas = listclassfromsoup('cal_entry c_hora',soup)
    locais = listclassfromsoup('cal_entry c_local',soup)
    homes = listclassfromsoup('cal_entry c_equipa_home',soup)
    aways = listclassfromsoup('cal_entry c_equipa_away',soup)
    phrases =[]
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    for data in datas:
        n = datas.index(data)
        data = datetime.datetime.strptime(data, "%d-%m-%Y").date()
        if data>=today:
            if homes[n]=="FC Porto":
                versus=aways[n]
            else:
                versus=homes[n]
            quando=" no dia "+datas[n]
            if data-today<datetime.timedelta(days=6):
                quando=", "+diadasemana(data)
            if data==today:
                quando=", hoje"
            if data==tomorrow:
                quando=unicode(", amanhã", 'utf-8')
            phrase="vs "+versus+quando
            if len(horas[n])==5:
                phrase=phrase+unicode(" às ", 'utf-8')+horas[n]
            phrase=phrase+", "+locais[n]+", "+categorias[n]
            phrases.append(phrase)
    text=""
    if entries+1>len(phrases):
        entries = len(phrases)-1
    for n in range(0,entries):
        text=text+phrases[n]+"\n"
    return text

@app.route('/fcp/<int:n>')
def fcp(n):
    return agenda(n)
    
@app.route('/')
def home():
    return 'fcp'

if __name__ == '__main__':
    import requests
    import datetime
    from bs4 import BeautifulSoup
    app.debug=True
    app.run()
