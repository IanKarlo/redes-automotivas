import torch
from torch import nn
from torchvision.models import efficientnet_b0

def transform_package_in_matrix(package):
    matrix = []
    for id in package:
        binary_string = bin(int(id, 16))[2:].zfill(16)
        binary_list = [int(bit) for bit in binary_string]
        matrix.append(binary_list)
    return matrix

def normalize_matrix_package(package_matrix):
    tensor = torch.tensor(package_matrix, dtype=torch.float32)
    tensor = tensor.unsqueeze(0).unsqueeze(0)
    return tensor

class CNNClassifier():
    def __init__(self):
        self.model = self.get_model()
        self.model.eval()
    def get_model(self):
        model = efficientnet_b0()
        out_ftrs = 5

        model.features[0][0] = nn.Conv2d(1, 32, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
        num_ftrs = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(num_ftrs, out_ftrs)

        model.load_state_dict(torch.load('files/model', map_location=torch.device('cpu')))

        return model

    def transform_data(self, package):
        matrix_package = transform_package_in_matrix(package)
        normalized_matrix_package = normalize_matrix_package(matrix_package)
        return normalized_matrix_package

    def validate_package(self, package):
        input_data = self.transform_data(package)
        y_logits = self.model(input_data)
        y_pred = torch.softmax(y_logits, dim=1).argmax(dim=1)
        return y_pred.item()