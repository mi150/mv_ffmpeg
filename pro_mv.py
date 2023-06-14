import numpy as np
import pickle


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

def move_bbox(frame_id,x,y,w,h,refer):
    MV = all_mv[frame_id - 1]
    x0, y0, x1, y1 = getmblist(x, y, w, h)
    x=[]
    y=[]
    if x0==x1:
        x1+=1
    if y0==y1:
        y1+=1
    for i in range(x0, x1, 1):
        for j in range(y0, y1, 1):
            if MV[i][j][0][2]==refer:
                x.append(MV[i][j][0][0])
                y.append(MV[i][j][0][1])
    x=clean(x)
    y=clean(y)
    if len(x)==0 or len(y)==0:
        return 0,0
    return sum(x)/len(x),sum(y)/len(y)

def move_re_bbox(frame_id,x,y,w,h,refer):
    MV = all_mv[frame_id - 1]
    x0, y0, x1, y1 = getmblist(x, y, w, h)
    x=[]
    y=[]
    if x0==x1:
        x1+=1
    if y0==y1:
        y1+=1
    for i in range(x0, x1, 1):
        for j in range(y0, y1, 1):
            if MV[i][j][1][2]==frame_id:
                x.append(MV[i][j][1][0])
                y.append(MV[i][j][1][1])

    x=clean(x)
    y=clean(y)
    if len(x)==0 or len(y)==0:
        return 0,0

    return sum(x)/len(x),sum(y)/len(y)

