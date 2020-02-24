import argparse
import os
import pickle

import numpy as np
import torch
import torchvision
from tqdm import tqdm

from tirg.datasets import Fashion200k
from tirg.img_text_composition_models import TIRG
from utils import load_fashion_dataset


device = 'cpu'


def query(mod, img_id, img, model, all_imgs):
    mods = [mod]
    imgs = [img]
    if 'torch' not in str(type(imgs[0])):
        imgs = [torch.from_numpy(d).float() for d in imgs]
    imgs = torch.stack(imgs).float()
    imgs = torch.autograd.Variable(imgs).to(device)
    query_index = model.compose_img_text(imgs, mods).data.cpu().numpy()
    print "Composing img and text..."
    query_index /= np.linalg.norm(query_index)
    similarities = query_index.dot(all_imgs.T)
    similarities[0, img_id] = -10e10
    nn_result = np.argsort(-similarities[0, :])[:20]
    return nn_result


def initialize_model(checkpoint_path, trainset):
    checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
    model_state_dict = checkpoint['model_state_dict']
    model = TIRG([t.decode('utf-8') for t in trainset.get_all_texts()], 512)
    model.load_state_dict(model_state_dict)
    print 'Model loaded and initialized.'
    return model


def prep_data_model(dataset_path, model_path):
    trainset, testset = load_fashion_dataset(dataset_path)
    print 'Testset loaded.'
    checkpoint_path = os.path.join(model_path, 'checkpoint_fashion200k.pth')
    model = initialize_model(checkpoint_path, trainset)
    model.eval()
    all_imgs_path = os.path.join(model_path, 'all_imgs_normalized.pkl')
    fp = open(all_imgs_path, 'rb')
    all_imgs = pickle.load(fp)
    fp.close()
    all_captions_path = os.path.join(model_path, 'all_captions.pkl')
    fp = open(all_captions_path, 'rb')
    all_captions = pickle.load(fp)
    fp.close()
    return all_imgs, model, testset


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('dataset_path', type=str)
    argparser.add_argument('model_path', type=str)
    argparser.add_argument('--dataset', type=str, default='fashion200k')
    argparser.add_argument('--batch_size', type=int, default=1)
    args = argparser.parse_args()

    dataset_path = args.dataset_path
    model_path = args.model_path
    dataset = args.dataset
    batch_size = args.batch_size

    all_imgs, model, testset = prep_data_model(dataset_path, model_path)

    while True:
        line = raw_input()
        if line == 'stop':
            break
        
        mod, img_id = line.split('|')
        img_id = int(img_id)
        img = testset.get_img(img_id)
        nn_result = query(mod, img_id, img, model, all_imgs)
        print nn_result


if __name__ == '__main__':
    main()