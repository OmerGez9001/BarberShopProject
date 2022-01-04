from flask import Flask, render_template, request
import requests
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


#creating app, configuring app and creating db
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#@jsf.use(app)
#class App():
  #def __init__(self):
    #self.print("welcome to the barber shop!")
  

class ClientModel(db.Model):
  Booked = db.Column(db.String(5), primary_key=True)
  Name = db.Column(db.String(30), nullable=False)
  Phone = db.Column(db.String(10), nullable=False)

db.create_all()

#parser for getting required names and phones in an organized way
db_put_args = reqparse.RequestParser()
db_put_args.add_argument("Name", type=str, help="Name of the client", required=True)
db_put_args.add_argument("Phone", type=str, help="Phone of the client", required=True)


#the format that will be returned when returning a model object.
resource_fields = {
    'Booked': fields.String, 
    'Name': fields.String,
    'Phone': fields.String
}

#list of available times
times = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]

#main resource
class DataBase(Resource):
    
  @marshal_with(resource_fields)
  def get(self, id):
    time = times[id]
    result = ClientModel.query.filter_by(Booked=time).first()
    if not result:
      abort(404, message="Could not find client in database")
        
    all_result = ClientModel.query.filter_by(Phone=result.Phone).all()
    return all_result, 200
    
  @marshal_with(resource_fields)
  def put(self, id):
    time = times[id]
    result = ClientModel.query.filter_by(Booked=time).first()
    if result:
        abort(409, message="Client booked...")
    
    args = db_put_args.parse_args()
    client = ClientModel(Booked=time, Name=args["Name"], Phone=args["Phone"])
    db.session.add(client)
    db.session.commit()   
    return client, 201
        

api.add_resource(DataBase, "/Clients/<int:id>")        

@app.route('/', methods=["POST", "GET"])
def app_start():
  base = "http://localhost:5000/"

  if request.method == "POST":
    response = requests.put(base + "Clients/" + str(request.form["tm"]), {"Name": request.form["nm"], "Phone": request.form["ph"]})
    if response == 201:
      print(response.json())
    elif response == 409:
      print(response.content)
    return render_template("start.html")
  return render_template("start.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')