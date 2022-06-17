import os
from flask import Flask, request
import redis
#starting flask
app = Flask(__name__)
#connecting to the database
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
db = redis.Redis(connection_pool=pool)

@app.route('/post', methods=['POST'])
def post():
    request_data = request.get_json()

    message = None

    if request_data:
        if 'message' in request_data:
            message = request_data['message']
    db.publish('messages', message)
    db.rpush('message_list', message)

@app.route('/getall',methods = ['GET'])
def getall():
    message_list = db.lrange('message_list',0,db.llen('message_list'))
    return "\n".join(message_list)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
