from flask import Flask, request
import requests
import json
import ncclient
from ncclient import manager
import xml.dom.minidom

############## Bot details ##############

bot_name = 'incubator20@webex.bot'
#roomId = 'Y2lzY29zcGFyazovL3VzL1JPT00vMWM4ZWRjMjQtMzBmYi0zZTFjLTk3OTgtODU5ZGVlMTYyNThl'
token = 'YjY3YThkNDEtNWQzMS00ZjczLTgwMmEtZDgxZTY5Nzk0ZjUwOTgzMjZmYWUtZTQ1_PF84_consumer'
header = {"content-type": "application/json; charset=utf-8", 
		  "authorization": "Bearer " + token}


############## Nexus connectivity ##############

node = 'sbx-nxos-mgmt.cisco.com'

def connect(node):
    try:
    	device_connection = ncclient.manager.connect(host = node, port = 8181, username = 'admin', password = 'Admin_1234!', hostkey_verify = False, allow_agent = False, look_for_keys = False, device_params={'name':'nexus'})
    	return device_connection
    except:
        print("Unable to connect " + node)

def getHostname(node):
    device_connection = connect(node)
    hostname = """
               <show xmlns="http://www.cisco.com/nxos:1.0">
                   <hostname>
                   </hostname>
               </show>
               """
    netconf_output = device_connection.get(('subtree', hostname))
    xml_doc = xml.dom.minidom.parseString(netconf_output.xml)
    hostname = xml_doc.getElementsByTagName("mod:hostname")
    return "Hostname: "+str(hostname[0].firstChild.nodeValue)


############## Flask Application ##############

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def sendMessage():
	webhook = request.json
	url = 'https://api.ciscospark.com/v1/messages'
	msg = {"roomId": webhook["data"]["roomId"]}
	sender = webhook["data"]["personEmail"]
	message = getMessage()
	if (sender != bot_name):
		if (message == "help"):
			msg["markdown"] = "Welcome to **CSRv1000 Spark Bot**!  \n List of available commands: \n- show hostname \n- help"
		elif (message == "show hostname"):
			msg["markdown"] = getHostname(node)
		else:
			msg["markdown"] = "Sorry! I didn't recognize that command. Type **help** to see the list of available commands."
		requests.post(url,data=json.dumps(msg), headers=header, verify=True)

def getMessage():
	webhook = request.json
	url = 'https://api.ciscospark.com/v1/messages/' + webhook["data"]["id"]
	get_msgs = requests.get(url, headers=header, verify=True)
	message = get_msgs.json()['text']
	return message

app.run(debug = True)