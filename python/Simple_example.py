#!/usr/bin/env python3

# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# pylint: disable=invalid-name, no-member

import torch
from torch import nn
from torch.optim import Adam, lr_scheduler
from torch.utils.data import DataLoader, TensorDataset

#from root_utils import tree_to_pandas

MODEL_PATH = "../models/"
MODEL_NAME = "Simple_example_bindings"
ONNX_MODEL_PATH = f"{MODEL_PATH}/{MODEL_NAME}.onnx"
batch_size = 32
data_size = 1024
classes = 5

class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()

        self.input = nn.Linear(5,15)
        self.hidden = nn.Linear(15,10)
        self.out = nn.Linear(10,classes)


    def forward(self, x1, x2, x3, x4, x5): # pylint: disable=too-many-arguments
        x = torch.cat((x1, x2, x3, x4, x5), dim=1)
        x = torch.tanh(self.input(x))
        x = torch.tanh(self.hidden(x))
        x = torch.softmax(self.out(x), 0) # No softmax() if we use CrossEntropyLoss()
        return x

model = SimpleNet()

data_1 = torch.rand(data_size, 1)
data_2 = torch.rand(data_size, 1)
data_3 = torch.rand(data_size, 1)
data_4 = torch.rand(data_size, 1)
data_5 = torch.rand(data_size, 1)

data = torch.cat((data_1, data_2, data_3, data_4, data_5), dim=1)
y = torch.floor(data.sum(1)).long().view(-1,1)

# One hot encoding buffer that you create out of the loop and just keep reusing
y_onehot = torch.FloatTensor(batch_size, classes)

dataset = TensorDataset(data_1, data_2, data_3, data_4, data_5, y)
train_loader = DataLoader(dataset, batch_size=batch_size)

optim = Adam(model.parameters(), lr=0.001)
scheduler = lr_scheduler.ExponentialLR(optim, gamma=0.95)
criterion = nn.MSELoss()
epoch = 50

for epoch in range(100):
    for idx, (train_x1, train_x2, train_x3, train_x4, train_x5, train_label) \
        in enumerate(train_loader):
        # Converting labels to one-hot
        y_onehot.zero_()
        y_onehot.scatter_(1, train_label, 1)
        optim.zero_grad()
        predict_y = model(train_x1, train_x2, train_x3, train_x4, train_x5)
        _error = criterion(predict_y, y_onehot)
        _error.backward()
        optim.step()
    if epoch % 5 == 0:
        print(f"epoch:{epoch}, idx: {idx}, loss: {_error}")

dummy_input1 = torch.rand(batch_size, 1)
dummy_input2 = torch.rand(batch_size, 1)
dummy_input3 = torch.rand(batch_size, 1)
dummy_input4 = torch.rand(batch_size, 1)
dummy_input5 = torch.rand(batch_size, 1)
model(dummy_input1, dummy_input2, dummy_input3, dummy_input4, dummy_input5)

torch.save(model, "{MODEL_PATH}/{MODEL_NAME}.torch")

#example_data = example_data.to(self.device)

torch.onnx.export(model,                                          # model being run
                  (dummy_input1, dummy_input2, dummy_input3,
                   dummy_input4, dummy_input5),                   # model input (or a tuple for multiple inputs)
                  ONNX_MODEL_PATH,                                # where to save the model (can be a file or file-like object)
                  export_params=True,                             # store the trained parameter weights inside the model file
                  opset_version=14,                               # the ONNX version to export the model to: https://onnxruntime.ai/docs/reference/compatibility.html
                  do_constant_folding=True,                       # whether to execute constant folding for optimization
                  input_names=['fX', 'fY', 'fPt', 'fEta', 'fPhi'], # the model's input names
                  output_names=['output'],                        # the model's output names
                  dynamic_axes={'fX': {0: 'batch_size'},    # variable length axes
                                'fY': {0: 'batch_size'},
                                'fPt': {0: 'batch_size'},
                                'fEta': {0: 'batch_size'},
                                'fPhi': {0: 'batch_size'},
                                'output': {0: 'batch_size'}})
