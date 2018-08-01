from gevent import monkey; monkey.patch_all()
from bottle import route, run, response, request
import bottle
import csv
import sys
import json
import statistics

class EnableCors(object):
    name = 'enable_cors'
    api = 2
    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
            if bottle.request.method != 'OPTIONS':
                return fn(*args, **kwargs)
        return _enable_cors

global Questions
global Answers
global JumpsoulSurvey

Questions = []
JumpsoulSurvey = []
Answers = [[],[],["Male", "Female"], ["<24", "25-29","30-34", "35-40", "40+"], ["Very Often", "Sometimes", "Rarely", "Never"], ["Yes","No"], [], ["While reading an article/journal on health","While watching Advertisements","Checking myself out in the mirror/selfie/photo","Waking up in the morning","While watching movies/series","While having a meal","Others"] ,["Better Focus, Attention, or Concentration","More Physically Active","Better Immunity","More Stamina","Better Weight Management","Better Stress Management","More Patience","More Self-confident","More Optimistic","Others"], ["Menstrual Cramps","Headache/Fever","Acidity/Indigestion/Constipation","Cold/Cough","Stress","Oral Problems","Muscular Ache","Hair Loss/thinning/damage","Vision Related Problems - Blurry vision, dry eyes, etc.","Skin Problems","Memory or Cognitive Functions","Sleep Related - Insomnia, Difficulty Falling Asleep, etc.","Low Energy","Others"], ["Yes","No"], [], ["Meat", "Dairy products", "None"], ["Yes", "No"], ["Doctor", "Online Research", "Referral", "Nutritionist", "Others"], ["Always", "Intermittently"], ["During/with meals","Before a meal","After a meal","No fixed routine","Others"], ["Offline Store", "Online Store", "Nutritionist's/Doctors Samples","Others"], ["Quality", "Price", "Brand", "Ingredients Sources", "Others"], ["Ayurvedic", "Non-Ayurvedic", "Whatever is available"], ["1","2","3","4","5","6","7","8","9","10"], ["Potency","Activation Time", "Transparency - ingredients and side-effects","Availability","Packaging","Others"], ["Reduce/Quit Smoking","Responsible Drinking","Manage Eating Habits","Exercise more or be more physically active","Maintain better personal hygiene","Get adequate sleep or maintain a better sleep cycle","Spend more time with friends and family","Be more productive at work","Focus more on appearance","Others"], ["Family","Peer Group","Work Place","Media/Advertisements","Others"], ["1","2","3","4","5"], [], ["1","2","3","4","5"],[],[],["Tablets/ Capsules","Powder/ Instant mixes","Gummy bears/ candies (Chewables)","Protein powder ","Drops ","Others"],[],[],[],[]]

numbers = [2,3,4,5,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,26,29]

app = bottle.app()

def readJumpsoulSurveydata():
    global Questions
    global JumpsoulSurvey
    Questions = []
    JumpsoulSurvey = []
    with open('JumpSoulSurvey-Combined.csv','r') as fil:
        reader = csv.reader(fil)
        i = 0
        for row in reader:
            if i == 0:
                Questions = row
            else:
                JumpsoulSurvey.append(row)
            i += 1

@app.route('/getheaderdata')
def getheaderdata():
    global Questions
    yield json.dumps(Questions)

@app.route('/getdistinctcolumndata/<columns>')
def getdisticnctcolumndata(columns):
    global Questions
    global JumpsoulSurvey
    result = []
    for i in range(len(JumpsoulSurvey)):
        if JumpsoulSurvey[i][int(columns)] not in result:
            result.append(JumpsoulSurvey[i][int(columns)])
    yield json.dumps(result)

@app.route('/getdistinctmultipledatacolumn/<column>')
def getdistinctmultipledatacolumn(column):
    global Questions
    global JumpsoulSurvey
    result = []
    for i in range(len(JumpsoulSurvey)):
        sting = (JumpsoulSurvey[i][int(column)]).split(';')
        for srt in sting:
            if srt not in result:
                result.append(srt)
    yield json.dumps(result)

@app.post('/getfilterdatavisualize_new')
def getfilterdatavisualize_new():
    global Questions
    global JumpsoulSurvey
    filters = json.loads(request.forms.get("filters"))
    column = int(request.forms.get("column"))
    data = []
    for i in range(len(JumpsoulSurvey)):
        c = 0
        for key in filters:
            if key in ['2','4','5','10','13','20','24','26','29']:
                if JumpsoulSurvey[i][int(key)] == filters[key] :
                    c += 1
            if key == '3':
                if filters[key] == '<24':
                    if int(JumpsoulSurvey[i][int(key)]) <= 24:
                        c += 1
                elif filters[key] == '25-29':
                    if int(JumpsoulSurvey[i][int(key)]) >= 25 and int(JumpsoulSurvey[i][int(key)]) <= 29:
                        c += 1
                elif filters[key] == '30-34':
                    if int(JumpsoulSurvey[i][int(key)]) >= 30 and int(JumpsoulSurvey[i][int(key)]) <= 34:
                        c += 1
                elif filters[key] == '35-40':
                    if int(JumpsoulSurvey[i][int(key)]) >= 35 and int(JumpsoulSurvey[i][int(key)]) <= 40:
                        c += 1
                elif filters[key] == '40+':
                    if int(JumpsoulSurvey[i][int(key)]) > 40:
                        c += 1
            if key in ['7','8','9','12','14','15','16','17','18','19','21','22','23']:
                if filters[key] != "Others" :
                    for sting in (JumpsoulSurvey[i][int(key)]).split(';'):
                        if sting == filters[key]:
                            c +=1
                            break
                else:
                    anwoth = [ans for ans in Answers[int(key)] if ans!='Others']
                    for sting in (JumpsoulSurvey[i][int(key)]).split(';'):
                        if sting not in anwoth:
                            c += 1
                            break
        if c == len(filters.keys()):
            data.append(JumpsoulSurvey[i][int(column)])
    result = {}
    answ = Answers[int(column)]
    for ans in answ:
        result[ans] = 0
    if len(data) != 0 :
        for i in range(len(data)):
            if int(column) in [7,8,9,12,14,15,16,17,18,19,21,22,23]:
                stdans = [ans for ans in answ if ans!='Others']
                for dat in data[i].split(';'):
                    if dat in stdans:
                        result[dat] += 1
                    else:
                        if dat == "" or dat == "I AM A DOCTOR" or dat == "NO ISSUE":
                            if 'NULL' in result.keys():
                                result['NULL'] += 1
                            else:
                                result['NULL'] = 1
                        else:
                            if 'Others' in result.keys():
                                result['Others'] += 1
                            else:
                                result['Others'] = 1
            if int(column) in [2,4,5,10,13,20,24,26,29]:
                if data[i] in [ans for ans in result.keys() if ans!='Others']:
                    result[data[i]] += 1
                elif data[i] == "":
                    if 'NULL' in result.keys():
                        result['NULL'] += 1
                    else:
                        result['NULL'] = 1
                else:
                    if 'Others' in result.keys():
                        result['Others'] += 1
                    else:
                        result['Others'] = 1
            if int(column) == 3:
                if int(data[i]) <= 24:
                    result['<24'] += 1
                elif int(data[i]) >= 25 and int(data[i]) <= 29:
                    result['25-29'] += 1
                elif int(data[i]) >= 30 and int(data[i]) <= 34:
                    result['30-34'] += 1
                elif int(data[i]) >= 35 and int(data[i]) <= 40:
                    result['35-40'] += 1
                elif int(data[i]) > 40:
                    result['40+'] += 1
        percen = 0
        for key in result:
            result[key] = (result[key]*100)/len(data)
            percen += result[key]
        if percen == 100.0:
            resultlist = [[Questions[int(column)],"Percent"]]
            for key in result:
                resultlist.append([key,result[key]])
            yield json.dumps({"data":resultlist,"chart":1})
        else:
            colors = ["#b87333","silver","gold","green","red","blue","orange","black","#1A5276","#C70039","FB8C00","BF360C","#455A64","#827717","#33691E"]
            resultlist = [[Questions[int(column)],"Percent",{'role':"style"}]]
            i = 0
            for key in result:
                resultlist.append([key,result[key],colors[i]])
                i += 1
            yield json.dumps({"data":resultlist,"chart":2})
    else:
        resultlist = [[Questions[int(column)],"Percent"]]
        for key in Answers[int(column)]:
            resultlist.append([key,0])
        yield json.dumps({"data":resultlist,"chart":1})

readJumpsoulSurveydata()

app.install(EnableCors())
app.run(host='0.0.0.0', port=5000, debug=True, server='gevent')
