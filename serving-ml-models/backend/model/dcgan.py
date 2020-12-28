import torch
import torchvision.transforms as Transforms

use_gpu = True if torch.cuda.is_available() else False

model = torch.hub.load('facebookresearch/pytorch_GAN_zoo:hub', 'DCGAN', pretrained=True, useGPU=use_gpu)

num_images = 1

def dcgan():
    noise, _ = model.buildNoiseData(num_images)
    with torch.no_grad():
        generated_images = model.test(noise)

    transform = Transforms.Compose([Transforms.Normalize((-1., -1., -1.), (2, 2, 2)),
                                    Transforms.ToPILImage()])
    generated_images = generated_images[0]
    generated_images = transform(generated_images.clamp(min=-1, max=1))
    return generated_images
