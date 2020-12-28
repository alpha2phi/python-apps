import numpy as np
import torch
import torchvision.transforms as Transforms
from PIL import Image

use_gpu = True if torch.cuda.is_available() else False

# trained on high-quality celebrity faces "celebA" dataset
# this model outputs 512 x 512 pixel images
model = torch.hub.load('facebookresearch/pytorch_GAN_zoo:hub',
                       'PGAN', model_name='celebAHQ-512',
                       pretrained=True, useGPU=use_gpu)
# this model outputs 256 x 256 pixel images
# model = torch.hub.load('facebookresearch/pytorch_GAN_zoo:hub',
#                        'PGAN', model_name='celebAHQ-256',
#                        pretrained=True, useGPU=use_gpu)
num_images = 1

def pgan():
    noise, _ = model.buildNoiseData(num_images)
    with torch.no_grad():
        generated_images = model.test(noise)

    transform = Transforms.Compose([Transforms.Normalize((-1., -1., -1.), (2, 2, 2)),
                                    Transforms.ToPILImage()])
    generated_images = generated_images[0]
    generated_images = transform(generated_images.clamp(min=-1, max=1))
    return generated_images
