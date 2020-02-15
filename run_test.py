import argparse

import torch

from tirg.datasets import Fashion200k
from tirg.img_text_composition_models import TIRG
from tirg.test_retrieval import test


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('dataset_path', type=str)
    argparser.add_argument('pretrained_model_path', type=str)

    dataset_path = args.dataset_path
    pretrained_model_path = args.pretrained_model_path
    
    model = TIRG()
    model.load_state_dict(torch.load(pretrained_model_path))
    


if __name__ == '__main__':
    main()
