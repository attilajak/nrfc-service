from quart import jsonify
from quart import make_response, Quart, render_template, url_for
from quart import Quart,request, g
from quart_openapi import Pint, Resource
import json
import urllib3
import logging


#app = Quart(__name__)
app = Pint(__name__, title='NRFC')

nrfaddressfile = open("nrfaddress.json", "r")
nrfaddress = json.loads(nrfaddressfile.read())

nrfaddressfile.close()

http = urllib3.PoolManager()

@app.route('/')
class Root(Resource):
    async def get(self):
        response="Nnrf_NFManagement Service\n"
        return response
@app.route('/nrfclient/register/<instanceid>',methods=['PUT'])
class Register(Resource):
    async def put(self,instanceid):
        response="register instance "+instanceid+"\n"
        print(response)
        nfprofile = await request.get_json(force=True)
        print(nfprofile)
        con = http.request('PUT','https://'+nrfaddress[0]["ip"]+":"+ str(nrfaddress[0]["port"])+'/nnrf-nfm/v1/nf-instances/'+instanceid,body=json.dumps(nfprofile))
        if con.status == 200:
            print("Connection Success")
        else:
            print(con.status)
            print(con.headers)

        con.close()
        response = await make_response(jsonify(nfprofile),200,{'Content-Type': 'application/json'})
        return response


@app.route('/nrfclient/suspend/<instanceid>',methods=['PUT'])
class Suspend(Resource):
    async def put(self,instanceid):
        response="suspend instance "+instanceid+"\n"
        print(response)
        nfprofile = await request.get_json(force=True)
        print(nfprofile)
        con = http.request('PUT','https://'+nrfaddress[0]["ip"]+":"+ str(nrfaddress[0]["port"])+'/nnrf-nfm/v1/nf-instances/'+instanceid,body=json.dumps(nfprofile))
        if con.status == 200:
            print("Connection Success")
        else:
            print(con.status)
            print(con.headers)
        con.close()
        response = await make_response(jsonify(nfprofile),200,{'Content-Type': 'application/json'})
        return response


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=443,
        certfile='servercert1.pem',
        keyfile='serverkey1.pem',
    )
