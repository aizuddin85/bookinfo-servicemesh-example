import os
from flask import Flask
from flask import request
import requests
import json

servicesDomain = "" if (os.environ.get("SERVICES_DOMAIN") is None) else "." + os.environ.get("SERVICES_DOMAIN")
custinfoservingport = "" if (os.environ.get("CUSTSERVING_PORT") is None) else  os.environ.get("CUSTSERVING_PORT")
custinfoServiceName = "custinfo" if (os.environ.get("CUSTINFO_HOSTNAME") is None) else os.environ.get("CUSTINFO_HOSTNAME")
billinfoservingport = "" if (os.environ.get("BILLSERVING_PORT") is None) else  os.environ.get("BILLSERVING_PORT")
billinfoServiceName = 'billinfo' if (os.environ.get("BILL_HOSTNAME") is None) else os.environ.get("BILL_HOSTNAME")

application = Flask(__name__)


@application.route("/")
def usage():
  clientstr = request.headers.get('host')
  return "Usage: http(s)://{0}/user1".format(clientstr)
  
@application.route("/user1", methods=['GET'])
def user1():

    user1custinfo = requests.get('http://{0}{1}:{2}/user1'.format(custinfoServiceName, servicesDomain, custinfoservingport))
    user1billinfo = requests.get('http://{0}{1}:{2}/user1'.format(billinfoServiceName, servicesDomain, billinfoservingport))
    user1custinforesp = json.loads(user1custinfo.content)
    user1billinforesp = json.loads(user1billinfo.content)
    user1info = user1custinforesp['userinfo'] +  user1billinforesp['userbill']

    return str(user1info)

if __name__ == "__main__":
 application.run()    
