import os

import flask
from flask import send_file

from config import dataset_path, model_path, dataset, batch_size, all_imgs, model, testset
from query import prep_data_model


app = flask.Flask(__name__, static_folder='/Users/timowang/Entwickler/')


@app.route('/test_get_image', methods=['GET'])
def test_get_image():
    image_path = testset.img_path + testset.imgs[idx]['file_path']
    print image_path
    return send_file(image_path)


if __name__ == '__main__':
    all_imgs, model, testset = prep_data_model(dataset_path, model_path)
    app.run(host='0.0.0.0', port=80)