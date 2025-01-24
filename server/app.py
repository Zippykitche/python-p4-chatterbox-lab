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

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_dict = [message.to_dict() for message in messages]

        response = make_response(
            messages_dict,
            200
        )
        return response

    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data.get("body"),
            username=data.get("username")
        )

        db.session.add(new_message)
        db.session.commit()

        response = make_response(
            new_message.to_dict(),
            201
        )

        return response

@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)
    if not message:
        return {"error": "Message not found"}, 404

    if request.method == 'PATCH':
        data = request.get_json()
        body = data.get('body')
        if body:
            message.body = body
            db.session.commit()
            return message.to_dict(), 200
        else:
            return {"error": "Body is required"}, 400

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        return {"message": "Message deleted successfully"}, 200
    

if __name__ == '__main__':
    app.run(port=5555)
