# MAMMAL_mouse 数据结构文档

## 目录

1. [数据文件概览](#1-数据文件概览)
2. [mouse_model/ 模型数据](#2-mouse_model-模型数据)
3. [mouse_txt/ 模型参数详解](#3-mouse_txt-模型参数详解)
4. [DANNCE数据集结构](#4-dannce数据集结构)
5. [输出数据结构](#5-输出数据结构)
6. [关键点映射](#6-关键点映射)

---

## 1. 数据文件概览

### 1.1 项目包含的数据类型

| 类型 | 格式 | 位置 | 用途 |
|------|------|------|------|
| 3D模型 | .pkl, .obj, .txt | mouse_model/ | 小鼠网格模型及参数 |
| 关键点映射 | .json | mouse_model/ | 22关键点到顶点的映射 |
| 视频数据 | .mp4 | data/ | 多视角去畸变视频 |
| 分割掩码 | .mp4 | data/ | SimpleClick分割结果 |
| 相机参数 | .pkl | data/ | 相机内外参数 |
| 姿态结果 | .pkl | data/ & output | 估计的3D姿态 |

---

## 2. mouse_model/ 模型数据

### 2.1 mouse.pkl

**文件**: `mouse_model/mouse.pkl`  
**大小**: ~2.4 MB  
**类型**: Python pickle 序列化对象  
**加载方式**:
```python
import pickle
with open('mouse_model/mouse.pkl', 'rb') as f:
    params = pickle.load(f)
```

**数据结构**:

| 键名 | 类型 | 形状 | 说明 |
|------|------|------|------|
| vertices | numpy.ndarray | (N, 3) | 网格顶点坐标 (T-pose) |
| t_pose_joints | numpy.ndarray | (J, 3) | T-pose关节位置 (140个关节) |
| skinning_weights | scipy.sparse | (V, J) | 稀疏蒙皮权重矩阵 |
| parents | numpy.ndarray | (J,) | 父关节索引 (-1表示根) |
| faces_vert | numpy.ndarray | (F, 3) | 网格面顶点索引 |
| faces_tex | numpy.ndarray | (F, 3) | 纹理坐标面索引 |
| textures | numpy.ndarray | (T, 2) | 纹理坐标 |

### 2.2 mouse_reduced_face_*.obj

**文件**: 
- `mouse_model/mouse_reduced_face_1800.obj` (~300KB)
- `mouse_model/mouse_reduced_face_3600.obj` (~600KB)
- `mouse_model/mouse_reduced_face_7200.obj` (~1.2MB)

**类型**: Wavefront OBJ 3D网格文件  
**用途**: 不同细节层次的3D网格，用于渲染

**文件格式**:
```
# 顶点
v x y z
v x y z
...

# 法线
vn nx ny nz
...

# 纹理坐标
vt u v
...

# 面 (顶点索引/纹理索引/法线索引)
f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3
...
```

### 2.3 keypoint22_mapper.json

**文件**: `mouse_model/keypoint22_mapper.json`  
**类型**: JSON  
**用途**: 定义22个关键点到3D模型顶点/关节的映射

**结构**:
```json
{
    "mapper": [
        {
            "keypoint": 0,           // 关键点索引 (0-21)
            "type": "V",             // 类型: V=顶点, J=关节
            "ids": [12274, 12225]   // 对应的顶点ID或关节ID列表
        },
        ...
    ]
}
```

**关键点定义** (来自 mouse_22_defs.py):

| ID | 名称 | 英文名 | 类型 |
|----|------|--------|------|
| 0 | 左耳尖 | left_ear_tip | V |
| 1 | 右耳尖 | right_ear_tip | V |
| 2 | 鼻子 | nose | V |
| 3 | 颈部 | neck | J |
| 4 | 身体中部 | body_middle | V |
| 5 | 尾巴根部 | tail_root | J |
| 6 | 尾巴中部 | tail_middle | V |
| 7 | 尾巴末端 | tail_end | V |
| 8 | 左前爪 | left_paw | V |
| 9 | 左前爪尖 | left_paw_end | V |
| 10 | 左肘 | left_elbow | V |
| 11 | 左肩 | left_shoulder | V |
| 12 | 右前爪 | right_paw | V |
| 13 | 右前爪尖 | right_paw_end | V |
| 14 | 右肘 | right_elbow | V |
| 15 | 右肩 | right_shoulder | V |
| 16 | 左后脚 | left_foot | V |
| 17 | 左膝 | left_knee | V |
| 18 | 左髋 | left_hip | V |
| 19 | 右后脚 | right_foot | V |
| 20 | 右膝 | right_knee | V |
| 21 | 右髋 | right_hip | V |

---

## 3. mouse_txt/ 模型参数详解

### 3.1 vertices.txt

**文件**: `mouse_model/mouse_txt/vertices.txt`  
**类型**: 文本 (空格分隔)  
**行数**: N行 (顶点数量)

**格式**:
```
x1 y1 z1
x2 y2 z2
...
xN yN zN
```

**说明**: T-pose状态下的网格顶点坐标，每行一个顶点 (x, y, z)

### 3.2 t_pose_joints.txt

**文件**: `mouse_model/mouse_txt/t_pose_joints.txt`  
**类型**: 文本  
**行数**: 140行 (关节数量)

**格式**:
```
x1 y1 z1
x2 y2 z2
...
x140 y140 z140
```

**说明**: T-pose状态下140个关节的3D位置

### 3.3 joint_names.txt

**文件**: `mouse_model/mouse_txt/joint_names.txt`  
**类型**: 文本  
**行数**: 140行

**内容** (部分):
```
root
lumbar_vertebrae_1
perlvis_l
femur_l
tibia_l
hind_paw_l
...
skull
ear_r
ear_tip_r
ear_l
ear_tip_l
snout
...
```

**说明**: 每个关节的名称，按索引顺序排列

### 3.4 parents.txt / parents.pkl

**文件**: `mouse_model/mouse_txt/parents.txt`  
**类型**: 文本/ pickle  
**行数**: 140行

**格式**:
```
-1   # 根节点 (root)，无父节点
0    # 第二个关节的父节点是root (索引0)
1    # 第三个关节的父节点是索引1
...
```

**说明**: 关节层级关系，每个值表示父关节的索引 (-1表示根)

### 3.5 skinning_weights.txt

**文件**: `mouse_model/mouse_txt/skinning_weights.txt`  
**类型**: 文本  
**格式**: 稀疏矩阵表示

**说明**: 每个顶点受各关节影响的权重，用于线性混合蒙皮 (LBS)

### 3.6 faces_vert.txt

**文件**: `mouse_model/mouse_txt/faces_vert.txt`  
**类型**: 文本  
**行数**: F行 (面数量)

**格式**:
```
v1 v2 v3
v1 v2 v3
...
```

**说明**: 每个面的三个顶点索引

### 3.7 reduced_ids_*.txt / reduced_face_*.txt

**文件**:
- `reduced_ids_1800.txt`, `reduced_ids_3600.txt`, `reduced_ids_7200.txt`
- `reduced_face_1800.txt`, `reduced_face_3600.txt`, `reduced_face_7200.txt`

**说明**: 简化网格的顶点ID和面索引，用于不同精度渲染

### 3.8 bone_length_mapper.txt

**文件**: `mouse_model/mouse_txt/bone_length_mapper.txt`  
**类型**: 文本

**说明**: 骨骼长度到关节索引的映射

### 3.9 init_joint_*.pkl

**文件**:
- `init_joint_euler.pkl` - 初始Euler角
- `init_joint_rot_mat.pkl` - 初始旋转矩阵
- `init_joint_rotvec.pkl` - 初始旋转向量
- `init_joint_trans.pkl` - 初始平移

**类型**: Python pickle  
**形状**: (J, 3) 或 (J, 3, 3) - 140个关节的参数

**说明**: 初始姿态参数

---

## 4. DANNCE数据集结构

### 4.1 预期数据目录

```
data/
└── markerless_mouse_1_nerf/
    ├── videos_undist/              # 去畸变视频
    │   ├── 0.mp4                   # 视角0
    │   ├── 1.mp4                   # 视角1
    │   ├── 2.mp4                   # 视角2
    │   ├── 3.mp4                   # 视角3
    │   ├── 4.mp4                   # 视角4
    │   └── 5.mp4                   # 视角5 (共6个视角)
    │
    ├── simpleclick_undist/         # SimpleClick分割掩码
    │   ├── 0.mp4
    │   ├── 1.mp4
    │   ├── 2.mp4
    │   ├── 3.mp4
    │   ├── 4.mp4
    │   └── 5.mp4
    │
    ├── new_cam.pkl                 # 相机参数
    │
    ├── new_keypoints.pkl          # 2D关键点检测结果
    │
    ├── poses/                      # 姿态估计结果
    │   ├── pose_000000.pkl
    │   ├── pose_000001.pkl
    │   └── ...
    │
    └── label_ids_mid.pkl          # 评估帧ID列表
```

### 4.2 new_cam.pkl

**文件**: `data/markerless_mouse_1_nerf/new_cam.pkl`  
**类型**: Python pickle (dict)

**结构**:
```python
{
    'cam_idx': [0, 1, 2, 3, 4, 5],           # 相机索引
    'R': [R0, R1, ..., R5],                  # 旋转矩阵列表 (6个)
    'T': [T0, T1, ..., T6],                  # 平移向量列表 (6个)
    'K': [K0, K1, ..., K5],                  # 相机内参矩阵 (6个)
    'dist': [d0, d1, ..., d5],               # 畸变系数 (6个)
    'frame_count': 18000,                    # 总帧数
    ...
}
```

**说明**: 6个视角相机的内外参数

### 4.3 pose_*.pkl (输入/输出姿态)

**文件**: `data/markerless_mouse_1_nerf/poses/pose_XXXXXX.pkl`  
**类型**: Python pickle (dict)

**结构** (来自 inspect_pkl_content.py):
```python
{
    'trans': numpy.ndarray,   # 平移向量 (3,)
    'poses': numpy.ndarray,   # 关节姿态 (140, 3) - Euler角或旋转向量
    'root_orient': numpy.ndarray,  # 根方向 (3,)
    'scale': float,           # 尺度因子
    ...
}
```

### 4.4 label_ids_mid.pkl

**文件**: `data/markerless_mouse_1_nerf/label_ids_mid.pkl`  
**类型**: Python pickle

**说明**: 用于评估的帧ID列表

---

## 5. 输出数据结构

### 5.1 拟合结果目录

```
mouse_fitting_result/
└── 20230628/                      # 日期目录 (由run.sh参数指定)
    ├── pose_000000.pkl           # 第0帧结果
    ├── pose_000001.pkl           # 第1帧结果
    ...
    └── pose_000009.pkl           # 第9帧结果 (由 --end 10 指定)
```

### 5.2 输出姿态文件结构

**文件**: `mouse_fitting_result/YYYYMMDD/pose_XXXXXX.pkl`

```python
{
    'trans': numpy.ndarray,       # 根节点平移 (3,) - 单位: mm
    'poses': numpy.ndarray,       # 关节角度 (140, 3) - Euler角 (radian)
    'root_orient': numpy.ndarray, # 根节点旋转 (3,) - Euler角
    'scale': float,              # 全局尺度
    'vertices': numpy.ndarray,   # 变形后的网格顶点 (N, 3)
    'joints': numpy.ndarray,     # 计算得到的关节位置 (140, 3)
    'confidence': float,         # 拟合置信度
    'loss': float,               # 最终损失值
    ...
}
```

---

## 6. 关键点映射

### 6.1 22关键点骨骼定义

**文件**: `mouse_22_defs.py`

```python
mouse_22_bones = [
    [0,2], [1,2],         # 左耳-颈部, 右耳-颈部
    [2,3],[3,4],[4,5],[5,6],[6,7],  # 鼻子-尾巴
    [8,9], [9,10], [10,11], [11,3],  # 左前肢
    [12,13], [13,14], [14,15], [15,3],  # 右前肢
    [16,17],[17,18],[18,5],  # 左后肢
    [19,20],[20,21],[21,5]   # 右后肢
]
```

### 6.2 颜色映射

**文件**: `colormaps/anliang_paper.txt`

每行一个RGB颜色 (0-255):
```
R G B
R G B
...
```

**用途**: 22关键点可视化时的颜色分配

### 6.3 评估用关键点

**文件**: `evaluate.py`

```python
keypoint_names_for_eval = [
    "Nose",     # 2
    "Tail",     # 7
    "LPaw",     # 8
    "RPaw",     # 12
    "LFoot",    # 16
    "RFoot",    # 19
    "LEar",     # 0
    "REar"      # 1
]
mapper = [2, 7, 8, 12, 16, 19, 0, 1]
```

---

## 数据流程图

```
输入数据
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  data/markerless_mouse_1_nerf/                              │
│  ├── videos_undist/*.mp4         (6视角视频)                │
│  ├── simpleclick_undist/*.mp4    (分割掩码)                 │
│  └── new_cam.pkl                 (相机参数)                 │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  fitter_articulation.py                                     │
│  1. 加载 mouse_model/mouse.pkl (3D模型)                     │
│  2. 加载 new_cam.pkl (相机参数)                             │
│  3. 加载 new_keypoints.pkl (2D关键点)                       │
│  4. L-BFGS优化: 最小化2D重投影误差                           │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
输出结果
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  mouse_fitting_result/YYYYMMDD/                             │
│  └── pose_*.pkl                                              │
│      ├── trans: 平移                                        │
│      ├── poses: 关节角度 (140,3)                            │
│      ├── vertices: 变形后网格                              │
│      └── joints: 关节位置                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 附录: 文件大小汇总

| 文件 | 大小 | 类型 |
|------|------|------|
| mouse.pkl | 2.4 MB | pickle |
| mouse_reduced_face_7200.obj | 1.2 MB | OBJ |
| mouse_reduced_face_3600.obj | 600 KB | OBJ |
| mouse_reduced_face_1800.obj | 300 KB | OBJ |
| vertices.txt | 1.1 MB | text |
| skinning_weights.txt | 720 KB | text |
| t_pose_joints.txt | 10 KB | text |
| parents.txt | 1 KB | text |
| joint_names.txt | 2 KB | text |
| keypoint22_mapper.json | 4 KB | JSON |

---
