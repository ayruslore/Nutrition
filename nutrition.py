from gevent import monkey; monkey.patch_all()
from bottle import route, run, response
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

global header
global Jumpsouldata

header = []
Jumpsouldata = []

app = bottle.app()

def makeJumpsouldata():
    global header
    global Jumpsouldata
    header = []
    Jumpsouldata = []
    with open('JumpSoulSurvey-Combined.csv','r') as fil:
        reader = csv.reader(fil)
        i = 0
        for row in reader:
            if i == 0:
                header = row
            else:
                Jumpsouldata.append(row)
            i += 1

@app.route('/getcolumns')
def getcolumns():
    global header
    print(len(header))
    yield json.dumps(header)

@app.route('/getfilterdatavisualize/<filters>/<column>')
def filterdatavisualize(filters,column):
    global header
    global Jumpsouldata
    filters = json.loads(filters)
    data = []
    for i in range(len(Jumpsouldata)):
        c = 0
        for key in filters:
            val = header[int(key)]
            if key == '3':
                if filters[key] == '24':
                    if int(Jumpsouldata[i][int(key)]) <= int(filters[key]):
                        c += 1
                elif filters[key] == '25-29':
                    if int(Jumpsouldata[i][int(key)]) >= 25 and int(Jumpsouldata[i][int(key)]) <= 29:
                        c += 1
                elif filters[key] == '30-34':
                    if int(Jumpsouldata[i][int(key)]) >= 30 and int(Jumpsouldata[i][int(key)]) <= 34:
                        c += 1
                elif filters[key] == '35-40':
                    if int(Jumpsouldata[i][int(key)]) >= 35 and int(Jumpsouldata[i][int(key)]) <= 40:
                        c += 1
                elif filters[key] == '40':
                    if int(Jumpsouldata[i][int(key)]) > 40:
                        c += 1
            elif key in ['12', '18', '19']:
                sting = Jumpsouldata[i][int(key)].split(';')
                for srt in sting:
                    if srt.lower() in filters[key].lower():
                        c += 1
                        Jumpsouldata[i][int(key)] = srt
            elif key in ['14', '17'] :
                if filters[key].lower() in Jumpsouldata[i][int(key)].lower():
                    c += 1
                    Jumpsouldata[i][int(key)] = filters[key]
            else:
                if Jumpsouldata[i][int(key)] == filters[key]:
                    c += 1
        if c == len(filters.keys()) :
            data.append(Jumpsouldata[i])
    result = {}
    for i in range(len(data)):
        if data[i][int(column)] not in result:
            result[data[i][int(column)]] = 1
        else:
            result[data[i][int(column)]] += 1
    resultlist = [[header[int(column)], 'Count']]
    for key in result:
        resultlist.append([key, result[key]])
    yield json.dumps(resultlist)

@app.route('/getcolumndata/<columns>')
def getcolumndata(columns):
    global header
    global Jumpsouldata
    result = []
    for i in range(len(Jumpsouldata)):
        if Jumpsouldata[i][int(columns)] not in result:
            result.append(Jumpsouldata[i][int(columns)])
    yield json.dumps(result)

@app.route('/multipledatacolumn/<column>')
def getmultipledatacolumn(column):
    global header
    global Jumpsouldata
    result = []
    for i in range(len(Jumpsouldata)):
        sting = Jumpsouldata[i][int(column)]
        sting = sting.split(';')
        for srt in sting:
            if srt not in result:
                result.append(srt)
    yield json.dumps(result)

makeJumpsouldata()

app.install(EnableCors())
app.run(host='0.0.0.0', port=5000, debug=True, server='gevent')
