# MAMMAL_mouse 项目结构文档 (project_map)

## 项目概述

- **项目名称**: MAMMAL_mouse
- **项目类型**: Python 3D计算机视觉 / 姿态估计 / 动作捕捉
- **编程语言**: Python 3.9
- **核心框架**: PyTorch, PyTorch3D, OpenCV, pyrender
- **项目用途**: 将3D铰接式小鼠模型拟合到多视图视频数据，实现无标记运动捕捉

---

## 目录结构

```
new_MAMMAL_mouse\
├── .git/                              # Git版本控制
│
├── .gitignore                         # Git忽略配置
│
├── .opencode/                         # OpenCode工具配置
│   ├── agents/
│   │   └── project_explorer.md       # 项目分析Agent配置
│   └── prompts/
│       └── project_explorer.txt      # 项目Explorer提示词
│
├── colormaps/                         # 可视化颜色配置
│   ├── anliang_blend.txt             # 混合颜色映射 (RGB)
│   ├── anliang_paper.txt            # 论文配色 (RGB)
│   ├── anliang_render.txt           # 渲染配色 (RGB)
│   └── anliang_rgb.txt              # RGB颜色定义
│
├── mouse_model/                      # 3D小鼠模型数据 (核心)
│   ├── bone_length_name.txt          # 骨骼长度名称映射
│   ├── keypoint22_mapper.json       # 22关键点映射配置
│   ├── mouse.pkl                     # 序列化的小鼠模型 (PyTorch)
│   ├── mouse_reduced_face_1800.obj  # 简化网格 (1800面)
│   ├── mouse_reduced_face_3600.obj  # 简化网格 (3600面)
│   ├── mouse_reduced_face_7200.obj  # 简化网格 (7200面)
│   ├── reg_weights.txt               # 正则化权重
│   │
│   └── mouse_txt/                    # 模型参数文本格式
│       ├── bone_length_mapper.txt    # 骨骼长度索引映射
│       ├── faces_vert.txt            # 网格面顶点索引
│       ├── faces_tex.txt             # 纹理坐标面索引
│       ├── id_to_names.pkl           # ID到名称映射
│       ├── init_joint_euler.pkl      # 初始关节Euler角
│       ├── init_joint_rot_mat.pkl    # 初始关节旋转矩阵
│       ├── init_joint_rotvec.pkl     # 初始关节旋转向量
│       ├── init_joint_trans.pkl      # 初始关节平移
│       ├── joint_names.txt           # 关节名称列表 (140个关节)
│       ├── names_to_id.pkl           # 名称到ID映射
│       ├── parents.pkl               # 父关节索引 (pickle)
│       ├── parents.txt               # 父关节索引 (文本)
│       ├── reduced_face_*.txt        # 简化网格面数据
│       ├── reduced_ids_*.txt        # 简化网格顶点ID
│       ├── skinning_weights.txt      # 蒙皮权重
│       ├── t_pose_joints.txt         # T-pose关节位置
│       ├── textures.txt              # 纹理坐标
│       └── vertices.txt              # 网格顶点坐标
│
├── 源代码文件 (根目录)
│   ├── fitter_articulation.py        # ★ 主入口 - 模型拟合算法
│   ├── bodymodel_th.py               # PyTorch身体模型实现
│   ├── bodymodel_np.py               # NumPy身体模型实现
│   ├── articulation_th.py             # 铰接/蒙皮处理 (PyTorch)
│   ├── data_seaker_video_new.py      # DANNCE数据加载器
│   ├── evaluate.py                   # 评估指标计算
│   ├── visualize_pose.py             # 姿态3D可视化
│   ├── visualize_DANNCE.py          # DANNCE结果可视化
│   ├── utils.py                      # 通用工具函数
│   ├── mouse_22_defs.py             # 22关键点定义
│   └── inspect_pkl_content.py       # PKL文件调试工具
│
├── 配置与运行
│   ├── README.md                      # 项目说明 (中英双语)
│   ├── requirements.txt               # Python依赖列表
│   ├── run.sh                        # 运行脚本
│   └── opencode.json                 # OpenCode配置
│
├── 预期运行时目录 (需下载)
│   ├── data/                         # 输入数据目录
│   │   └── markerless_mouse_1_nerf/ # DANNCE小鼠数据序列
│   │       ├── videos_undist/        # 去畸变视频 (6个视角)
│   │       ├── simpleclick_undist/   # 分割mask视频
│   │       ├── new_cam.pkl          # 相机参数
│   │       ├── poses/               # 姿态估计结果
│   │       └── label_ids_mid.pkl    # 评估帧ID
│   │
│   └── mouse_fitting_result/          # 拟合结果输出目录
│       └── *.pkl                     # 每帧的姿态参数
│
└── figs/                            # 文档图片 (未包含在仓库中)
    ├── mouse_1.png                  # 小鼠模型图
    └── mouse_2.png                  # 对比图
```

---

## 文件类型分类

### Python源代码 (.py)
| 文件 | 类型 | 功能描述 |
|------|------|----------|
| fitter_articulation.py | **主入口** | 3D模型拟合算法，优化关节参数 |
| bodymodel_th.py | 核心模块 | PyTorch版身体模型，支持蒙皮 |
| bodymodel_np.py | 核心模块 | NumPy版身体模型，用于快速计算 |
| articulation_th.py | 核心模块 | 铰接和蒙皮处理实现 |
| data_seaker_video_new.py | 数据模块 | 加载DANNCE数据集 |
| evaluate.py | 工具模块 | 计算评估指标 (MPJPE等) |
| visualize_pose.py | 工具模块 | 3D姿态可视化 |
| visualize_DANNCE.py | 工具模块 | DANNCE结果可视化 |
| utils.py | 工具模块 | 颜色映射、骨骼定义等工具 |
| mouse_22_defs.py | 定义模块 | 22关键点名称和骨骼定义 |
| inspect_pkl_content.py | 调试工具 | 查看pickle文件内容 |

### 数据文件 (.pkl, .txt, .json)
| 文件 | 格式 | 用途 |
|------|------|------|
| mouse.pkl | pickle | 序列化的小鼠3D模型 |
| mouse_model/*.pkl | pickle | 各类初始化参数 |
| mouse_model/*.txt | text | 模型参数文本格式 |
| keypoint22_mapper.json | JSON | 22关键点到顶点的映射 |
| colormaps/*.txt | text | 可视化颜色配置 |

### 3D模型文件 (.obj)
| 文件 | 描述 |
|------|------|
| mouse_reduced_face_1800.obj | 低分辨率网格 (1800面) |
| mouse_reduced_face_3600.obj | 中分辨率网格 (3600面) |
| mouse_reduced_face_7200.obj | 高分辨率网格 (7200面) |

### 配置文件
| 文件 | 用途 |
|------|------|
| requirements.txt | Python包依赖 |
| run.sh | 批处理运行脚本 |
| README.md | 项目说明文档 |

---

## 入口点与运行流程

### 主入口
```bash
bash run.sh
# 等价于:
python fitter_articulation.py --start 0 --end 10 --date 20230628
```

### 运行流程
```
run.sh
  └─> fitter_articulation.py (主拟合器)
        ├─> bodymodel_th.py (加载3D模型)
        ├─> data_seaker_video_new.py (加载视频/关键点)
        ├─> articulation_th.py (蒙皮计算)
        └─> 优化循环
              ├─> 计算3D姿态
              ├─> 渲染可视化 (可选 WITH_RENDER=True)
              └─> 保存结果到 mouse_fitting_result/
```

---

## 依赖关系图

```
fitter_articulation.py
├── articulation_th.py        # 铰接计算
├── bodymodel_th.py          # 身体模型
├── data_seaker_video_new.py # 数据加载
├── utils.py                  # 工具函数
├── bodymodel_np.py          # NumPy模型
├── pyrender                 # 3D渲染
├── pytorch3d                # PyTorch 3D
└── opencv-python           # 图像处理

evaluate.py
├── scipy, numpy, matplotlib
└── seaborn, pandas

visualize_pose.py
├── articulation_th.py
├── matplotlib
└── mpl_toolkits.mplot3d

visualize_DANNCE.py
├── glfw, OpenGL           # OpenGL渲染
├── pyrender
├── cv2
└── videoio
```

---

## 关键配置参数

### fitter_articulation.py
```python
WITH_RENDER = False          # 是否启用渲染 (影响速度)
KEYPOINT_NUM = 22            # 关键点数量
RENDER_CAMERAS = [0,1,2,3,4,5]  # 使用的相机视角
```

### 运行参数
```bash
--start 0      # 起始帧
--end 10        # 结束帧
--date 20230628 # 结果保存日期目录
```

---

## 小鼠模型关节结构 (140个关节)

骨骼层级结构，包含:
- **脊柱**: lumbar_vertebrae (腰部椎骨), thoracic_vertebrae (胸部椎骨), cervical_vertebrae (颈部椎骨)
- **头部**: skull, snout, ear_l/r, mandible, tongue
- **前肢**: scapula, humerus, ulna, fore_paw (左/右)
- **后肢**: perlvis, femur, tibia, hind_paw (左/右)
- **尾巴**: tail_0 ~ tail_9 (10段)
- **胸部**: chest, belly_stretch

---

*文档生成时间: 2026-02-22*
