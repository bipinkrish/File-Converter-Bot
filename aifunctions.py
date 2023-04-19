import requests
import json
import time
import base64
import os
import cv2
import copy
import numpy as np
import os.path
import shutil
import speech_recognition as sr 
from pydub import AudioSegment
from pydub.silence import split_on_silence
from gtts import gTTS
from websocket import create_connection


############################################################################################################
# bg remove

def bg_remove(file):

	url = "https://nateraw-background-remover.hf.space/api/predict/"
	splits = file.split("/")[-1]
	name = splits.split(".")[0]
	ext = splits.split(".")[1]

	with open(file, "rb") as byte: rdata = f"data:image/{ext};base64," + base64.b64encode(byte.read()).decode('utf-8')
	payload = json.dumps({"data": [rdata, 140]})

	response = requests.post(url, data=payload).json()
	data = response["data"][0].split(",")[1]
	image = base64.b64decode(data)
	with open(name + "_bg_removed." + ext, "wb") as f: f.write(image)

	return name + "_bg_removed." + ext


############################################################################################################
# riffusin music generator

def riffusion(prompt): 

	while 1:
		try:
			ws = create_connection("wss://fffiloni-spectrogram-to-music.hf.space/queue/join")
			break
		except: pass
		
	ws.recv()
	ws.send('{"session_hash":"'+ "nothing" +'","fn_index":0}')

	while True:
			result =  json.loads(ws.recv())
			if result["msg"] != "estimation": break
		
	ws.send('{"fn_index":0,"data":["' + prompt + '","",null,10],"session_hash":"nothing"}')
	result = ws.recv()
	result =  json.loads(ws.recv())
	ws.close()

	name = "".join( x for x in prompt if (x.isalnum() or x in " "))
	image = base64.b64decode(result["output"]["data"][0].split(",")[1])
	with open(name + ".jpeg","wb") as f: f.write(image)
	music = requests.get("https://fffiloni-spectrogram-to-music.hf.space/file=" + result["output"]["data"][1]["name"])
	with open(name + ".wav","wb") as f: f.write(music.content)

	return name+".wav", name+".jpeg"


############################################################################################################
# bloom para writter

def bloom(para,AutoCall=True):
	headers = {
		'authority': 'huggingface-bloom-demo.hf.space',
		'accept': '*/*',
		'accept-language': 'en-US,en;q=0.9',
		'content-type': 'application/json',
		'dnt': '1',
		'origin': 'https://huggingface-bloom-demo.hf.space',
		'referer': 'https://huggingface-bloom-demo.hf.space/?__theme=light',
		'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-origin',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
	}

	json_data = {
			'fn_index': 2,
			'data': [para,64,'Sample','Sample 1',],
			'action': 'predict',
			'session_hash': 'nothing',
		}

	response = requests.post('https://huggingface-bloom-demo.hf.space/api/queue/push/',headers=headers,json=json_data,).json()
	hash = response["hash"]
	#queue_position = str(response["queue_position"])

	if AutoCall: return bloomstatus(hash, headers)
	else: return hash


def bloomstatus(hash, headers):

	json_data = {'hash': hash,}
	response = requests.post('https://huggingface-bloom-demo.hf.space/api/queue/status/',headers=headers,json=json_data,).json()
	status = response["status"]
	#print("Status : " + status)
	
	while status != "COMPLETE":
		if status == "FAILED": return None
		if status == "QUEUED":
			queue_position = str(response["data"])
			# print("Queue Position : " + queue_position)
		if status == "PENDING":
			pass
			# print("Your job is processing")
		
		time.sleep(5)
		response = requests.post('https://huggingface-bloom-demo.hf.space/api/queue/status/',headers=headers,json=json_data,).json()
		status = response["status"]
		#print("Status : " + status)
	
	return response["data"]["data"][1]


############################################################################################################
# chat with ai

def chatWithAI(msg, hash, rec_count=0):
	response = requests.post("https://tloen-alpaca-lora.hf.space/run/predict", 
			    json={"data": ["",msg,0.1,0.75,40,4,512,]}).json()
	if response["error"] is not None: return response["data"]

	while 1:
		try:
			ws = create_connection("wss://tloen-alpaca-lora.hf.space/queue/join")
			break
		except: pass
	
	ws.recv()
	ws.send('{"fn_index":0,"session_hash":"' + hash +'"}')
	
	while True:
		result =  json.loads(ws.recv())
		if result["msg"] != "estimation": break
	
	ws.send('{"fn_index":0,"data":["","' + msg + '",0.1,0.75,40,4,512],"event_data":null,"session_hash":"' + hash + '"}')
	ws.recv()
	result =  json.loads(ws.recv())
	ws.close()
	
	if not result["success"]: return None
	final = result["output"]["data"][0]
	if final in ["",'<p>.</p>\n',None]:
		if rec_count == 3: return None
		else: return chatWithAI(msg, hash, rec_count+1)
	else: return final

############################################################################################################
# stabilty AI

def stabilityAI(prompt):
	ws = create_connection("wss://stabilityai-stable-diffusion.hf.space/queue/join")
	ws.recv()
	ws.send('{"session_hash":"nothing","fn_index":3}')
	#print("started")

	# waiting for queue
	while True:
		result =  json.loads(ws.recv())
		#print("in Queue")
		if result["msg"] == "queue_full":
			time.sleep(3)
			continue
		if result["msg"] != "estimation": break
	
	#print("processing")
	ws.send('{"fn_index":3,"data":["' + prompt + '","",9],"session_hash":"nothing"}')
	result =  ws.recv()
	print(result)
	result =  json.loads(ws.recv())
	ws.close()

	imgs = result['output']['data'][0]
	final = []
	for i, img in enumerate(imgs):
		image = base64.b64decode(img.split(",")[1])
		with open(f"{i+1}-{prompt}.jpeg","wb") as file:
			file.write(image)
		final.append(f"{i+1}-{prompt}.jpeg")
	return final


############################################################################################################
# point e

import plotly.io as pio
import plotly.graph_objects as go


def pointE(prompt):

	reqUrl = "https://openai-point-e.hf.space/run/predict"
	headersList = {
	"Accept": "*/*",
	"User-Agent": "Thunder Client (https://www.thunderclient.com)",
	"Content-Type": "application/json" 
	}
	payload = json.dumps({"data": [prompt]})
	response = requests.post(reqUrl, data=payload,  headers=headersList).json()

	plot_data = json.loads(response["data"][0]["plot"])
	fig = go.Figure(data=plot_data["data"])
	pio.write_html(fig, f'{prompt}.html')
	return f'{prompt}.html'


############################################################################################################
# whisper

def whisper(file):

	reqUrl = "https://hf.space/embed/Amrrs/openai-whisper-live-transcribe/api/predict"
	headersList = {
		"authority": "hf.space",
		"accept": "*/*",
		"accept-language": "en-US,en;q=0.9",
		"cache-control": "no-cache",
		"content-type": "application/json",
		"dnt": "1",
		"origin": "https://hf.space",
		"pragma": "no-cache",
		"referer": "https://huggingface.co/spaces/Amrrs/openai-whisper-live-transcribe",
		"sec-ch-ua-mobile": "?0",
		"sec-ch-ua-platform": "Linux",
		"sec-fetch-dest": "empty",
		"sec-fetch-mode": "cors",
		"sec-fetch-site": "same-origin",
		"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" 
		}


	with open(file,"rb") as byte:
		rdata = base64.b64encode(byte.read()).decode('utf-8')
	rdata = "data:audio/mp3;base64," + rdata

	payload = json.dumps({ "data": [{
											"name": file.split("/")[-1],
											"data": rdata
									}]
						})
	try: 
		response = requests.request("POST", reqUrl, data=payload, headers=headersList).json()
		data = response["data"][0]
		return data
	except: return None


##############################################################################################################
# dalle


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


#############################################################################################################
# satble diffusion


def stablediff(prompt,AutoCall=True):

	reqUrl = "https://hf.space/embed/Shuang59/Composable-Diffusion/api/queue/push/"
	headersList = {
	"authority": "hf.space",
	"accept": "*/*",
	"accept-language": "en-US,en;q=0.9",
	"cache-control": "no-cache",
	"content-type": "application/json",
	"dnt": "1",
	"origin": "https://hf.space",
	"pragma": "no-cache",
	"referer": "https://hf.space/embed/Shuang59/Composable-Diffusion/+?__theme=light",
	"sec-ch-ua-mobile": "?0",
	"sec-ch-ua-platform": "Linux",
	"sec-fetch-dest": "empty",
	"sec-fetch-mode": "cors",
	"sec-fetch-site": "same-origin",
	"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" 
	}

	payload = json.dumps({ "fn_index": 0, "data": [
													prompt,
													"Stable_Diffusion_1v_4",
													15,
													50
												], "action": "predict", "session_hash": "nothing" })

	response = requests.request("POST", reqUrl, data=payload,  headers=headersList).json()
	hash = response["hash"]

	if AutoCall:
		filepath = stablediffstatus(hash,prompt)
		return filepath
	else:
		return hash


def stablediffstatus(hash,prompt="stable-diff"):

	reqUrl = "https://hf.space/embed/Shuang59/Composable-Diffusion/api/queue/status/"
	headersList = {
	"authority": "hf.space",
	"accept": "*/*",
	"accept-language": "en-US,en;q=0.9",
	"cache-control": "no-cache",
	"content-type": "application/json",
	"dnt": "1",
	"origin": "https://hf.space",
	"pragma": "no-cache",
	"referer": "https://hf.space/embed/Shuang59/Composable-Diffusion/+?__theme=light",
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
			
		time.sleep(10)
		
		response = requests.request("POST", reqUrl, data=payload,  headers=headersList).json()
		status = response["status"]

	data = response["data"]["data"][0]
	if data == None:
		return None
	data = data.split(",")[1]
	image = base64.b64decode(data)
	with open(f"{prompt}.png","wb") as file:
		file.write(image)
	
	return f"{prompt}.png"


##############################################################################################################
# deolidfy


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
# latent diffusion


def latentdiff(prompt):

	reqUrl = "https://hf.space/embed/CompVis/text2img-latent-diffusion/api/predict"
	headersList = {
	"Accept": "*/*",
	"User-Agent": "Thunder Client (https://www.thunderclient.com)",
	"Content-Type": "application/json" 
					}

	payload = json.dumps({ "data": [ prompt, 50, 2147483647, 20 ]})
	response = requests.request("POST", reqUrl, data=payload,  headers=headersList).json()

	data = response["data"][0].split(",")[1]
	image = base64.b64decode(data)
	with open(f"{prompt}.jpg","wb") as file:
		file.write(image)

	return f"{prompt}.jpg"


def latdif(prompt, AutoCall=True):

	reqUrl = "https://hf.space/embed/multimodalart/latentdiffusion/api/queue/push/"
	headersList = {
	"authority": "hf.space",
	"accept": "*/*",
	"accept-language": "en-US,en;q=0.9",
	"cache-control": "no-cache",
	"content-type": "application/json",
	"dnt": "1",
	"origin": "https://hf.space",
	"pragma": "no-cache",
	"referer": "https://hf.space/embed/multimodalart/latentdiffusion/+",
	"sec-ch-ua-mobile": "?0",
	"sec-ch-ua-platform": "Linux",
	"sec-fetch-dest": "empty",
	"sec-fetch-mode": "cors",
	"sec-fetch-site": "same-origin",
	"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" 
	}

	payload = json.dumps({
							"data": [ prompt, 45, 256, 256, 4, 5 ],
							"cleared": "false",
							"example_id": "null",
							"session_hash": "nothing",
							"action": "predict"
						})

	response = requests.request("POST", reqUrl, data=payload,  headers=headersList).json()

	hash = response["hash"]
	queue_position = str(response["queue_position"])
	
	#print("Hash : " + hash)
	#print("Queue Postion : " + queue_position)
	if AutoCall:
		filepath = latdifstatus(hash,prompt)
		return filepath
	else:
		return hash


def latdifstatus(hash, prompt="latentdiffusion"):

	reqUrl = "https://hf.space/embed/multimodalart/latentdiffusion/api/queue/status/"
	headersList = {
	"authority": "hf.space",
	"accept": "*/*",
	"accept-language": "en-US,en;q=0.9",
	"cache-control": "no-cache",
	"content-type": "application/json",
	"dnt": "1",
	"origin": "https://hf.space",
	"pragma": "no-cache",
	"referer": "https://hf.space/embed/multimodalart/latentdiffusion/+",
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

		time.sleep(10)

		response = requests.request("POST", reqUrl, data=payload,  headers=headersList).json()
		status = response["status"]
		#print("Status : " + status)

	imagelist = []
	for i in range(4):
		data = response["data"]["data"][1][i][0].split(",")[1]
		image = base64.b64decode(data)

		with open(f"{i+1}-{prompt}.png","wb") as file:
			file.write(image)

		imagelist.append(f"{i+1}-{prompt}.png")

	return imagelist


##############################################################################################################
# speech to text


r = sr.Recognizer()

def get_large_audio_transcription(path,message):

	id = message.id
	sound = AudioSegment.from_wav(path)  
	chunks = split_on_silence(sound,
		min_silence_len = 500,
		silence_thresh = sound.dBFS-14,
		keep_silence=500,
	)

	folder_name = f"audio-chunks-{id}"
	if not os.path.isdir(folder_name):
		os.mkdir(folder_name)
	whole_text = ""

	tsize = os.path. getsize(path)
	# edi = app.send_message(message.chat.id,f"Total Size: {tsize}") # status
	psize = 0

	for i, audio_chunk in enumerate(chunks, start=1):
		chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
		audio_chunk.export(chunk_filename, format="wav")

		with sr.AudioFile(chunk_filename) as source:
			audio_listened = r.record(source)

			try:
				text = r.recognize_google(audio_listened)
			except sr.UnknownValueError as e:
				#print("Error:", str(e))
				whole_text += "\n(error)\n"
			else:
				text = f"{text.capitalize()}. "
				#print(chunk_filename, ":", text)
				whole_text += text
		size = os.path. getsize(chunk_filename)        
		psize = psize + size
		# app.edit_message_text(f"Processed {psize/1024/1024} MB out of {tsize/1024/1024} MB - {math.floor(psize*100/tsize)}%",message.chat.id,edi.message_id)

	return whole_text


def splitfn(file,message,output):
	
	converted = get_large_audio_transcription(file,message)
	
	with open(output,"w") as file:
		file.write(converted)
	
	shutil.rmtree(f"audio-chunks-{message.id}", ignore_errors=True)
	return output



#######################################################################################################################################################
# text to speech


def texttospeech(file,output):
	''' Takes Text File and Output FileName ( Text 2 Speech ) '''

	with open(file,"r") as readfile:
		spctext = readfile.read()

	myobj = gTTS(text=spctext, lang='en', slow=False)
	myobj.save(output)
	return output


#######################################################################################################################################################
# zyro ai upscaller


def upscale(file,output):
	reqUrl = "https://upscaler.zyro.com/v1/ai/image-upscaler"

	headersList = {
	"authority": "upscaler.zyro.com",
	"accept": "application/json, text/plain, */*",
	"accept-language": "en-US,en;q=0.9",
	"cache-control": "no-cache",
	"content-type": "application/json",
	"dnt": "1",
	"origin": "https://zyro.com",
	"pragma": "no-cache",
	"referer": "https://zyro.com/",
	"sec-ch-ua-mobile": "?0",
	"sec-ch-ua-platform": "Linux",
	"sec-fetch-dest": "empty",
	"sec-fetch-mode": "cors",
	"sec-fetch-site": "same-site",
	"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" 
				}

	with open(file,"rb") as byte:
			rdata = base64.b64encode(byte.read()).decode('utf-8')

	payload = json.dumps({"image_data": rdata})
	response = requests.request("POST", reqUrl, data=payload,  headers=headersList).json()

	data = response["upscaled"].split(",")[1]
	image = base64.b64decode(data)

	with open(output,"wb") as file:
		file.write(image)

	return output


#######################################################################################################################################################
# cog video ( text to video )


def cogvideo(prompt,AutoCall=True):

	reqUrl = "https://hf.space/embed/THUDM/CogVideo/api/queue/push/"
	headersList = {
	"authority": "hf.space",
	"accept": "*/*",
	"accept-language": "en-US,en;q=0.9",
	"cache-control": "no-cache",
	"content-type": "application/json",
	"dnt": "1",
	"origin": "https://hf.space",
	"pragma": "no-cache",
	"referer": "https://hf.space/embed/THUDM/CogVideo/+?__theme=light",
	"sec-ch-ua-mobile": "?0",
	"sec-ch-ua-platform": "Linux",
	"sec-fetch-dest": "empty",
	"sec-fetch-mode": "cors",
	"sec-fetch-site": "same-origin",
	"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36" 
				}

	payload = """
			{
				"fn_index": 1,
				"data": [ "prompt", 1, 1234, 1, null ],
				"action": "predict",
				"session_hash": "nothing"
			}
			  """
	payload = payload.replace('"prompt"',f'"{prompt}"')

	response = requests.request("POST", reqUrl, data=payload,  headers=headersList).json()
	hash = response["hash"]
	queue_position = str(response["queue_position"])
	
	#print("Hash : " + hash)
	#print("Queue Postion : " + queue_position)
	if AutoCall:
		filepath = cogvideostatus(hash,prompt)
		return filepath
	else:
		return hash, int(queue_position)


def cogvideostatus(hash,prompt="cogvideo"):

	reqUrl = "https://hf.space/embed/THUDM/CogVideo/api/queue/status/"
	headersList = {
	"authority": "hf.space",
	"accept": "*/*",
	"accept-language": "en-US,en;q=0.9",
	"cache-control": "no-cache",
	"content-type": "application/json",
	"dnt": "1",
	"origin": "https://hf.space",
	"pragma": "no-cache",
	"referer": "https://hf.space/embed/THUDM/CogVideo/+?__theme=light",
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

	data = response["data"]["data"][1]["data"].split(",")[1]
	video = base64.b64decode(data)
	with open(f"{prompt}.mp4","wb") as file:
		file.write(video)

	return f"{prompt}.mp4"


########################################################################################################################################################	
