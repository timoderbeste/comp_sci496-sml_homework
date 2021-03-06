import argparse
import json

import torch

from tirg.img_text_composition_models import TIRG
from tirg.test_retrieval import test
from utils import load_fashion_dataset


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('dataset_path', type=str)
    argparser.add_argument('checkpoint_path', type=str)
    argparser.add_argument('--batch_size', type=int, default=1)
    argparser.add_argument('--dataset', type=str, default='fashion200k')
    args = argparser.parse_args()
    dataset_path = args.dataset_path
    checkpoint_path = args.checkpoint_path
    batch_size = args.batch_size
    dataset = args.dataset

    trainset, testset = load_fashion_dataset(dataset_path)
    
    checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
    model_state_dict = checkpoint['model_state_dict']
    model = TIRG([t.decode('utf-8') for t in trainset.get_all_texts()], 512)
    model.load_state_dict(model_state_dict)
    print 'Successfully created and initialized the model'
    
    print 'Start running test retrieval...'
    test_result = test(args, model, testset)
    
    print test_result
    try:
        with open('/tmp/tirg_test_results.json', 'w+') as fp:
            json.dump(test_result, fp)
    except e:
        print e


if __name__ == '__main__':
    main()
