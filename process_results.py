from dds_utils import Region,Results
import numpy as np

def resize(r):
    if (r.x + r.w) > 1:
        r.w = 1 - r.x
    if (r.y + r.h) > 1:
        r.w = 1 - r.y
    r.x = max(0, r.x)
    r.y = max(0, r.y)
    r.h = max(0, r.h)
    r.w = max(0, r.w)
    r.x = min(1, r.x)
    r.y = min(1, r.y)
    return r


def process_mv(filename):
    def process_play_order(line,time_base):
        line=line.split(':')[-1]
        return int(int(line)/(time_base))
    #依赖关系
    #总帧数
    num_size=3000
    #文件位置
    f=open(filename)
    #poc列表，每帧的前和后依赖，按播放顺序排列,依赖帧播放顺序=I帧帧号+poc(加入list时已经除2)
    f_poc_list=[ [[],[]] for _ in range(num_size)]
    #解码顺序下每帧的播放顺序
    f_play_list=[ 0 for _ in range(num_size)]
    #解码顺序每帧的帧类型
    f_type_list=['' for _ in range(num_size)]

    block_x_len=0
    block_y_len=0
    ###初始化
    f_mv_list = [[[[ [],[] ] for _ in range(block_y_len)] for _ in range(block_x_len)] for _ in range(num_size)]

    gop=-1
    prev_line=[]
    f_num=-1
    mx,my=0,0
    #遍历文件
    for idx,line in enumerate(f):
        line=line.split()

        if "mb_type_I:" in line[0] and prev_line[-1]=="mb_xy:0/0":
            gop+=1
            #处理到第几个gop停止
            if gop == 2:
                break

        prev_line=line
        if gop==0:
            continue
        #process_mv
        if "mb_xy: "in line[-1]:
            mx,my=line[1][3:].split("/")

        if line[-1]=="mb_xy:0/0":
            f_num+=1
            f_type_list[f_num]=''
            time_base = int(line[0][5:])
            f_play_list[f_num]=process_play_order(line[1],f_num,time_base)
        elif "list" in line[0]:
            l_num=int(line[0][5:])
            ref=int(line[-1][4:])
            if int(ref/2) not in f_poc_list[f_play_list[f_num]][l_num]:
                f_poc_list[f_play_list[f_num]][l_num].append(int(ref/2))
            mvx,mvy=line[1][3:].split("/")
            ###保存mv
            f_mv_list[f_num][int(mx)][int(my)][l_num].append([int(mvx),int(mvy),ref])

        if "mb_type_B" in line[0]:
            f_type_list[f_num]="B"
        elif "mb_type_P" in line[0]:
            f_type_list[f_num]="P"
        elif "mb_type_I:" in line[0]:
            f_type_list[f_num] = "I"
    return f_mv_list,f_poc_list

def getmblist(x,y,w,h):
    x0 = int(x * width)
    y0 = int(y * height)
    x1 = int(w * width+x0)
    y1 = int((h * height) + y0)
    return min(79,int(x0/16)),min(44,int(y0/16)),min(79,int(x1/16)+1),min(44,int(y1/16)+1)


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

def move_re_bbox(frame_id,x,y,w,h):

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
def find_refer(frame_id):
    MV=all_mv[frame_id-1]
    x0,y0,x1,y1=getmblist(0,0,1,1)
    if x0==x1:
        x1+=1
    if y0==y1:
        y1+=1
    rl=np.zeros(len(r0l[frame_id-1]))
    rl=rl.tolist()
    for i in range(x0,x1,1):
        for j in range(y0,y1,1):
            if MV[i][j][0][2] in r0l[frame_id-1]:
                rl[r0l[frame_id-1].index(MV[i][j][0][2])]+=1
    if len(rl)==0:
        return -1
    return r0l[frame_id-1][rl.index(max(rl))]

def find_re_refer(frame_id):
    MV = all_mv[frame_id - 1]
    x0,y0,x1,y1=getmblist(0,0,1,1)
    if x0==x1:
        x1+=1
    if y0==y1:
        y1+=1
    rl=np.zeros(len(r1l[frame_id-1]))
    rl=rl.tolist()
    for i in range(x0,x1,1):
        for j in range(y0,y1,1):
            #print(MV[i][j])
            if MV[i][j][1][2] in r1l[frame_id-1]:
                rl[r1l[frame_id-1].index(MV[i][j][1][2])]+=1
    return r1l[frame_id-1][rl.index(max(rl))]


if __name__=="__main__":
    filename=""
    all_mv,poc=process_mv(filename)
    r0l, r1l=[i[0] for i in poc],[i[1] for i in poc]
    frame_length = 3000
    width = 1280
    height = 720
    s_frames = []
    result = []
    final_results = Results()
    for frame_idx in range(frame_length):
        # 检测过的帧
        if frame_idx in s_frames:
            for r in result[frame_idx]:
                label, conf, (x, y, w, h) = r.label, r.conf, (r.x, r.y, r.w, r.h)
                r = Region(frame_idx, x, y, w, h, conf, label,
                           0, origin="mpeg")
                final_results.append(r)
        # 需要复用的帧
        else:
            refer = find_refer(frame_idx + 1) - 1
            if refer==-1:continue
            for r in final_results[refer]:
                label, conf, (x, y, w, h) = r.label, r.conf, (r.x, r.y, r.w, r.h)
                _x, _y = move_bbox(frame_idx + 1, x, y, w, h, refer + 1)
                _x, _y = _x / 4, _y / 4


                r = Region(frame_idx, (x - _x / width), (y - _y / width), w, h, conf,
                           label,
                           0, origin="mpeg")
                r = resize(r)
                final_results.append(r)
    final_results.write_results_txt("final_results")