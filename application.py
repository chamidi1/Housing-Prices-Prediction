from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from random import seed
from random import randint

application = Flask(__name__)
cors = CORS(application)
application.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/housing_prices_prediction_db"
db = SQLAlchemy(application)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['CORS_HEADERS'] = 'Content-Type'


class PricesPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crimeRate = db.Column(db.Integer, unique=False, nullable=False)
    roomsCount = db.Column(db.Integer, unique=False, nullable=False)
    weather = db.Column(db.Integer, unique=False, nullable=False)
    duration = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, crimeRate, roomsCount, weather, duration):
        self.crimeRate = crimeRate
        self.roomsCount = roomsCount
        self.weather = weather
        self.duration = duration


db.create_all()
db.session.commit()


def errorResponse():
    return make_response(jsonify({
        "success": "false",
        "msg": "Something went wrong",
        "status": "500"
    }), 500)


@application.route("/")
def hello_world():
    return "<p>hello world!</p>"


@application.route('/prices-prediction/add', methods=['POST'])
@cross_origin()
def addUser():
    try:
        data = request.form
        pricesPrediction = PricesPrediction(
            crimeRate=data.get('crimeRate'),
            roomsCount=data.get('roomsCount'),
            weather=data.get('weather'),
            duration=data.get('duration'),
        )
        print(pricesPrediction)
        db.session.add(pricesPrediction)
        db.session.commit()

        pre = randint(4800000, 8800000)

        return make_response(jsonify({
            "success": "true",
            "msg": "Prices prediction added successfully!",
            "status": "200",
            "data": pre
        }), 200)
    except:
        return errorResponse()


