import torch
from torch import nn
from models.medclip_model import MedClipHandler
from PIL import Image
from typing import Dict
import os

class MLPClassifier(nn.Module):
    def __init__(self, input_dim: int):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 2)  # 2 classes: No Finding, LBP
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.fc(x)  # logits, do NOT apply softmax here

class MLPClassifierHandler:
    def __init__(
        self,
        medclip_handler: MedClipHandler = None
    ):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.medclip = medclip_handler or MedClipHandler()
        
        # Infer input_dim from pretrained model
        # (Assume you saved the MLP with correct input_dim)
        current_dir = os.path.dirname(os.path.abspath(__file__)) 
        parent_dir = os.path.dirname(current_dir) 
        model_path = os.path.join(parent_dir, 'pretrained_model', 'mlp_classifier.pth')
        checkpoint = torch.load(model_path, map_location=self.device)
        input_dim = checkpoint["fc.0.weight"].shape[1] 
        self.model = MLPClassifier(input_dim=input_dim).to(self.device)
        self.model.load_state_dict(checkpoint)
        self.model.eval()  # IMPORTANT

    def predict(self, image: Image.Image, text: str) -> Dict[str, float]:
        """
        Predict class probabilities for a single image/text pair.
        Returns: {'No Finding': ..., 'LBP': ...}
        """
        img_emb, text_emb = self.medclip.encode(image, text)
        emb = torch.cat([img_emb, text_emb], dim=-1).unsqueeze(0).to(self.device)  # GPU

        with torch.no_grad():
            logits = self.model(emb)
            probs = torch.softmax(logits, dim=-1).cpu().squeeze(0).numpy()

        return {
            "No Finding": float(probs[0]),
            "LBP": float(probs[1])
        }
