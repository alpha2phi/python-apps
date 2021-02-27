import os
import torch
from PIL import Image
from network.Transformer import Transformer

import logging

model_path = os.path.abspath("./pretrained-model")
styles = {0: "Hosoda", 1: "Hayao", 2: "Shinkai", 3: "Paprika"}


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
        models[style] = model

    return models


models = load_models()


def cartoonify():
    pass
