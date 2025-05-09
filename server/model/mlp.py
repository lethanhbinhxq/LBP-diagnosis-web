from torch import nn

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