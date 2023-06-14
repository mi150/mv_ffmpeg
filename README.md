# mv_ffmpeg
主要是对ffmpeg的h264_cabac.c文件进行修改；

在h264_cabac.c中ff_h264_decode_mb_cabac函数实现了对每个宏块的运动向量的解码；

主要在const H264Context *h和H264SliceContext *sl结构体中保存了需要用到的信息：

    h->cur_pic_ptr->f->pkt_duration：时间基
    
    h->cur_pic_ptr->f->pts：时间基*帧号(播放顺序)
    
    sl->mb_x：宏块x坐标
    
    sl->mb_y：宏块y坐标
    
fprintf(fp, "time:%ld frame_num:%lld mb_xy:%d/%d \n",h->cur_pic_ptr->f->pkt_duration, h->cur_pic_ptr->f->pts,sl->mb_x, sl->mb_y);

输出了当前解码宏块帧号：h->cur_pic_ptr->f->pts/h->cur_pic_ptr->f->pkt_duration；宏块xy坐标(sl->mb_x, sl->mb_y)；

fprintf(fp, "list:%d mv:%d/%d ref:%d \n", list, mx, my, ref_l.poc - 65536);

输出了当前运动向量的参考方向：list：0/1；运动向量x，y方向的数值(mx,my)，为四分之一精度使用时要/4；以及该mv的POC：ref_l.poc - 65536，具体参考帧为 当前GOP I帧号+POC/2；

mv的去噪：

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
