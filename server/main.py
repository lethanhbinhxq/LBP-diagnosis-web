from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import torch
from medclip import MedCLIPModel, MedCLIPVisionModelViT, MedCLIPProcessor
from model import mlp

# Initialize FastAPI
app = FastAPI()

# CORS for Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("CUDA available in server:", torch.cuda.is_available())

# Load processor
processor = MedCLIPProcessor()

# Load MedCLIP model
medclip_model = MedCLIPModel(vision_cls=MedCLIPVisionModelViT)
medclip_model.from_pretrained("./model/medclip_pretrained")
medclip_model.cuda()

# Load MLP classifier
clf = mlp.MLPClassifier(input_dim=1024).cuda()
clf.load_state_dict(torch.load("./model/mlp_classifier.pth"))

# Inference function
def infer(image, text):
    inputs = processor(text=[text], images=[image], return_tensors="pt", padding=True)
    with torch.no_grad():
        img_emb = medclip_model.encode_image(inputs['pixel_values'].cuda()).cpu()
        text_emb = medclip_model.encode_text(inputs['input_ids'].cuda(), inputs['attention_mask'].cuda()).cpu()
    emb = torch.cat([img_emb.squeeze(0), text_emb.squeeze(0)], dim=-1)
    emb = emb.unsqueeze(0).cuda()
    with torch.no_grad():
        outputs = clf(emb)
        pred_class = torch.argmax(outputs, dim=1).item()
    return 'No Finding' if pred_class == 0 else 'LBP'

# API endpoint
@app.post("/predict")
async def predict(image: UploadFile = File(...), text: str = Form(...)):
    image_data = Image.open(image.file).convert("RGB")
    result = infer(image_data, text)
    print(result)
    return JSONResponse(content={"diagnosis": result})
