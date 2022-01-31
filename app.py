from logging import debug
from flask import Flask, request
from flask_restful import Api, Resource, original_flask_make_response as make_response
from flask_socketio import SocketIO, Namespace, disconnect, emit
import base64


app = Flask(__name__)
app.config['SECRET_KEY'] = '^&iuhnbTY^78ouijbvty5^&*IUbgyft6&8'
api = Api(app)
socketio = SocketIO(app)

users = [
    {'username': 'Harry', 'password': '123456'},
    {'username': 'Ron', 'password': 'qwerty'},
    {'username': 'Hermione', 'password': 'asdfgh'}
]
tokenized = ["Bearer "+ base64.b64encode(":".join(i.values()).encode()).decode() for i in users]

class Login(Resource):
    
    def get(self):
        print(request.get_json(force=True))
        if (creds := request.get_json(force=True)) in users:
            resp = make_response({"status": "ok"}, 200)
            resp.headers['authorization'] = "Bearer "+ base64.b64encode(":".join(creds.values()).encode()).decode()
            return resp
        else:
            resp = make_response({"status": "error"}, 401)
            return resp


class Chatroom(Namespace):
    
    def on_connect(self):
        if request.headers.get('authorization') not in tokenized:
            emit('connection_error', {'error': 'unauthorized'})
            disconnect()
            return 401
        else:
            print('sucess')

    def on_disconnect(self):
        pass

    def on_send(self, data):
        print(data)
        emit('recv', data)

socketio.on_namespace(Chatroom('/chat'))
api.add_resource(Login, '/login')

if __name__ == '__main__':
    socketio.run(app, port=5000, host='0.0.0.0')
