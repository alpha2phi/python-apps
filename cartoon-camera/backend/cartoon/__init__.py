import logging
import os

from PIL import Image
import numpy as np
import torch
from torch.autograd import Variable
import torchvision.transforms as transforms

from network.Transformer import Transformer

model_path = os.path.abspath("./pretrained-model")
styles = {0: "Hayao", 1: "Hosoda", 2: "Paprika", 3: "Shinkai"}

gpu = torch.cuda.is_available()


def load_models():
    """Load the pre-trained models."""
    models = {}
    for style in styles.values():
        model = Transformer()
        model_file_path = os.path.join(model_path, style + "_net_G_float.pth")

        logging.info(f"Loading { style } from { model_file_path }...")
        model.load_state_dict(
            torch.load(os.path.join(model_path, style + "_net_G_float.pth"))
        )
        model.eval()
        if gpu:
            model.cuda()
        else:
            model.float()

        models[style] = model

    return models


models = load_models()


def cartoonify(input_image, style_id=0, load_size=450):
    """Cartoonify an image."""
    style = styles[int(style_id)]
    model = models[style]
    load_size = int(load_size)

    # resize image, keep aspect ratio
    h = input_image.size[0]
    w = input_image.size[1]
    ratio = h * 1.0 / w
    if ratio > 1:
        h = load_size
        w = int(h * 1.0 / ratio)
    else:
        w = load_size
        h = int(w * ratio)
    input_image = input_image.resize((h, w), Image.BICUBIC)

    input_image = np.asarray(input_image)
    # RGB -> BGR
    input_image = input_image[:, :, [2, 1, 0]]
    input_image = transforms.ToTensor()(input_image).unsqueeze(0)

    # preprocess, (-1, 1)
    input_image = -1 + 2 * input_image
    if gpu:
        input_image = Variable(input_image).cuda()
    else:
        input_image = Variable(input_image).float()

    # forward
    with torch.no_grad():
        output_image = model(input_image)
        output_image = output_image[0]

    # BGR -> RGB
    output_image = output_image[[2, 1, 0], :, :]

    # deprocess, (0, 1)
    output_image = output_image.data.cpu().float() * 0.5 + 0.5

    output_image = output_image.numpy()
    output_image = np.uint8(output_image.transpose(1, 2, 0) * 255)
    output_image = Image.fromarray(output_image)

    return output_image

