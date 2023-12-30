from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy, model
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS


app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# API
api = Api(app)




class CityModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    temp = db.Column(db.String(100), nullable=False)
    weather = db.Column(db.String(100), nullable=False)
    people = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"City(name={name},temp={temp},weather={weather},people={people})"


# Create tables
with app.app_context():
    db.create_all()

# Request Parser
city_add_args = reqparse.RequestParser()
city_add_args.add_argument("name", type=str, required=True, help="Please provide the city name")
city_add_args.add_argument("temp", type=str, required=True, help="Please provide the temperature")
city_add_args.add_argument("weather", type=str, required=True, help="Please provide the weather condition")
city_add_args.add_argument("people", type=str, required=True, help="Please provide the number of people")

# Request Update
city_update_args = reqparse.RequestParser()
city_update_args.add_argument("name", type=str,  help="Please edit the city name")
city_update_args.add_argument("temp", type=str,  help="Please edit the temperature")
city_update_args.add_argument("weather", type=str,  help="Please edit the weather condition")
city_update_args.add_argument("people", type=str,  help="Please edit the number of people")

# Resource Fields
resource_field = {
    "id": fields.Integer,
    "name": fields.String,
    "temp": fields.String,
    "weather": fields.String,
    "people": fields.String
}

# Validate request
# Validate request
def not_found_city(city_id):
    city = CityModel.query.filter_by(id=city_id).first()
    if not city:
        abort(404, message="City not found")


# Design
class WeatherCity(Resource):

    @marshal_with(resource_field)
    def get(self,city_id):
        result=CityModel.query.filter_by(id=city_id).first()
        if not result:
            abort(404,message="not found request")
        return result

    @marshal_with(resource_field)
    def post(self,city_id):
        result=CityModel.query.filter_by(id=city_id).first()
        if result:
            abort(409,message="this id already saved")
        args=city_add_args.parse_args()
        city=CityModel(id=city_id,name=args["name"],temp=args["temp"],weather=args["weather"],people=args["people"])
        db.session.add(city)
        db.session.commit()
        return city,201
    
    @marshal_with(resource_field)
    def patch(self,city_id):
        args = city_update_args.parse_args()
        result=CityModel.query.filter_by(id=city_id).first()
        if not result:
            abort(404,message="not found request")
        if args["name"]:
            result.name = args["name"]
        if args["temp"]:
            result.temp = args["temp"]
        if args["weather"]:
            result.weather = args["weather"]
        if args["people"]:
            result.people = args["people"]
            
        db.session.commit()
        return result
        
        

#call
api.add_resource(WeatherCity,"/weather/<int:city_id>")

if __name__ == "__main__":
    app.run(debug=True)

