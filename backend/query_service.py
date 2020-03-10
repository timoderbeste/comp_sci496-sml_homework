import base64
import os
from io import BytesIO

import flask
from flask import Response, send_file, jsonify
# from flask_cors import CORS
from PIL import Image

from config import dataset_path, model_path, dataset, batch_size, all_imgs, model, testset
from query import prep_data_model, query


app = flask.Flask(__name__, static_folder='/Users/timowang/Entwickler/')
# CORS(app, resources={r'*': {'origins': '*'}})


def process_mod(mod):
    mod = mod.lower()
    
    mod = mod.replace('black', 'WHITE')
    mod = mod.replace('white', 'black')
    mod = mod.replace('WHITE', 'white')
    
    return mod


@app.route('/image', methods=['GET', 'POST'])
def get_image():
    params = flask.request.json
    if not params:
        params = flask.request.args
    
    if not params:
        return Response("{'error': 'Missing either mod or img_id'}",
                        status=400, mimetype='application/json')
    
    img_id = params.get('img_id')
    image_path = testset.img_path + testset.imgs[img_id]['file_path']
    print image_path
    fp = open(image_path, 'rb')
    img_base64 = base64.b64encode(fp.read())
    fp.close()
    print img_base64
    response_data = {
        'img_base64': img_base64
    }
    # return send_file(image_path)
    return jsonify(response_data)


@app.route('/img_ids_with_id', methods=['GET', 'POST'])
def get_img_ids_with_id():
    params = flask.request.json
    if not params:
        params = flask.request.args

    if not params:
        return Response("{'error': 'Missing either mod or img_id'}",
                        status=400, mimetype='application/json')
    
    print params
    
    mod = params.get('mod')
    mod = process_mod(mod)
    img_id = params.get('img_id')
    img = testset.get_img(img_id)
    nn_result = query(mod, all_imgs, img, model, img_id)
    print nn_result
    response_data = {
        'img_ids': list(nn_result)
    }
    return jsonify(response_data)


@app.route('/img_ids_with_img', methods=['GET', 'POST'])
def get_img_ids_with_img():
    params = flask.request.json
    if not params:
        params = flask.request.args
    
    if not params:
        return Response("{'error': 'Missing either mod or img_id'}",
                        status=400, mimetype='application/json')

    mod = params.get('mod')
    mod = process_mod(mod)
    img_base64 = params.get('img_base64')
    img_base64 = img_base64[img_base64.find('base64') + 7:]
    print mod
    print img_base64
    try:
        img = Image.open(BytesIO(base64.b64decode(img_base64)))
    except Exception as e:
        print e
    img = img.convert('RGB')
    img = testset.transform(img)
    
    nn_result = query(mod, all_imgs, img, model, None)
    print nn_result
    response_data = {
        'img_ids': list(nn_result)
    }
    return jsonify(response_data)


if __name__ == '__main__':
    all_imgs, model, testset = prep_data_model(dataset_path, model_path)
    app.run(host='0.0.0.0', port=80)