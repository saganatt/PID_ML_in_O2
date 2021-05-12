# PID ML in O2

Porting Python PID ML codes to C++ O2.

## Python API - train + apply

Based on [documentation](https://pytorch.org/docs/master/onnx.html) and [example](https://pytorch.org/tutorials/advanced/super_resolution_with_onnxruntime.html)  

1. Load new environment: `source load.sh`
2. Install all packages: `pip install -e .`
3. Open the notebook: `python -m notebook Simple_example.ipynb`
4. To quit the environment, type again `source load.sh`.

`source load.sh --recreate` creates a new, fresh environment.

## C++ API - apply

Based on [example](https://github.com/microsoft/onnxruntime/blob/master/samples/c_cxx/model-explorer/model-explorer.cpp)

1. Pre-build with CMake. Use your system CMake if you have version >= 3.17 or borrow one from O2:
```
<path_to_alice>/sw/ubuntu1804_x86-64/CMake/<o2_version>/bin/cmake .
```
2. Build with make.
3. Run: `./pid-in-o2 <path_to_model_file>`

### O2 Analysis Task
Available on repo, [branch](https://github.com/saganatt/AliceO2/tree/pid-in-o2), [file](https://github.com/saganatt/AliceO2/blob/pid-in-o2/Analysis/Tutorials/src/pidWithONNX.cxx)

To launch this:
1. If you don't have O2 build, you need to build it with aliBuild: `aliBuild build O2 --defaults o2`.
2. Otherwise you can make it faster:
```
cd alice/sw/BUILD/O2-latest/O2/
ninja stage/bin/o2-analysistutorial-pid-with-onnx
cp stage/bin/o2-analysistutorial-pid-with-onnx <your_analysis_dir>
```
3. Build ONNXRuntime: `aliBuild build onnxruntime`

   Known issues:
   - `Could not find PythonLibs` - install `python3-dev` (Ubuntu) or `python3-devel` (CentOS)

4. Enter both O2 and ONNXRuntime: `alienv enter O2/latest onnxruntime/latest`
5. Run: `./o2-analysistutorial-pid-with-onnx --aod-file <some_input_AOD> -b`

The model outputs are saved to the `results` histogram in `AnalysisResults.root`.

Most important parts of the analysis code:
- lines 23-35: setting up the ONNX session
- lines 79-80: putting tracks data as ONNX input
- line 92: applying the model
- lines 102-106: saving the outputs to a histogram
