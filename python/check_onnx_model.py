"""
Examine ONNX models, both in text and on a graph.
"""

import argparse
import os
import onnx
from onnx import ModelProto
from onnx.tools.net_drawer import GetOpNodeProducer, GetPydotGraph

parser = argparse.ArgumentParser(description="Arguments to pass")
parser.add_argument("input_file", help="input ONNX model file")
args = parser.parse_args()

onnx_model = onnx.load(args.input_file)

print(f"Model {onnx_model}")

model = ModelProto()
with open(args.input_file, 'rb') as fid:
    content = fid.read()
    model.ParseFromString(content)

pydot_graph = GetPydotGraph(
    model.graph, name=model.graph.name, rankdir="LR", node_producer=GetOpNodeProducer("docstring")
)
pydot_graph.write_dot("graph.dot")
os.system("dot -O -Tpng graph.dot")
