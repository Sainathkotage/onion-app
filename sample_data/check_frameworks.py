import sys

for mod in ['ai_edge_litert', 'tflite_runtime', 'tensorflow', 'onnx', 'torch', 'torchvision']:
    try:
        m = __import__(mod)
        ver = getattr(m, '__version__', 'unknown')
        print(f'{mod}: available ({ver})')
    except ImportError as e:
        print(f'{mod}: NOT available ({e})')
