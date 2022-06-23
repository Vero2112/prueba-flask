"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Task
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# todos = [
#     { "text": "My first task", "done": False }
# ]

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate_sitemap con todos los endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
    # return "Hola!"


@app.route('/task', methods=['GET'])
def get_task():
    # json_text = jsonify(todos) learnpack devuelve asi las task, no mapea
    # no puedo retornarla directamente, necesito serializarla, hay que transoformala en json. necesito llamar a la funcion list 
    # y se mapea. En vez de utilizar una función flecha equiv función lambda y va a llamar al serializador y me va
    # a retornar el serializador
# esta Task es line 23 models?
    tasks = Task.query.all()
    all_tasks = list(map(lambda task: task.serialize(), tasks))
    # print (tasks)
    # print("hola")
    # print(all_tasks)
    return jsonify(all_tasks)
    # return json_text

@app.route('/task', methods=['POST'])
def create_task():
    # request_body = request.data que significa?
# We already used request.json for that, since we know that the request will be in format application/json. If that is not known, you may want to use request.get_json(force=True) to ignore the content type and treat it like json.
    body = request.get_json()
    print(body)
# body es un diccionario equivalente a un objeto en JS, text es la key
    task = Task(text=body["text"], done= False)
# Una vez instanciada la clase, agrego objeto a mi base de datos
    db.session.add(task)
# confirmamos añadir tarea a mi base de datos, pero no la puedo retornar directamente, para eso necesito serializar
    db.session.commit()
# coge un objeto, tipo task y me lo transforma en un diccionario
# models line 33-37, pq no le ponemos el parametro self?
    return jsonify(task.serialize())

@app.route('/task/<int:task_id>', methods=['PUT'])
def refresh_task(task_id):
    task = Task.query.get(task_id)
    # print("hola")
    # print(task)
    # print(body)
    if task is None:
        raise APIException("Tarea no encontrada", 404)
    body = request.get_json()
    if not ("done" in body):
        raise APIException("Tarea no encontrada", 404)
    task.done = body["done"]
    db.session.commit()
    return jsonify(task.serialize())

@app.route('/task/<int:task_id>', methods=['GET'])
def get_refresh_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        raise APIException("Tarea no encontrada", 404)
    return jsonify(task.serialize())

@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        raise APIException("Tarea no encontrada", 404)
    db.session.delete(task)
    db.session.commit()
    return jsonify(task.serialize())

@app.route('/user', methods=['GET'])
def get_user():
    # response_body = {"msg": "Hello, this is your GET/user response"}
    # return jsonify(response_body), 200
    users = User.query.all()
    all_users = list(map(lambda user: user.serialize(), users))
# todos = db.session.query(Todo)
# list_todo = []
# for todo in todos:
# list_todo.append(todo.serialize())
# return list_todo

    return jsonify(all_users), 200

@app.route('/user', methods=['POST'])
def create_user():
   
    body = request.get_json()
    print(body)
    user = User(email=body["email"], is_active=True, password="******")
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

