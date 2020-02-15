import argparse

import torch
import torchvision

from tirg.datasets import Fashion200k
from tirg.img_text_composition_models import TIRG


def load_fashion_dataset(dataset_path):
    testset = Fashion200k(
        path=dataset_path,
        split='test',
        transform=torchvision.transforms.Compose([
            torchvision.transforms.Resize(224),
            torchvision.transforms.CenterCrop(224),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize([0.485, 0.456, 0.406],
                                             [0.229, 0.224, 0.225])
        ]))

    print 'testset size:', len(testset)
    return testset


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('dataset_path', type=str)
    argparser.add_argument('checkpoint_path', type=str)
    args = argparser.parse_args()

    dataset_path = args.dataset_path
    checkpoint_path = args.checkpoint_path

    testset = load_fashion_dataset(dataset_path)
    print 'Test set loaded.'
    

if __name__ == '__main__':
    main()