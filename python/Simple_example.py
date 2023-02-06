#!/usr/bin/env python

import numpy as np
import pandas as pd
#import uproot3

import torch
import torch.nn as nn
from torch.optim import Adam, lr_scheduler
from torch.utils.data import DataLoader, TensorDataset
from torchvision import transforms
import torch.nn.functional as F

#from root_utils import tree_to_pandas

MODEL_PATH = "../models/"
MODEL_NAME = "Simple_example_multioutput"
ONNX_MODEL_PATH = "%s/%s.onnx" % (MODEL_PATH, MODEL_NAME)
batch_size = 32
data_size = 1024
classes = 5

class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()

        self.input = nn.Linear(5,15)
        self.hidden = nn.Linear(15,10)
        self.out = nn.Linear(10,classes)


    def forward(self, x):
        x = torch.tanh(self.input(x))
        x = torch.tanh(self.hidden(x))
        x = torch.softmax(self.out(x), 0) # No softmax() if we use CrossEntropyLoss()
        return x

model = SimpleNet()

x = torch.rand(data_size,5)
x[:5]

y = torch.floor(x.sum(1)).long().view(-1,1)
print(y[:5])

# One hot encoding buffer that you create out of the loop and just keep reusing
y_onehot = torch.FloatTensor(batch_size, classes)

dataset = TensorDataset(x,y)
train_loader = DataLoader(dataset, batch_size=batch_size)

optim = Adam(model.parameters(), lr=0.001)
scheduler = lr_scheduler.ExponentialLR(optim, gamma=0.95)
criterion = nn.MSELoss()
epoch = 50

for epoch in range(1000):
    for idx, (train_x, train_label) in enumerate(train_loader):
        # Converting labels to one-hot
        y_onehot.zero_()
        y_onehot.scatter_(1, train_label, 1)
    #     label_np = np.zeros((train_label.shape[0], 10))
        optim.zero_grad()
        predict_y = model(train_x)
        _error = criterion(predict_y, y_onehot)
        _error.backward()
        optim.step()
    if epoch % 5 == 0:
        print('epoch:{}, idx: {}, loss: {}'.format(epoch, idx, _error))

dummy_input = torch.tensor([0.3,1,1.2,0.3,1])
model(dummy_input)

torch.save(model, "%s/%s.torch" % (MODEL_PATH, MODEL_NAME))

torch.onnx.export(model,dummy_input, ONNX_MODEL_PATH,input_names=["input"],output_names=["out"])

#example_data = example_data.to(self.device)

torch.onnx.export(model,                                          # model being run
                  dummy_input,                                    # model input (or a tuple for multiple inputs)
                  ONNX_MODEL_PATH,                                # where to save the model (can be a file or file-like object)
                  export_params=True,                             # store the trained parameter weights inside the model file
                  opset_version=14,                               # the ONNX version to export the model to: https://onnxruntime.ai/docs/reference/compatibility.html
                  do_constant_folding=True,                       # whether to execute constant folding for optimization
                  input_names=['input'],                          # the model's input names
                  output_names=['output'],                        # the model's output names
                  dynamic_axes={'input': {0: 'batch_size'},       # variable length axes
                                'output': {0: 'batch_size'}})
