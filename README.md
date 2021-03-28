# PID ML in O2

Porting Python PID ML codes to C++ O2.

## Python API - train + apply

1. Load new environment: `source load.sh`
2. Install all packages: `pip install -e .`
3. Open the notebook: `python -m notebook Simple_example.ipynb`
4. To quit the environment, type again `source load.sh`.

`source load.sh --recreate` creates a new, fresh environment.

## C++ API - apply

1. Pre-build with CMake. Use your system CMake if you have version >= 3.17 or borrow one from O2:
```
<path_to_alice>/sw/ubuntu1804_x86-64/CMake/<o2_version>/bin/cmake .
```
2. Build with make.
3. Run: `./pid-in-o2 <path_to_model_file>`
