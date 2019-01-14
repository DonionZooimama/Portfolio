from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from patient_processing import *
import werkzeug

app = Flask(__name__)
api = Api(app)


class UpdatePatient(Resource):
    def get(self):
        print (request.args)
        name = request.args.get('name')
        age = request.args.get('age')
        bloodtype = request.args.get('blood_type')
        medications = request.args.get('medications')
        allergies = request.args.get('allergies')
        ID = request.args.get('ID')

        return UpdatePatientData(str(ID), str(name), str(age), str(bloodtype), str(medications), str(allergies))


class NewPatient(Resource):
    def post(self):
        first = request.args.get('first_name')
        last = request.args.get('last_name')
        bloodtype = request.args.get('blood_type')
        allergies = request.args.get('allergies')
        return NewPatientData(first, last, bloodtype, allergies)


class PatientInfo(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        my_file = args['file']
        my_file.save("temp.jpg")
        rv = GetPatientData()
        print rv
        return rv
        

class Hello(Resource):
    def get(self):
        return "Hello"


api.add_resource(UpdatePatient, '/update')
api.add_resource(NewPatient, '/new')
api.add_resource(PatientInfo, '/info')
api.add_resource(Hello, '/')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
