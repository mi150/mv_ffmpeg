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
后会获得mv.txt保存了所有帧的运动向量信息；

## 3. 


获取mv.txt文件后，并获取到检测结果results文件，将检测结果重定义为dds_utils.py中Region结构，运行process_results.py文件对结果进行复用并将最终结果保存为final_results。

将原结果results和复用后的final_results作为visual.py文件的nomv_filename和filename变量，执行后可以得到演示视频mp4文件。

