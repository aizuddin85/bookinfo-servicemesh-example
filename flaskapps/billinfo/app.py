from flask import Flask
from flask import jsonify


user1bill = [ {'Due Date': '25th July 2020'},
          {'Amount' : 'USD 120.25'}
        ]

api = Flask(__name__)

@api.route("/user1", methods=['GET'])
def user1info():
  return jsonify({'userbill' : user1bill})