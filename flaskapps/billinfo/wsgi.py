from flask import Flask
from flask import jsonify


user1bill = [ {'Due Date': '25th July 2020'},
          {'Amount' : 'USD 120.25'}
        ]

api = Flask(__name__)


@api.route("/")
def home():
  return "Im serving!"

@api.route("/user1", methods=['GET'])
def user1info():
  return jsonify({'userbill' : user1bill})

if __name__ == "__main__":
  api.run()


