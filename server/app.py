from flask import Flask, request, Response

from database import db_session, init_db
from models import Images

app = Flask(__name__)

init_db()


@app.route('/', methods=['POST'])
def receive_image():
    request_data = request.get_json()
    file = request_data['file']
    file_name = request_data['file_name']
    i = Images(file, file_name)
    db_session.add(i)
    db_session.commit()
    images = Images.query.all()
    print(images)
    return Response(status=202)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
