from flask import Flask
import sqlite3
import flask
import os.path
import Image
import io
import uuid
import base64
import tensorflow
from flask import jsonify
import json
from math import sin, cos, sqrt, atan2, radians
from geopy.distance import vincenty

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")


app = Flask(__name__)

DATABASE = '/path/to/database.db'
@app.route('/userinfo',methods=["POST"])
def uploadUserInfo():
    #userid = flask.request.values.get('userid')
    clanid=flask.request.values.get('clanid')
    #level=flask.request.values.get('level')
    pl=flask.request.values
    print("ggggg")
    print(clanid)

    enterUserInfo(clanid)
    with sqlite3.connect(db_path) as db:
        cursor=db.execute("SELECT userid FROM UserInfo ORDER BY userid DESC LIMIT 1")
    for row in cursor:
        print(row[0])

    #return row[0]
    return str(row[0])


@app.route('/locationinfo',methods=["POST"])
def uploadLocationInfo():


    lat = flask.request.values.get('lat')
    print(lat)
    lon = flask.request.values.get('lon')
    print(lon)
    clanid = flask.request.values.get('clanid')

    imagear = flask.request.files.get('image','')

   # image = Image.open(io.BytesIO(imagear))

    savepath=uuid.uuid4().hex+".png"
    imagear.save(savepath)
    if(checkLocation(lat,lon)):
        enterLocationInfo(lat,lon,clanid,savepath)
        return "true"
    return "false"
@app.route('/getdetails',methods=["POST"])
def getDetails():
    print("oo")
    data={}
    with sqlite3.connect(db_path) as db:
        cursor=db.execute("SELECT latitude,clanid,longitude FROM Location")
        for row in cursor:
            lat=row[0]
            lon=row[2]
            clan=row[1]
            data[(str(lat)+','+str(lon))]=str(clan)
    print(data)
    return json.dumps(data)

    #print(cur)
def checkLocation(mylat,mylon):
    with sqlite3.connect(db_path) as db:
        cursor=db.execute("SELECT latitude,longitude FROM Location")
        for row in cursor:
            lat=row[0]
            lon=row[1]

            if(getDistanceFromLatLonInKm(mylat,mylon,lat,lon)<10):
                print('false')
                return False
        print('true')
        return True

def getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) :
        print('vfdfvdfvv')
        print(lat1)
        print(lon1)
        print(lat2)
        print(lon2)

        t1=(float(lat1),float(lon1))
        t2 = (float(lat2), float(lon2))
        p=vincenty(t1,t2).meters
        return p

def enterUserInfo(clanid):
    print('h')

    with sqlite3.connect(db_path) as db:
        db.execute("INSERT INTO UserInfo(clanid) VALUES (?)", (clanid,))
        print('entered')


def enterLocationInfo(lat,lon,clanid,bphoto):
    print('h')
    with sqlite3.connect(db_path) as db:
        db.execute("INSERT INTO Location(latitude,longitude,clanid,bphoto) VALUES (?,?,?,?)", (lat,lon,clanid,bphoto))


if __name__ == '__main__':
    print('k')
    getDetails()
    app.run('10.0.3.55',5005)
    print('g')


