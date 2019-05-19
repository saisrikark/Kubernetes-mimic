from flask import Flask
from flask import Blueprint, request, jsonify, Response, abort
import requests
import os
import threading
import time
import sys
app = Flask(__name__)

which_container = 0
lock = threading.Lock()
containerList = {}
unhealthy_containers = {}

first_request = 0

no_of_requests = 0

def scaledown(diff):
    pop_list = list(containerList.keys())
    pop_list.sort()
    pop_list = pop_list[-diff:]
    for port in pop_list:   
        container_id = containerList.pop(port)
        # Killing that container
        os.popen("sudo docker kill "+container_id)
        print("Killed container %s ha ha ha", container_id)

def scaleup(diff):
    pop_list = list(containerList.keys())
    print("Wasuppppppppppppppppppppppppppppppppppp:")
    print(pop_list)
    # I'm sorting and taking the maximum port number
    # next port number will be the one after that
    pop_list.sort()

    next_port = int(max(pop_list))
    for i in range(diff):
        next_port += 1
        # please fill this below statement yourself
        # Now to start the new container,
        # and fetch the new container_id and store in containerList
        temp_str = "sudo docker run -dit -v Database:/acts -p "+ str(next_port) +":80"+" acts:latest"
        new_container_id = os.popen(temp_str).readlines()[0][:12]
        print("Next_posrt ",next_port)
        containerList[str(next_port)] = new_container_id
        print("New container ", new_container_id)
        
def autoscaling():
    print("I'm auto scaling after 2 min")
    global no_of_requests
    print("No. of requests: ",str(no_of_requests))
    no_of_containers = (no_of_requests // 20) + 1
    # docker container ls -> to show the running containers
    # Finding the number of containers
    details = os.popen("sudo docker ps").readlines()
    curr_no_of_containers = len(details) - 1
    print(no_of_containers)
    print("curr_no_of_containers:",curr_no_of_containers)
    diff = curr_no_of_containers - no_of_containers
    print("Diff:",str(diff))
    if(diff == 0):
        print("Just perfect")
    elif(diff > 0):
        print("We have tooooo many !!!")
        scaledown(diff)
    else:
        print("We have tooooo less !!!")
        scaleup(-diff)

    threading.Timer(120, autoscaling).start()   
    no_of_requests = 0



def get_containers():
	container_cmd = os.popen("sudo docker ps")
	container_details = container_cmd.readlines()
	for each in container_details[1:]:
		#print(each)
		each = each.split(" ")
		each = [x for x in each if x]
		container_id = each[0]
		container_port = each[-2].split(":")[1].split("->")[0]
		containerList[container_port] = container_id
	#print(containerList)
	#print(conatiner_details)

def get_crashed_containers():
    crashed_ports = {}
    for port in list(containerList.keys()):
    	status_code = 0
    	try:
    		response = requests.get('http://127.0.0.1:'+port+'/api/v1/_health')
    		status_code = response.status_code
    	except Exception as e:
            #response = requests.get('http://127.0.0.1:'+port+'/api/v1/_health')
    		status_code = 500
    	if(status_code == 500):
        	crashed_ports[port] = containerList[port]
    return crashed_ports

def check_container_health(container_dict):
    #global lock
    t_id = threading.current_thread().ident
    unhealthy_containers = get_crashed_containers()
    '''
    if not unhealthy_containers:
    '''
    print(unhealthy_containers,file=sys.stdout)
    
    for port in list(unhealthy_containers.keys()):
        container_id = unhealthy_containers[port]
        stop_container = os.popen("sudo docker kill "+container_id)
        print(str(t_id),"is Restarting at port "+port)
        #sudo docker run -dit -v Database:/acts -p 8000:80 acts
        temp_str = "sudo docker run -dit -v Database:/acts -p "+ port +":80"+" acts:latest"
        new_container_id = os.popen(temp_str).readlines()[0][:12]
        #print(threading.current_thread().ident)
        print(str(t_id)," has made New container ", new_container_id)
        unhealthy_containers.pop(port)
        get_containers()
    threading.Timer(1, check_container_health,[containerList]).start()   

@app.route('/api/v1/categories',methods=['GET','POST'])
def categories():
	get_containers()
	global which_container
	global first_request
	global no_of_requests
	if(first_request == 0):
		print("Helllooo:",first_request)
		first_request = 1
		t2 = threading.Thread(target=autoscaling)
		t2.start()
	
	no_of_requests = no_of_requests+1
	print("Why Bro:",str(no_of_requests))
	
	if request.method == 'GET':
		if(len(containerList) ==1):
			response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
			while(response.status_code !=200 ):
				which_container = (which_container+1)%len(containerList)
				response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
			print("Using:Port {} and Container ID {}".format(list(containerList.keys())[0],containerList[list(containerList.keys())[0]]))
			return_value = requests.get('http://127.0.0.1:'+list(containerList.keys())[0]+'/api/v1/categories')
			#print(return_value,type(return_value))
			return (return_value.text, return_value.status_code, return_value.headers.items())
		else:
			response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
			while(response.status_code !=200 ):
				which_container = (which_container+1)%len(containerList)
				response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
			print("Using:Port {} and Container ID {}".format(list(containerList.keys())[which_container],containerList[list(containerList.keys())[which_container]]))
			return_value = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/categories')
			which_container = (which_container+1)%len(containerList)
			#print(return_value,type(return_value))
			return (return_value.text, return_value.status_code, return_value.headers.items())
	if request.method == 'POST':
		response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
		while(response.status_code !=200 ):
			which_container = (which_container+1)%len(containerList)
			response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
		print("Using:Port {} and Container ID {}".format(list(containerList.keys())[which_container],containerList[list(containerList.keys())[which_container]]))
		json_data = request.get_json(force=True)
		print(json_data)
		response = requests.post('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/categories',json = json_data)
		which_container = (which_container+1)%len(containerList)
		return (response.text, response.status_code, response.headers.items())



@app.route('/api/v1/categories/<categoryName>',methods=['DELETE'])
def deleteCategory(categoryName):
	get_containers()
	global which_container
	response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
	while(response.status_code !=200 ):
		which_container = (which_container+1)%len(containerList)
		response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
	print("Using:Port {} and Container ID {}".format(list(containerList.keys())[which_container],containerList[list(containerList.keys())[which_container]]))
	response = requests.delete('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/categories/'+categoryName)
	which_container = (which_container+1)%len(containerList)
	return (response.text, response.status_code, response.headers.items())

@app.route('/api/v1/categories/<categoryName>/acts',methods=['GET'])
def listActs(categoryName):
	get_containers()
	global which_container
	response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
	while(response.status_code !=200 ):
		which_container = (which_container+1)%len(containerList)
		response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
	print("Using:Port {} and Container ID {}".format(list(containerList.keys())[which_container],containerList[list(containerList.keys())[which_container]]))
	response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/categories/'+categoryName+'/acts')
	which_container = (which_container+1)%len(containerList)
	return (response.text, response.status_code, response.headers.items())
@app.route('/api/v1/categories/<categoryName>/acts/size',methods=['GET'])
def getActSize(categoryName):
	get_containers()
	global which_container
	response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
	while(response.status_code !=200 ):
		which_container = (which_container+1)%len(containerList)
		response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
	print("Using:Port {} and Container ID {}".format(list(containerList.keys())[which_container],containerList[list(containerList.keys())[which_container]]))
	response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/categories/'+categoryName+'/acts/size')
	which_container = (which_container+1)%len(containerList)
	return (response.text, response.status_code, response.headers.items())

@app.route('/api/v1/acts/count',methods=['GET'])
def countActs():
	get_containers()
	global which_container
	response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
	while(response.status_code !=200 ):
		which_container = (which_container+1)%len(containerList)
		response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
	print("Using:Port {} and Container ID {}".format(list(containerList.keys())[which_container],containerList[list(containerList.keys())[which_container]]))
	response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/acts/counts')
	which_container = (which_container+1)%len(containerList)
	return (response.text, response.status_code, response.headers.items())

@app.route('/api/v1/acts/upvote',methods=['POST'])
def upvote():
	response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
	while(response.status_code !=200 ):
		which_container = (which_container+1)%len(containerList)
		response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
	print("Using:Port {} and Container ID {}".format(list(containerList.keys())[which_container],containerList[list(containerList.keys())[which_container]]))
	json_data = request.get_json(force=True)
	print(json_data)
	response = requests.post('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/acts/upvote',json = json_data)
	which_container = (which_container+1)%len(containerList)
	return (response.text, response.status_code, response.headers.items())


@app.route('/api/v1/acts/<actID>',methods=['DELETE'])
def removeAct(actID):
	get_containers()
	global which_container
	response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
	while(response.status_code !=200 ):
		which_container = (which_container+1)%len(containerList)
		response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
	print("Using:Port {} and Container ID {}".format(list(containerList.keys())[which_container],containerList[list(containerList.keys())[which_container]]))
	response = requests.delete('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/acts/'+actID)
	which_container = (which_container+1)%len(containerList)
	return (response.text, response.status_code, response.headers.items())
@app.route('/api/v1/acts',methods=['POST'])
def uploadAct():
	response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
	while(response.status_code !=200 ):
		which_container = (which_container+1)%len(containerList)
		response = requests.get('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/_health')
	print("Using:Port {} and Container ID {}".format(list(containerList.keys())[which_container],containerList[list(containerList.keys())[which_container]]))
	json_data = request.get_json(force=True)
	#print(json_data)
	response = requests.post('http://127.0.0.1:'+list(containerList.keys())[which_container]+'/api/v1/acts/upvote',json = json_data)
	which_container = (which_container+1)%len(containerList)
	return (response.text, response.status_code, response.headers.items())


if __name__=="__main__":
    #cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    get_containers()
    #
    print("Making new thread")
    t1 = threading.Thread(target=check_container_health, args=(containerList,))
    t1.start()
   
    print(str(threading.current_thread().ident),"is running")
    #threading.Timer(5, check_container_health,[containerList]).start()	
    app.run(host='0.0.0.0', port=80)
    #t1.join()
    #print("Thread closed")