import requests
import json
import time
import base64
import os

def mindalle(prompt,AutoCall=True):
	'''Takes Prompt, AutoCall calls the Final Function defaults to True, if False Returns HASH of the Request else Returns Image Filepath'''

	reqUrl = "https://hf.space/embed/kuprel/min-dalle/api/queue/push/"
	headersList = {
	"authority": "hf.space",
	"accept": "*/*",
	"accept-language": "en-US,en;q=0.9",
	"cache-control": "no-cache",
	"content-type": "application/json",
	"dnt": "1",
	"origin": "https://hf.space",
	"pragma": "no-cache",
	"referer": "https://hf.space/embed/kuprel/min-dalle/+?__theme=light",
	"sec-ch-ua-mobile": "?0",
	"sec-ch-ua-platform": "Linux",
	"sec-fetch-dest": "empty",
	"sec-fetch-mode": "cors",
	"sec-fetch-site": "same-origin",
	"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" 
				}

	payload = json.dumps({ "fn_index": 1,
							"data": [ prompt,3,"false","false",1,"16","128" ],
							"action": "predict",
							"session_hash": "nothing" 
						})
	response = requests.request("POST", reqUrl, data=payload,  headers=headersList).json()

	hash = response["hash"]
	queue_position = str(response["queue_position"])
	
	#print("Hash : " + hash)
	#print("Queue Postion : " + queue_position)
	if AutoCall:
		filepath = mindallestatus(hash,prompt)
		return filepath
	else:
		return hash

def mindallestatus(hash,prompt="min-dalle"):
	'''Takes Hash and Optional Prompt, Returns Image Filepath. Don't Call this Fuction in Directly, Call 'mindalle' which in turns calls this Function'''

	reqUrl = "https://hf.space/embed/kuprel/min-dalle/api/queue/status/"
	headersList = {
	"authority": "hf.space",
	"accept": "*/*",
	"accept-language": "en-US,en;q=0.9",
	"cache-control": "no-cache",
	"content-type": "application/json",
	"dnt": "1",
	"origin": "https://hf.space",
	"pragma": "no-cache",
	"referer": "https://hf.space/embed/kuprel/min-dalle/+?__theme=light",
	"sec-ch-ua-mobile": "?0",
	"sec-ch-ua-platform": "Linux",
	"sec-fetch-dest": "empty",
	"sec-fetch-mode": "cors",
	"sec-fetch-site": "same-origin",
	"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" 
					}
	
	payload = json.dumps({ "hash": hash })
	response = requests.request("POST", reqUrl, data=payload,  headers=headersList).json()

	status = response["status"]
	print("Status : " + status)

	while status != "COMPLETE":

		if status == "QUEUED":
			queue_position = str(response["data"])
			print("Queue Position : " + queue_position)

		if status == "PENDING":
			print("Your job is processing")

		time.sleep(20)

		response = requests.request("POST", reqUrl, data=payload,  headers=headersList).json()
		status = response["status"]
		#print("Status : " + status)

	
	data = response["data"]["data"][0].split(",")[1]
	image = base64.b64decode(data)
	with open(f"{prompt}.jpeg","wb") as file:
		file.write(image)

	return f"{prompt}.jpeg"

def deoldifyurl(url):
	'''Takes Image URL and Returns Deoldified Image URL'''

	reqUrl = "https://hf.space/embed/paochoa/DeOldification/api/predict"
	headersList = {
	"Accept": "*/*",
	"User-Agent": "Thunder Client (https://www.thunderclient.com)",
	"Content-Type": "application/json" 
				  }

	payload = json.dumps({ "data": [ url ] })
	response = requests.request("POST", reqUrl, data=payload,  headers=headersList).json()

	link = response["data"][0]
	return link


def deoldify(file,fileto="colored.jpeg"):
	'''Takes Source Image Filepath and Optional Destination Filepath, Returns Deoldified Image Filepath'''

	#reqUrl = "https://hf.space/embed/geraltofrivia/deoldify_videos/api/predict"
	#reqUrl = "https://hf.space/embed/ecarbo/deoldify-demo/api/predict/"
	reqUrl = "https://hf.space/embed/PaddlePaddle/deoldify/api/predict/"
	
	headersList = {
	"Accept": "*/*",
	"User-Agent": "Thunder Client (https://www.thunderclient.com)",
	"Content-Type": "application/json" 
				  }

	with open(file,"rb") as byte:
		rdata = base64.b64encode(byte.read()).decode('utf-8')
	rdata = "data:image/jpeg;base64," + rdata

	payload = json.dumps({ "data": [rdata] })
	response = requests.request("POST", reqUrl, data=payload,  headers=headersList).json()

	data = response["data"][0].split(",")[1]
	image = base64.b64decode(data)
	with open(fileto,"wb") as file:
		file.write(image)

	return fileto

def dallemini(prompt):
	'''Takes Prompt. Creates a Folder in that name and Returns List of Filepaths'''

	reqUrl = "https://backend.craiyon.com/generate"
	headersList = {
		"authority": "backend.craiyon.com", 
		"accept": "application/json", 
		"accept-language": "en-US,en;q=0.9", 
		"cache-control": "no-cache", 
		"content-type": "application/json", 
		"dnt": "1", "origin": "https://www.craiyon.com", 
		"pragma": "no-cache", "sec-ch-ua-mobile": "?0", 
		"sec-ch-ua-platform": "Linux", 
		"sec-fetch-dest": "empty", 
		"sec-fetch-mode": "cors", 
		"sec-fetch-site": "same-site", 
		"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
				 }

	payload = json.dumps({"prompt": prompt})
	response = requests.request("POST", reqUrl, data=payload, headers=headersList).json()
	os.mkdir(prompt)

	images = []
	i = 1
	for ele in response["images"]:
		image = base64.b64decode(ele.replace('\\n',''))
		with open(f"{prompt}/{i}.jpeg","wb") as file:
			file.write(image)
		images.append(f"{prompt}/{i}.jpeg")
		i = i + 1
		
	return images


