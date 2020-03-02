from flask import Flask
from flask import jsonify


user1 = [ {'Name': 'Customer No 1'},
          {'ID' : 'CU77662266'}
        ]

api = Flask(__name__)

@api.route("/user1", methods=['GET'])
def user1info():
  return jsonify({'userinfo' : user1})