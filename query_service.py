import os

import flask
from flask import Response, send_file

from config import dataset_path, model_path, dataset, batch_size, all_imgs, model, testset
from query import prep_data_model, query


app = flask.Flask(__name__, static_folder='/Users/timowang/Entwickler/')


@app.route('/test_get_image', methods=['GET'])
def test_get_image():
    image_path = testset.img_path + testset.imgs[14027]['file_path']
    return send_file(image_path)


@app.route('/query', methods=['GET'])
def query():
    data = {'success': False}
    params = flask.request.json
    if not params:
        params = flask.request.args

    if not params:
        return Response("{'error': 'Missing either mod or img_id'}",
                        status=400, mimetype='application/json')
    
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