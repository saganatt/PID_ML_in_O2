# PID ML in O2

Porting Python PID ML codes to C++ O2.

## Python API - in `python/`

1. Load new environment: `source load.sh`
2. Install all packages: `pip install -e .`
3. Open the notebook: `python -m notebook Simple_example.ipynb`
4. To quit the environment, type again `source load.sh`.

`source load.sh --recreate` creates a new, fresh environment.

## C++ API - in progress...

### Installing ONNX Runtime on Linux

```
wget https://github.com/microsoft/onnxruntime/releases/download/v1.4.0/onnxruntime-linux-x64-1.4.0.tgz
tar -xvf onnxruntime-linux-x64-1.4.0.tgz
cd onnxruntime-linux-x64-1.4.0/
sudo cp lib/* /usr/local/lib/
sudo ln -sf /usr/local/lib/libonnxruntime.so.1.4.0 /usr/local/lib/libonnxruntime.so
sudo cp include/* /usr/local/include/
```
