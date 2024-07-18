from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():

    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.all()]
        response = make_response(
            messages,
            200,
            {"Content-Type": "application/json"}
        )
        return response

    elif request.method == 'POST':
        data = request.get_json()
        body = data.get("body")
        username = data.get("username")
        created_at = data.get("created_at")
        updated_at = data.get("updated_at")
        new_message = Message(body=body, username=username, created_at=created_at, updated_at=updated_at)
        db.session.add(new_message)
        db.session.commit()
        return new_message.to_dict(), 201

@app.route('/messages/<int:id>', methods=["PATCH","DELETE"], endpoint="message")
def messages_by_id(id):

    if request.method == "PATCH":
        message = Message.query.get(id)
        data = request.get_json()
        for key, value in data.items():
            if hasattr(message, key):
                setattr(message, key, value)
        db.session.add(message)
        db.session.commit()
        return message.to_dict(), 201
    
    elif request.method == "DELETE":
        message = Message.query.get(id)
        db.session.delete(message)
        db.session.commit()

if __name__ == '__main__':
    app.run(port=5555)
