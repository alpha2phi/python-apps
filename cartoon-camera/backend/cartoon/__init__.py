from PIL import Image

model_path = "./pretrained_model"

models = {}

def load_modesl():

    for style in styles:
        model = Transformer()
        response = s3.get_object(Bucket=bucket, Key=f"models/{style}_net_G_float.pth")
        state = torch.load(BytesIO(response["Body"].read()))
        model.load_state_dict(state)
        model.eval()
        models[style] = model

    return models


def cartoonify():
    pass
