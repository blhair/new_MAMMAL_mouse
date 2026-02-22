import os
import sys
import pickle
import torch
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse
from articulation_th import ArticulationTorch

def visualize_pose(input_val, output_file):
    # Determine input type
    if os.path.isfile(input_val):
        pose_file = input_val
        print(f"Using provided file path: {pose_file}")
    else:
        try:
            idx = int(input_val)
            pose_file = f"data/markerless_mouse_1_nerf/poses/pose_{idx:06d}.pkl"
            print(f"Using pose index {idx}, constructed path: {pose_file}")
        except ValueError:
            print(f"Error: Input '{input_val}' is neither a file path nor an integer index.")
            return

    if not os.path.exists(pose_file):
        print(f"Error: Pose file {pose_file} not found.")
        return

    print(f"Loading pose from {pose_file}...")
    with open(pose_file, 'rb') as f:
        pose_data = pickle.load(f)

    # Initialize model
    print("Initializing ArticulationTorch model...")
    # Ensure we are in the correct directory for relative paths in ArticulationTorch to work
    # We assume the script is run from MAMMAL_mouse directory
    
    try:
        model = ArticulationTorch()
    except Exception as e:
        print(f"Failed to initialize model: {e}")
        # Try to fix path issue if running from wrong dir?
        # But let's assume correct dir first.
        return

    device = model.device # Should be cuda if available

    # Prepare input tensors
    batch_size = 1
    
    # Extract data and convert to tensors
    # Keys: 'thetas', 'trans', 'scale', 'rotation', 'bone_lengths', 'chest_deformer'
    
    def to_tensor_dev(arr):
        if torch.is_tensor(arr):
            return arr.to(device)
        return torch.tensor(arr, dtype=torch.float32, device=device)

    thetas = to_tensor_dev(pose_data['thetas'])
    trans = to_tensor_dev(pose_data['trans'])
    scale = to_tensor_dev(pose_data['scale'])
    rotation = to_tensor_dev(pose_data['rotation']) # rotation vector (axis-angle)? or euler?
    # Inspecting ArticulationTorch.forward:
    # forward(self, thetas, bone_lengths_core, R, T, s, chest_deformer)
    # R is expected to be [batch, 3], logical to be axis-angle or euler depending on config.
    # In fitter_articulation.py, init_params uses "rotation" as np.zeros([batch, 3]).
    
    bone_lengths = to_tensor_dev(pose_data['bone_lengths']) # This might be bone_lengths_core
    chest_deformer = to_tensor_dev(pose_data['chest_deformer'])

    # ArticulationTorch forward signature:
    # V, J = A.forward(thetas, bone_lengths_core, R, T, s, chest_deformer)
    
    # Check shapes
    if len(thetas.shape) == 2: thetas = thetas.unsqueeze(0)
    if len(rotation.shape) == 1: rotation = rotation.unsqueeze(0)
    if len(trans.shape) == 1: trans = trans.unsqueeze(0)
    if len(scale.shape) == 1: scale = scale.unsqueeze(0)
    if len(chest_deformer.shape) == 1: chest_deformer = chest_deformer.unsqueeze(0)
    if len(bone_lengths.shape) == 1: bone_lengths = bone_lengths.unsqueeze(0)
    # Note: bone_lengths in pkl might be 20 dims, but forward expects bone_lengths_core which is used to scale bones.
    # In ArticulationTorch.forward: bone_lengths_core: [batchsize, ?] (used as index into bone_length_mapper)
    # Let's hope the size matches.
    
    print("Running model forward pass...")
    with torch.no_grad():
        V, J = model.forward(
            thetas=thetas,
            bone_lengths_core=bone_lengths,
            R=rotation,
            T=trans,
            s=scale,
            chest_deformer=chest_deformer
        )

    # Move to CPU for plotting
    V_np = V.cpu().numpy().squeeze()
    J_np = J.cpu().numpy().squeeze()

    print(f"Vertices shape: {V_np.shape}")
    print(f"Joints shape: {J_np.shape}")

    # Visualization
    print("Generating visualization...")
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Plot Joints
    ax.scatter(J_np[:, 0], J_np[:, 1], J_np[:, 2], c='r', marker='o', s=20, label='Joints')

    # Plot a subsample of vertices for better performance and visibility
    # Step 10
    ax.scatter(V_np[::20, 0], V_np[::20, 1], V_np[::20, 2], c='b', s=1, alpha=0.3, label='Vertices (Subsampled)')
    
    # Draw bones? 
    # Need parent info.
    parents = model.parents # list
    for i, p in enumerate(parents):
        if p != -1 and i < len(J_np) and p < len(J_np):
            ax.plot([J_np[i, 0], J_np[p, 0]], 
                    [J_np[i, 1], J_np[p, 1]], 
                    [J_np[i, 2], J_np[p, 2]], 'k-', lw=1)

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Mouse Pose {pose_idx}')
    
    # Equal aspect ratio hack for 3D
    # Get limits
    x_lim = ax.get_xlim()
    y_lim = ax.get_ylim()
    z_lim = ax.get_zlim()
    
    # Calculate ranges
    x_range = x_lim[1] - x_lim[0]
    y_range = y_lim[1] - y_lim[0]
    z_range = z_lim[1] - z_lim[0]
    
    max_range = max(x_range, y_range, z_range)
    
    mid_x = (x_lim[0] + x_lim[1]) * 0.5
    mid_y = (y_lim[0] + y_lim[1]) * 0.5
    mid_z = (z_lim[0] + z_lim[1]) * 0.5
    
    ax.set_xlim(mid_x - max_range * 0.5, mid_x + max_range * 0.5)
    ax.set_ylim(mid_y - max_range * 0.5, mid_y + max_range * 0.5)
    ax.set_zlim(mid_z - max_range * 0.5, mid_z + max_range * 0.5)

    plt.legend()
    plt.savefig(output_file)
    print(f"Visualization saved to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize mouse pose from pkl file')
    parser.add_argument('input', help='Pose index (int) or path to pkl file')
    parser.add_argument('--output', '-o', default='pose_visualization.png', help='Output image file')
    
    args = parser.parse_args()
    visualize_pose(args.input, args.output)
