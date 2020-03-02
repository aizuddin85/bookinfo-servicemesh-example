from flask import Flask
from flask import jsonify


user1bill = [ {'Due Date': '25th July 2020'},
          {'Amount' : 'USD 120.25'}
        ]

app = Flask(__name__)


@app.route("/")
def home():
  return "Im serving!"

@app.route("/user1", methods=['GET'])
def user1info():
  return jsonify({'userbill' : user1bill})

if __name__ == "__main__":
  app.run()


