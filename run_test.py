import argparse

import torch
import torchvision

from tirg.datasets import Fashion200k
from tirg.img_text_composition_models import TIRG
from tirg.test_retrieval import test


def load_fashion_dataset(dataset_path):
    trainset = Fashion200k(
        path=dataset_path,
        split='train',
        transform=torchvision.transforms.Compose([
            torchvision.transforms.Resize(224),
            torchvision.transforms.CenterCrop(224),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize([0.485, 0.456, 0.406],
                                             [0.229, 0.224, 0.225])
        ]))
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

    print 'trainset size:', len(trainset)
    print 'testset size:', len(testset)
    return trainset, testset

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('dataset_path', type=str)
    argparser.add_argument('checkpoint_path', type=str)
    args = argparser.parse_args()
    dataset_path = args.dataset_path
    checkpoint_path = args.checkpoint_path

    trainset, testset = load_fashion_dataset(dataset_path)
    checkpoint = torch.load(checkpoint_path)
    model_state_dict = checkpoint['model_state_dict']
    
    model = TIRG([t.decode('utf-8') for t in trainset.get_all_texts()], 512)
    
    print 'Successfully created the model'
    


if __name__ == '__main__':
    main()
