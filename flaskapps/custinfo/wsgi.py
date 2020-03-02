from flask import Flask
from flask import jsonify


user1 = [ {'Name': 'Customer No 1'},
          {'ID' : 'CU77662266'}
        ]

application = Flask(__name__)

@application.route("/user1", methods=['GET'])
def user1info():
  return jsonify({'userinfo' : user1})

if __name__ == "__main__":
  application.run()
