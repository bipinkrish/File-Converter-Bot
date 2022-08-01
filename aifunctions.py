
##############################################################################################################
# dalle

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


##############################################################################################################
# deolidfy


import requests
import json
import time
import base64
import os


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


##############################################################################################################
# negative to positive


import cv2
import copy


def reverse_rgb(image):
    return 255 - image

def equalize_adaptive_histogram(image, clipLimit=2.0, tileGridSize=8):
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(tileGridSize, tileGridSize))
    equalized = clahe.apply(image)
    return equalized

def on_trackbar():
    global out_image
    
    y = int(1 * (tmp_image.shape[1] / 200))
    x = int(1 * (tmp_image.shape[0] / 200))
    w = int(200 * (tmp_image.shape[0] / 200))
    h = int(200 * (tmp_image.shape[1] / 200))
    rows, cols = tmp_image.shape
    
    M = cv2.getRotationMatrix2D(((cols - 1) / 2.0, (rows - 1) / 2.0), 0, 1)
    output = cv2.warpAffine(tmp_image, M, (cols, rows))
    output = output[x:x + w, y:y + h]
   
    output = reverse_rgb(output) 
    output = equalize_adaptive_histogram(output)
    out_image = copy.deepcopy(output)

def run_for_file(image, output):
    global tmp_image
    tmp_image = copy.deepcopy(image)
    tmp_image = cv2.cvtColor(tmp_image, cv2.COLOR_BGR2GRAY)
    on_trackbar()
    cv2.imwrite(output,out_image)
    
    
def positiver(filepath, output):
    image = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
    run_for_file(image,output)


##############################################################################################################
# image colorizer


import numpy as np
import cv2
import os.path

version = '7 June 2020'

prototxt = r'model/colorization_deploy_v2.prototxt'
model = r'model/colorization_release_v2.caffemodel'
points = r'model/pts_in_hull.npy'
points = os.path.join(os.path.dirname(__file__), points)
prototxt = os.path.join(os.path.dirname(__file__), prototxt)
model = os.path.join(os.path.dirname(__file__), model)
net = cv2.dnn.readNetFromCaffe(prototxt, model)     # load model from disk
pts = np.load(points)

# add the cluster centers as 1x1 convolutions to the model
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

def colorize_image(output, image_filename=None, cv2_frame=None):
   
    image = cv2.imread(image_filename) if image_filename else cv2_frame
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")
    
    cv2.imwrite(output, colorized)


##############################################################################################################