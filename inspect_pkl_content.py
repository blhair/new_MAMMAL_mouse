import pickle
import numpy as np
import sys

# Load the pickle file
file_path = "/root/new_moremouse/new_moremouse/MAMMAL_mouse/data/markerless_mouse_1_nerf/poses/pose_000000.pkl"

try:
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    
    print(f"Data type: {type(data)}")
    if isinstance(data, dict):
        print("Keys:", data.keys())
        for key, value in data.items():
            print(f"Key: {key}")
            if hasattr(value, 'shape'):
                print(f"  Shape: {value.shape}")
                print(f"  Value: {value}")
            elif isinstance(value, list):
                print(f"  Length: {len(value)}")
                print(f"  Value: {value[:5]}...") # First 5 elements
            else:
                print(f"  Value: {value}")
    else:
        print(data)
except Exception as e:
    print(f"Error reading file: {e}")
