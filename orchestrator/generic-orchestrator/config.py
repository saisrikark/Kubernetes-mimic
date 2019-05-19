import xml.etree.ElementTree as ET
parser = argparse.ArgumentParser()
parser.add_argument("--file",help="config file")


args = parser.parse_args()

if(args.file):
	file_name = args.file
else:
	file_name = "configuration.xml"
try:
	root = ET.parse(file_name).getroot()
except Exception as e:
	print("File configuration doesnot exist.")

act_container = root.find('act_container')
start_port = act_container.find('start_port').text
act_vm_ip_address = act_container.find('ip_address').text
orchestrator_port = root.find('orchestrator/port').text

if __name__ == '__main__':
	orchestrator = Orchestrator(start_port,act_vm_ip_address,orchestrator)
	orchestrator.init_container()
	orchestrator.get_containers()
	orchestrator.run_webserver()