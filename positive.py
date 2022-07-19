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

