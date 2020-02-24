import os

import flask
from flask import Response, send_file

from config import dataset_path, model_path, dataset, batch_size, all_imgs, model, testset
from query import prep_data_model, query


app = flask.Flask(__name__, static_folder='/Users/timowang/Entwickler/')


@app.route('/get_image', methods=['GET', 'POST'])
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


@app.route('/query_img_ids', methods=['GET', 'POST'])
def query_img_ids():
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
    nn_result = query(mod, img_id, img, model, all_imgs)
    print nn_result
    return Response("{'img_ids': %s}" % str(nn_result),
                    status=200, mimetype='application/json')


if __name__ == '__main__':
    all_imgs, model, testset = prep_data_model(dataset_path, model_path)
    app.run(host='0.0.0.0', port=80)