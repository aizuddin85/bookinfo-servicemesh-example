from flask import Flask
from flask import jsonify


user1bill = [ {'Due Date': '25th July 2020'},
          {'Amount' : 'USD 120.25'}
        ]

application = Flask(__name__)


@application.route("/")
def home():
  return "Im serving!"

@application.route("/user1", methods=['GET'])
def user1info():
  return jsonify({'userbill' : user1bill})

if __name__ == "__main__":
  application.run()


