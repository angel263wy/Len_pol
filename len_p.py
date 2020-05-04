import numpy as np
import glob
import struct

# raw 文件输出函数
def raw_file_output(fname, raw_data):
    with open(fname, 'wb') as f:
        raw_data[raw_data < 0] = 0  # 除去负数
        for i in raw_data.flat:          
            foo = struct.pack('H', int(i))
            f.write(foo)

# DPC02 帧转移校正函数
def smearing(img):
    width = 1024
    height = 1030
    raw_data = np.array(img).reshape(height, width)
    # 取暗行
    dark_lines = raw_data[0:6, :]
    # 求平均
    dark_lines_mean = np.mean(dark_lines, axis=0) 
    # 帧转移校正 按行扣暗行平均值 广播算法 矩阵每行减去向量 并扣除负值
    img_final = np.clip(raw_data - dark_lines_mean, 0, 65530)
    
    return img_final.flatten()


# 预处理 求平均 扣本底 帧转移校正 输出
def raw_proc(filelist, darkfile,fout):
    width = 1024
    height = 1030
    raw_data = np.empty([len(filelist), width*height], dtype=np.uint16)
    # 读入文件求平均    
    for i, filename in enumerate(filelist):
        raw_data[i] = np.fromfile(filename, dtype=np.uint16)
    img_mean = np.mean(raw_data, axis=0) 
    # 读入本底并扣本底
    img_dark = np.fromfile(darkfile, dtype=np.uint16)
    img = img_mean- img_dark
    # 帧转移校正
    img_ok = smearing(img)   
    # 输出
    raw_file_output(fout, img_ok)
    print(fout)
    


p_cnt = ['001', '015', '030', '045', '059']
# p_cnt = ['001']
for i in p_cnt:  # 视场角
    for j in range(1,26):  # 偏振片方位角
        fw = str(j).zfill(2)
        flist = glob.glob('DPC_P' + i +'_C' + fw +'_B*') 
        darkFileName = 'bugeli_dark.raw'
        foutName = 'proc_DPC_P' + i +'_C' + fw + '.raw'
        raw_proc(flist, darkFileName, foutName) 
        
