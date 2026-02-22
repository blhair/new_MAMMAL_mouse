# MAMMAL_mouse
This is the sub project of the manuscript _Three-dimensional surface motion capture of multiple freely moving pigs using MAMMAL_ (unpublished). By running `run.sh`, we fit the an articulated mouse model to the `markerless_mouse_1` sequence proposed by [DANNCE](https://github.com/tqxli/dannce-pytorch) paper. 

Here is the model we used. The model was extracted from the blender file `C57BL6_Female_V1.2_opensource-file.blend` proposed by _A three-dimensional virtual mouse generates synthetic training data for behavioral analysis_. 

![mouse_model](figs/mouse_1.png)

Here is a comparison between DANNCE and MAMMAL_mouse. The DANNCE-T model was the temporal version of DANNCE (https://github.com/tqxli/dannce-pytorch). The results were generated from the pretrained model provided by the original project. 

![mouse_model2](figs/mouse_2.png)

## Environment
We recommend to use Anaconda to configure the environment. 

1. We assume that you have installed anaconda. Create a virtual environment as 
```
conda create -n mouse python=3.9
conda activate mouse
```
2. Install pytorch as 
```
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
```
3. Install other libraries as 
```
pip install -r requirements.txt
```
4. Install pytorch3d 
```
conda install -c fvcore -c iopath -c conda-forge fvcore iopath
conda install -c bottler nvidiacub
conda install jupyter
pip install black usort flake8 flake8-bugbear flake8-comprehensions
conda install pytorch3d -c pytorch3d
```
## Download markerless_mouse_1 
To run the code, please download the preprocessed `markerless_mouse_1` sequence `data.zip` from [google drive](https://drive.google.com/file/d/1NbaIFOvpvQ_WLOabUtMrVHS7vVBq-8zD/view?usp=sharing). Then, unzip the `data.zip` to `data/` under this directory. `data/` contains the undistorted videos, detected 2D keypoints and silhouettes produced by [SimpleClick](https://github.com/uncbiag/SimpleClick) software. 

## Run the code 
Use `bash run.sh` to run the code. It may take about 7min to process one frame when "WITH_RENDER=True" (in `fitter_articulation.py`). 
The results are saved at `mouse_fitting_result/`. 

## Citation 
If you found this project insightful to your own work, please cite the papers: 


```BibTex
@article{MAMMAL, 
    author = {An, Liang and Ren, Jilong and Yu, Tao and Hai, Tang and Jia, Yichang and Liu, Yebin},
    title = {Three-dimensional surface motion capture of multiple freely moving pigs using MAMMAL},
    journal = {},
    year = {2023}
}
```
and 
```BibTex
@article{bolanos2021three,
  title={A three-dimensional virtual mouse generates synthetic training data for behavioral analysis},
  author={Bola{\~n}os, Luis A and Xiao, Dongsheng and Ford, Nancy L and LeDue, Jeff M and Gupta, Pankaj K and Doebeli, Carlos and Hu, Hao and Rhodin, Helge and Murphy, Timothy H},
  journal={Nature methods},
  volume={18},
  number={4},
  pages={378--381},
  year={2021},
  publisher={Nature Publishing Group US New York}
}
```

## Contact
If you find any problems about using the code, do not hesitate to propose an issue. I will reply as soon as possible. 


以下是该项目 README 文件的中文翻译：

---

# MAMMAL_mouse
这是论文《使用 MAMMAL 对多只自由运动的猪进行三维表面动作捕捉》（*Three-dimensional surface motion capture of multiple freely moving pigs using MAMMAL*，待发表）的一个子项目。通过运行 `run.sh`，我们可以将一个铰接式小鼠模型拟合到 [DANNCE](https://github.com/tqxli/dannce-pytorch) 论文中提出的 `markerless_mouse_1` 序列上。

这是我们使用的模型。该模型提取自《三维虚拟小鼠为行为分析生成合成训练数据》（*A three-dimensional virtual mouse generates synthetic training data for behavioral analysis*）一文提供的 Blender 文件 `C57BL6_Female_V1.2_opensource-file.blend`。

![mouse_model](figs/mouse_1.png)

以下是 DANNCE 和 MAMMAL_mouse 的对比。其中 DANNCE-T 模型是 DANNCE 的时序版本（https://github.com/tqxli/dannce-pytorch ）。结果是使用原项目提供的预训练模型生成的。

![mouse_model2](figs/mouse_2.png)

## 环境配置
建议使用 Anaconda 来配置环境。

1. 假设你已经安装了 Anaconda。按如下方式创建虚拟环境：
```bash
conda create -n mouse python=3.9
conda activate mouse
```
2. 安装 PyTorch：
```bash
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
```
3. 安装其他依赖库：
```bash
pip install -r requirements.txt
```
4. 安装 PyTorch3D：
```bash
conda install -c fvcore -c iopath -c conda-forge fvcore iopath
conda install -c bottler nvidiacub
conda install jupyter
pip install black usort flake8 flake8-bugbear flake8-comprehensions
conda install pytorch3d -c pytorch3d
```

## 下载 markerless_mouse_1 数据
要运行代码，请从 [Google Drive](https://drive.google.com/file/d/1NbaIFOvpvQ_WLOabUtMrVHS7vVBq-8zD/view?usp=sharing) 下载预处理好的 `markerless_mouse_1` 序列文件 `data.zip`。然后，将 `data.zip` 解压缩到当前目录下的 `data/` 文件夹中。`data/` 文件夹内包含：去畸变后的视频、检测到的 2D 关键点，以及由 [SimpleClick](https://github.com/uncbiag/SimpleClick) 软件生成的轮廓（silhouettes）。

## 运行代码
使用 `bash run.sh` 运行代码。如果在 `fitter_articulation.py` 中设置了 `WITH_RENDER=True`，处理一帧图像大约需要 7 分钟。
结果将保存在 `mouse_fitting_result/` 目录下。

## 引用
如果你发现本项目对你的研究有所启发，请引用以下论文：

```BibTex
@article{MAMMAL, 
    author = {An, Liang and Ren, Jilong and Yu, Tao and Hai, Tang and Jia, Yichang and Liu, Yebin},
    title = {Three-dimensional surface motion capture of multiple freely moving pigs using MAMMAL},
    journal = {},
    year = {2023}
}
```

以及：

```BibTex
@article{bolanos2021three,
  title={A three-dimensional virtual mouse generates synthetic training data for behavioral analysis},
  author={Bola{\~n}os, Luis A and Xiao, Dongsheng and Ford, Nancy L and LeDue, Jeff M and Gupta, Pankaj K and Doebeli, Carlos and Hu, Hao and Rhodin, Helge and Murphy, Timothy H},
  journal={Nature methods},
  volume={18},
  number={4},
  pages={378--381},
  year={2021},
  publisher={Nature Publishing Group US New York}
}
```

## 联系方式
如果你在使用代码时遇到任何问题，请随时提出 Issue。我会尽快回复。