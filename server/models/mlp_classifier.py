import torch
from torch import nn
import os

class MLPClassifier(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 2)  # 2 classes: No Finding, LBP
        )

    def forward(self, x):
        return self.fc(x)

class MLPClassifierHandler:
    def __init__(self):
        self.model = MLPClassifier(input_dim=1024).cuda()
        current_dir = os.path.dirname(os.path.abspath(__file__))  # models/
        model_path = os.path.join(current_dir, 'pretrained_model', 'mlp_classifier.pth')
        self.model.load_state_dict(torch.load(model_path))

    def predict(self, img_emb, text_emb):
        emb = torch.cat([img_emb, text_emb], dim=-1).unsqueeze(0).cuda()
        with torch.no_grad():
            outputs = self.model(emb)
            soft_labels = torch.sigmoid(outputs).cpu().numpy().flatten()
            return {
                "No Finding": float(soft_labels[0]),
                "LBP": float(soft_labels[1])
            }
