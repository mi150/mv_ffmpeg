# mv_ffmpeg

## 0. Environment

```OS ubuntu~18.04
   python 3.7
   ffmpeg version 4.4.1 Copyright (c) 2000-2021 the FFmpeg developers
   built with gcc 7 (Ubuntu 7.5.0-3ubuntu1~18.04)
   configuration: --enable-shared --disable-static

```

## 1. Install Instructions

运行代码前，请确保安装了```ffmpeg-4.4.1```，若没有，请执行：
1.通过https://git.ffmpeg.org/ffmpeg.git获取ffmpeg-4.4.1版本
2.依次执行以安装ffmpeg

   ```./configure --enable-shared --disable-static
   
   make -j8
   
   make install
   ```   

``` pip.....```

## 2. Run our code

现在，用次repo中的```h264_cabac.c```将```libavcodec```文件夹下的```h264_cabac.c```:

```cd/......```

编译：

```build```

执行：

```
    cd...
    ffmpeg.....
```
## 3. 
主要是对ffmpeg的h264_cabac.c文件进行修改；

在```h264_cabac.c```中```ff_h264_decode_mb_cabac```函数实现了对每个宏块的运动向量的解码；

主要在```const H264Context```和```H264SliceContext```结构体中保存了需要用到的信息：

    h->cur_pic_ptr->f->pkt_duration：时间基
    
    h->cur_pic_ptr->f->pts：时间基*帧号(播放顺序)
    
    sl->mb_x：宏块x坐标
    
    sl->mb_y：宏块y坐标
    
fprintf(fp, "time:%ld frame_num:%lld mb_xy:%d/%d \n",h->cur_pic_ptr->f->pkt_duration, h->cur_pic_ptr->f->pts,sl->mb_x, sl->mb_y);

输出了当前解码宏块帧号：h->cur_pic_ptr->f->pts/h->cur_pic_ptr->f->pkt_duration；宏块xy坐标(sl->mb_x, sl->mb_y)；

fprintf(fp, "list:%d mv:%d/%d ref:%d \n", list, mx, my, ref_l.poc - 65536);

输出了当前运动向量的参考方向：list：0/1；运动向量x，y方向的数值(mx,my)，为四分之一精度使用时要/4；以及该mv的POC：ref_l.poc - 65536，具体参考帧为 当前GOP I帧号+POC/2；

mv复用的流程为获取目标检测的bbox后，根据bbox位置获取检测帧的宏块，然后通过帧间参考关系利用运动向量将bbox移动到需要复用的帧上；

mv的去噪(python)：

    def clean(data_list):
        data_array = np.asarray(data_list)
        if len(data_list)>5:
            data_array=data_array[data_array != 0]
            if data_array.shape[0]==0:
                return data_array
            mean = np.mean(data_array, axis=0)
            std = np.std(data_array, axis=0)
            preprocessed_data_array = [x for x in data_array if (x > mean - 0.8 * std)]
            preprocessed_data_array = [x for x in preprocessed_data_array if (x < mean + 0.8 * std)]
            return preprocessed_data_array
        return data_array
