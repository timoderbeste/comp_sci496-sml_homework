import base64
import os
from io import BytesIO

import flask
from flask import Response, send_file
from PIL import Image

from config import dataset_path, model_path, dataset, batch_size, all_imgs, model, testset
from query import prep_data_model, query


app = flask.Flask(__name__, static_folder='/Users/timowang/Entwickler/')


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
    return send_file(image_path)


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
    img_id = params.get('img_id')
    img = testset.get_img(img_id)
    nn_result = query(mod, all_imgs, img, model, img_id)
    print nn_result
    return Response("{'img_ids': %s}" % str(nn_result),
                    status=200, mimetype='application/json')


@app.route('/img_ids_with_img', methods=['GET', 'POST'])
def get_img_ids_with_img():
    params = flask.request.json
    if not params:
        params = flask.request.args
    
    if not params:
        return Response("{'error': 'Missing either mod or img_id'}",
                        status=400, mimetype='application/json')

    mod = params.get('mod')
    img_base64 = params.get('img_base64')
    img = Image.open(BytesIO(base64.b64decode(img_base64)))
    img.convert('RGB')
    img = testset.transform(img)
    
    nn_result = query(mod, all_imgs, img, model, None)
    print nn_result
    return Response("{'img_ids': %s}" % str(nn_result),
                    status=200, mimetype='application/json')


if __name__ == '__main__':
    all_imgs, model, testset = prep_data_model(dataset_path, model_path)
    app.run(host='0.0.0.0', port=80)