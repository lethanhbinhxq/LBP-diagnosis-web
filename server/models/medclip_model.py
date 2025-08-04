import torch
from medclip import MedCLIPModel, MedCLIPVisionModelViT, MedCLIPProcessor

class MedClipHandler:
    def __init__(self):
        print("CUDA available:", torch.cuda.is_available())
        self.processor = MedCLIPProcessor()
        self.model = MedCLIPModel(vision_cls=MedCLIPVisionModelViT)
        self.model.from_pretrained("./pretrained_model/medclip_pretrained")
        self.model.cuda()

    def encode(self, image, text):
        inputs = self.processor(text=[text], images=[image], return_tensors="pt", padding=True)
        with torch.no_grad():
            img_emb = self.model.encode_image(inputs['pixel_values'].cuda()).cpu()
            text_emb = self.model.encode_text(inputs['input_ids'].cuda(), inputs['attention_mask'].cuda()).cpu()
        return img_emb.squeeze(0), text_emb.squeeze(0)
