

import io
import torch
from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request
from flask import render_template, Response
import png
import cv2
import numpy as np

import model
import data



app = Flask(__name__)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
net = model.WasteNet(10).move(device)
# net.load_state_dict(torch.load('model/mar31_1103.pth', map_location=device))
net.load_state_dict(torch.load('model/apr23_2334.pth', map_location=device))
net.eval()

def bytes2PILImage(image_bytes):
    return Image.open(io.BytesIO(image_bytes)).convert('RGB')

def transform_image(pil_image):
    my_transforms = data.get_transform('test')
    return my_transforms(pil_image).unsqueeze(0)

def get_prediction(pil_image):
    tensor = transform_image(pil_image)
    outputs = net(tensor)
    predict = torch.argmax(outputs, -1).item()
    return data.id_label(predict)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        global img_bytes
        global class_name
        img_bytes = request.data

        img = bytes2PILImage(img_bytes)
        class_name = get_prediction(img)
        return class_name

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
