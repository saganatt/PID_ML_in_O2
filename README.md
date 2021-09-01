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

### O2Physics Analysis Task
ONNXRuntime is integrated with O2Physics - you can simply add this as a library dependency to the CMakeLists.txt for your task, as [here](https://github.com/saganatt/O2Physics/blob/pid-with-onnx/Tasks/PIDML/CMakeLists.txt).

An example of a task using ONNX model is available in O2Physics repo: [branch](https://github.com/saganatt/O2Physics/tree/pid-with-onnx), [file](https://github.com/saganatt/O2Physics/blob/pid-with-onnx/Tasks/PIDML/pidWithONNX.cxx).

To launch this:
1. Download and checkout to the proper branch:
```
git add remote saganatt https://github.com/saganatt/O2Physics.git
git fetch saganatt
git checkout saganatt/pid-with-onnx
```
2. If you don't have O2Physics built, you need to build it with aliBuild: `aliBuild build O2Physics --defaults o2`.<br>
   Otherwise, you can make it faster:
```
cd alice/sw/BUILD/O2Physics-latest/O2Physics/
cmake .
ninja install stage/bin/o2physics-analysistutorial-pid-with-onnx
```
   Known issues:
   - `Could not find PythonLibs` --> install `python3-dev` (Ubuntu) or `python3-devel` (CentOS)

3. Enter O2: `alienv enter O2Physics/latest` or `alienv load O2Physics/latest`
4. Run the task: `o2physics-analysistutorial-pid-with-onnx --aod-file <some_input_AOD> -b`

The model outputs are saved to the `results` histogram in `AnalysisResults.root`.

Most important parts of the analysis code:
- lines 23-35: setting up the ONNX session
- lines 79-80: putting tracks data as ONNX input
- line 92: applying the model
- lines 102-106: saving the outputs to a histogram
