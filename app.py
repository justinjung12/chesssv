from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)
def Toint(string):
    # 정규표현식을 사용하여 숫자 부분만 추출
    number = re.search(r'\d+', string)
    
    if number:
        return int(number.group())  # 추출된 숫자를 정수로 변환하여 반환
def reverse(pos):
    pos['king'][0][1] = str(358 - Toint(pos['king'][0][1]) + 8) + 'px'
    pos['queen'][0][1] = str(358 - Toint(pos['queen'][0][1]) + 8) + 'px'
    for i,v in enumerate(pos['rook']):
        pos['rook'][i][1] = str(358 - Toint(v[1]) + 8) + 'px'

    for i,v in enumerate(pos['bishop']):
        pos['bishop'][i][1] = str(358 - Toint(v[1]) + 8) + 'px'
    
    for i,v in enumerate(pos['knight']):
        pos['knight'][i][1] = str(358 - Toint(v[1]) + 8) + 'px'

    for i,v in enumerate(pos['pawn']):
        pos['pawn'][i][1] = str(358 - Toint(v[1]) + 8) + 'px'
    return pos
room = [{'roomnumber':12345,'enterpeople':1,'hostnickname':'wj','opponent':'ww'}]
roomchesspos = [{'roomnumber':12345,'hostpos':{},'opponentpos':{}}]
whoseturn = [{'roomnumber':12345,'turn':'wj'}]
caughtlist = [{'roomnumber':12345,'piece':'pawn','index':0,'whocatch':'wj'}]
surrender = [{'roomnumber':12345,'winner':'wj'}]
startpos = {

        "king": [
            [
                "158px",
                "8px"
            ]
        ],
        "queen": [
            [
                "208px",
                "8px"
            ]
        ],
        "rook": [
            [
                "8px",
                "8px"
            ],
            [
                "358px",
                "8px"
            ]
        ],
        "bishop": [
            [
                "108px",
                "8px"
            ],
            [
                "258px",
                "8px"
            ]
        ],
        "knight": [
            [
                "58px",
                "8px"
            ],
            [
                "308px",
                "8px"
            ]
        ],
        "pawn": [
            [
                "8px",
                "58px"
            ],
            [
                "58px",
                "58px"
            ],
            [
                "108px",
                "58px"
            ],
            [
                "158px",
                "58px"
            ],
            [
                "208px",
                "58px"
            ],
            [
                "258px",
                "58px"
            ],
            [
                "308px",
                "58px"
            ],
            [
                "358px",
                "58px"
            ]
        ]


    }






@app.route('/',methods=['POST'])


def index():
    data = request.get_json()
    if(data['type'] == 'enter'):
        for i,l in enumerate(room):
            if(l['roomnumber'] == data['roomnumber']):
                room[i]['enterpeople'] += 1
                room[i]['opponent'] = data['nickname']
                break

    if(data['type'] == 'make'):
        
        roomchesspos.append({'roomnumber':data['roomnumber'],'hostpos':startpos, 'opponentpos':startpos})
        room.append({'roomnumber':data['roomnumber'],'enterpeople':1,'hostnickname':data['nickname'],'opponent':''})
        whoseturn.append({'roomnumber':data['roomnumber'],'turn':data['nickname']})
        for ind,m in enumerate(whoseturn):
            if(m['roomnumber'] == data['roomnumber']):
                whoseturn[ind]['turn'] = data['nickname']
    return jsonify(data)





@app.route('/waiting',methods=['POST'])


def waiting():
    data = request.get_json()
    for x in room:
        if(x['roomnumber'] == data['roomnumber']):
            if(x['enterpeople'] == 2):
                return jsonify({'ok':True})
            else:
                return jsonify({'ok':False})
    
    return 'error'


@app.route('/getpos',methods=['POST'])


def getpos():
    data = request.get_json()
    for i,k in enumerate(roomchesspos) :
        if(k['roomnumber'] == data['roomnumber']):
            if(room[i]['hostnickname'] == data['nickname']):
                for ix,c in enumerate(caughtlist):
                    if(c['roomnumber'] == data['roomnumber']):
                        return jsonify({'pos':k['hostpos'],'turn':whoseturn[i]['turn'],'caught':caughtlist[ix],'surrender':surrender})
                return jsonify({'pos':k['hostpos'],'turn':whoseturn[i]['turn'],'caught':'no','surrender':surrender})
            elif(room[i]['opponent'] == data['nickname']):
                for ix,c in enumerate(caughtlist):
                    if(c['roomnumber'] == data['roomnumber']):
                        return jsonify({'pos':k['opponentpos'],'turn':whoseturn[i]['turn'],'caught':caughtlist[ix],'surrender':surrender})

                return jsonify({'pos':k['opponentpos'],'turn':whoseturn[i]['turn'],'caught':'no','surrender':surrender})

            
    return 'error'




@app.route('/changpos',methods=['POST'])

    


def changepos():
    istrue = False
    data = request.get_json()
    for index,k in enumerate(room):
        if(k['roomnumber'] == data['roomnumber']):

            if(k['hostnickname'] == data['nickname']):
                roomchesspos[index]['opponentpos'] = reverse(data['pos'])
                whoseturn[index]['turn'] = k['opponent']
                if(data['caught'] != 'no'):
                    for ie,h in enumerate(caughtlist):
                        if(h['roomnumber'] == data['roomnumber']):
                            caughtlist[ie] = {'roomnumber':data['caught']['roomnumber'],'piece':data['caught']['piece'],'index':data['caught']['index'],'whocatch':data['caught']['whocatch']}
                            print('호스트가 상대편 말을 잡음'+' '+data['caught']['piece'])
                            istrue = True
                    if(istrue == False):
                        print('호스트가 상대편 말을 처음 잡음'+' '+data['caught']['piece'])
                        caughtlist.append({'roomnumber':data['caught']['roomnumber'],'piece':data['caught']['piece'],'index':data['caught']['index'],'whocatch':data['caught']['whocatch']})
            
            
            elif(k['opponent'] == data['nickname']):
                roomchesspos[index]['hostpos'] = reverse(data['pos'])
                whoseturn[index]['turn'] = k['hostnickname']
                if(data['caught'] != 'no'):
                    for ie,h in enumerate(caughtlist):
                        if(h['roomnumber'] == data['roomnumber']):
                            print('상대가 호스트 말을 잡음'+' '+data['caught']['piece'])
                            caughtlist[ie] = {'roomnumber':data['caught']['roomnumber'],'piece':data['caught']['piece'],'index':data['caught']['index'],'whocatch':data['caught']['whocatch']}
                            istrue = True
                    if(istrue == False):
                        print('상대가 호스트 말을 처음 잡음'+' '+data['caught']['piece'])
                        caughtlist.append({'roomnumber':data['caught']['roomnumber'],'piece':data['caught']['piece'],'index':data['caught']['index'],'whocatch':data['caught']['whocatch']})

            
            
            else:
                return 'error'
    return 'ok'
@app.route('/surrender',methods=['POST'])


def Surrender():
    print("giveup")
    data = request.get_json()
    for i in room:
        if(i['roomnumber'] == data['roomnumber']):
            if(i['hostnickname'] == data['nickname']):
                print("giveuphost")
                surrender.append({'roomnumber':data['roomnumber'],'winner':i['opponent']})
            elif(i['opponent'] == data['nickname']):
                print("giveup")
                surrender.append({'roomnumber':data['roomnumber'],'winner':i['hostnickname']})

            
    return ''




    
