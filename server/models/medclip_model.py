import torch
from medclip import MedCLIPModel, MedCLIPVisionModel, MedCLIPVisionModelViT, MedCLIPProcessor
from PIL import Image
from typing import Tuple 

class MedClipHandler:
    def __init__(self, pretrained_path: str = "./pretrained_model/medclip_pretrained"):
        print("CUDA available:", torch.cuda.is_available())
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load MedCLIP model and processor
        self.processor = MedCLIPProcessor()
        self.model = MedCLIPModel(vision_cls=MedCLIPVisionModel)
        self.model.from_pretrained(pretrained_path)
        self.model.to(self.device)
        self.model.eval()  # IMPORTANT: use eval mode for inference

    def encode(self, image: Image.Image, text: str) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Encode a single image and text to embeddings
        Returns: (img_emb, text_emb), both are 1D tensors on CPU
        """
        inputs = self.processor(text=[text], images=[image], return_tensors="pt", padding=True)
        pixel_values = inputs['pixel_values'].to(self.device)
        input_ids = inputs['input_ids'].to(self.device)
        attention_mask = inputs['attention_mask'].to(self.device)

        with torch.no_grad():
            img_emb = self.model.encode_image(pixel_values)
            text_emb = self.model.encode_text(input_ids, attention_mask)

        return img_emb.squeeze(0), text_emb.squeeze(0)
