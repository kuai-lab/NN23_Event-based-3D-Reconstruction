import torch
from model.model import *


def load_model(path_to_model):
    print('Loading model {}...'.format(path_to_model))
    raw_model = torch.load(path_to_model)
    arch = raw_model['arch']

    try:
        model_type = raw_model['model']
    except KeyError:
        model_type = raw_model['config']['model']

    print ("Model Type", model_type)
    # instantiate model
    model = eval(arch)(model_type)
    config = raw_model['config']

    # load model weights
    # model.load_state_dict(checkpoint['state_dict'])
    if config["use_phased_arch"]:
        C, (H, W) = config["model"]["num_bins"], config["model"]["spatial_resolution"]
        dummy_input = torch.Tensor(1, C, H, W)
        times = torch.Tensor(1)
        _ = model.forward(dummy_input, times=times, prev_states=None)

    model.load_state_dict(raw_model['state_dict'])

    return model


def get_device(use_gpu):
    if use_gpu and torch.cuda.is_available():
        device = torch.device('cuda:0')
    else:
        device = torch.device('cpu')
    print('Device:', device)

    return device
