from flask import Flask, request, make_response, jsonify, g
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

@app.route('/messages/<int:id>, methods=["PATCH"], endpoint="message')
def messages_by_id(id):
    for attr in request.form:
        setattr(message, attr, message.get(attr))
    
    db.session.add(message)
    db.session.commit()

    message_dict = message.to_dict()

    response = make_response(
        message_dict,
        200
    )

    return response
    
    data = request.get_json
    body = data.get("body")
    message = Message.query.get(id)
    return make_response(g.message.to_dict(), 200)

if __name__ == '__main__':
    app.run(port=5555)
