# mv_ffmpeg

## 0. Environment

```OS ubuntu~18.04
   python 3.7
   ffmpeg version 4.4.1 Copyright (c) 2000-2021 the FFmpeg developers
   built with gcc 7 (Ubuntu 7.5.0-3ubuntu1~18.04)
   configuration: --enable-shared --disable-static

```
需要安装imutils和cv2库
## 1. Install Instructions

运行代码前，请确保安装了```ffmpeg-4.4.1```，若没有，请执行：

1.通过https://git.ffmpeg.org/ffmpeg.git  获取ffmpeg-4.4.1版本(或其他4.4版本)

2.依次执行以安装ffmpeg

   ```
   cd ffmpeg-4.4.1
   ./configure --enable-shared --disable-static
   make -j8
   make install
   ```   


## 2. Run our code

现在，用次repo中的```h264_cabac.c```将```libavcodec```文件夹下的```h264_cabac.c```:

```cd ffmpeg-4.4.1```

编译：

```
make
make install
```

执行：

```
    ffmpeg -c:v h264 -i input.mp4 -f null - 
```

随后，在执行指令的文件夹中获得```mv.txt```文件保存了所有帧的运动向量信息；

## 3. Detection

使用任意目标检测模型对```input.mp4```进行检测，检测结果保存在```results```csv文件中。

## 4. MV-based shift

获取```mv.txt```文件后，并获取到检测结果```results```csv文件，将检测结果重定义为```dds_utils.py```中```Region```结构，运行```process_results.py```文件对结果进行复用并将最终结果保存为```final_results```csv文件。
```
class Region:
    def __init__(self, fid, x, y, w, h, conf, label, resolution,
                 origin="generic"):
        self.fid = int(fid)
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)
        self.conf = float(conf)
        self.label = label
        self.resolution = float(resolution)
        self.origin = origin
```

## 5. Visualization

将原结果```results```和复用后的```final_results```作为```visual.py```文件的```nomv_filename```和```filename```变量，执行后可以得到可视化视频文件，如该repo中的```demo.mp4```。
下列图片中，绿色框是按业务流程每秒一帧的检测结果，蓝色框是MV-based的追踪结果：
![an image is a 3d matrix RGB](/0000000125.png "An image is a 3D matrix")
![an image is a 3d matrix RGB](/0000000151.png "An image is a 3D matrix")
![an image is a 3d matrix RGB](/0000000155.png "An image is a 3D matrix")
![an image is a 3d matrix RGB](/0000000177.png "An image is a 3D matrix")

