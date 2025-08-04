from PIL import Image
from models.medclip_model import MedClipHandler
from models.mlp_classifier import MLPClassifierHandler

# Initialize model handlers globally
medclip_handler = MedClipHandler()
mlp_handler = MLPClassifierHandler()

async def process_diagnosis(image_file, text):
    image_data = Image.open(image_file.file).convert("RGB")
    img_emb, text_emb = medclip_handler.encode(image_data, text)
    result = mlp_handler.predict(img_emb, text_emb)
    return result
