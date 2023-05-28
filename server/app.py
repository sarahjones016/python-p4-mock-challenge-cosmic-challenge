#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Planet, Scientist, Mission

from werkzeug.exceptions import NotFound, BadRequest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Scientists(Resource):
    def get(self):
        # scientists_dict = [scientist.to_dict(rules=('-missions', '-planets')) for scientist in Scientist.query.all()]
        scientists_dict = []
        for scientist in Scientist.query.all():
            scientists_dict.append(scientist.to_dict(rules=('-missions', '-planets')))
        
        response = make_response(
            scientists_dict,
            200,
        )

        return response
    
    def post(self):
        new_scientist = Scientist(
            name=request.json['name'],
            field_of_study=request.json['field_of_study'],
            avatar=request.json['avatar'],
        )

        db.session.add(new_scientist)
        db.session.commit()

        new_scientist_dict = new_scientist.to_dict()

        response = make_response(
            new_scientist_dict,
            201
        )

        if not response:
            raise BadRequest
        else:
            return response
    
api.add_resource(Scientists, '/scientists')

class ScientistsById(Resource):
    def get(self, id):
        
        scientist = Scientist.query.filter_by(id = id).first()

        if not scientist:
            raise NotFound
        
        scientist_dict = scientist.to_dict()

        response = make_response(
            scientist_dict,
            200,
        )

        return response
    
    def patch(self, id):
        scientist = Scientist.query.filter_by(id = id).first()

        if not scientist:
            raise NotFound

        for attr in request.json:
            setattr(scientist, attr, request.json[attr])

        db.session.add(scientist)
        db.session.commit()

        scientist_dict = scientist.to_dict()

        response = make_response(
            scientist_dict, 
            200
        )

        if not response:
            raise BadRequest
        else:
            return response
    
    def delete(self, id):

        scientist = Scientist.query.filter_by(id = id).first()
        # Delete missions associated with scientists?

        if not scientist:
            raise NotFound

        db.session.delete(scientist)
        db.session.commit()

        response = make_response(
            "",
            204
        )

        return response
    
api.add_resource(ScientistsById, '/scientists/<int:id>')

class Planets(Resource):
    def get(self):
        planets_dict = [planet.to_dict(rules=('-missions', '-scientists')) for planet in Planet.query.all()]

        response = make_response(
            planets_dict,
            200
        )

        return response

api.add_resource(Planets, '/planets')

class Missions(Resource):
    def get(self):
        missions_dict = [mission.to_dict() for mission in Mission.query.all()]

        response = make_response(
            missions_dict,
            200
        )

        return response

    def post(self):
        new_mission = Mission(
            name=request.json['name'],
            scientist_id=request.json['scientist_id'],
            planet_id=request.json['planet_id']
        )

        db.session.add(new_mission)
        db.session.commit()

        new_mission_dict = new_mission.to_dict(rules=('-scientists',))

        response = make_response(
            new_mission_dict,
            201
        )

        if not response:
            raise BadRequest
        else:
            return response

api.add_resource(Missions, '/missions')

@app.errorhandler(NotFound)
def resource_not_found(e):
    return {"error": "404: Scientist not found"}, 404

@app.errorhandler(BadRequest)
def bad_request(e):
    return {"error": "400: Validation error"}, 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
