import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
import math


class Net:
    def __init__(self, B=1e7, BS_num=4, UE_num=50, BS_init_power=10, BS_max_power=20,
                 FrequencyBand_num=2, Subcarrier_num=50, net_size=(100, 100), N0=1e-7,
                 Max_BandNumConnectedToUE = 10):
        # np.random.seed(1)
        self.BS_num = BS_num
        self.UE_num = UE_num
        self.net_size = net_size
        self.B = B
        self.N0 = N0
        self.BS_power = BS_init_power * np.ones(BS_num)
        self.AdjacentMatrix = []  # 邻接矩阵
        self.all_distance = []  # 基站和用户两两之间的距离
        self.BS_UE_distance = []  # 用户到基站的距离
        self.BS_BS_distance = []  # 基站到基站的距离
        self.BS_location = []  # 基站位置
        self.UE_location = []  # 用户位置
        self.FrequencyBand_num = FrequencyBand_num                  # 单个基站的频点个数,默认为两个
        self.Subcarrier_num = Subcarrier_num                        # 单个频点的子载波个数
        self.UENumConnectedToBS = []                                # 连接到某个基站的用户数
        self.Max_BandNumConnectedToUE = Max_BandNumConnectedToUE    # 单个用户最大连接信道数，默认为10个
        self.BandNumConnectedToUE = []                              # 连接到某个用户的信道数
        self.net_channel = []  # 信道状况

    def net_generation(self):
        BS_UE_loc = np.vstack((self.BS_location, self.UE_location))
        distance = squareform(pdist(BS_UE_loc, 'euclidean'))
        BS_UE_distance = distance[self.BS_num:, :self.BS_num]
        BS_BS_distance = distance[:self.BS_num, :self.BS_num]
        AdjacentMatrix = [np.where(i == min(i), 1, 0) for i in BS_UE_distance]
        self.AdjacentMatrix = np.vstack(AdjacentMatrix)
        self.BS_UE_distance = BS_UE_distance
        self.BS_BS_distance = BS_BS_distance
        self.all_distance = distance
        self.UENumConnectedToBS = np.sum(AdjacentMatrix, axis=0)

    def ue_loc_generation(self):
        width = self.net_size[0]
        length = self.net_size[1]
        location_x = np.random.rand(self.UE_num) * width
        location_y = np.random.rand(self.UE_num) * length
        UE_location = np.vstack((location_x, location_y))  # 2*Ue_num
        return UE_location.T  # 转置    UE_num*2

    def bs_loc_generation(self):
        # width = self.net_size[0]            #基站位置确定
        # length = self.net_size[1]
        # x_loc = np.random.rand(self.BS_num)*width
        # y_loc = np.random.rand(self.BS_num)*length
        # loc = np.vstack((x_loc, y_loc))
        # return loc.T
        loc = np.array([[25, 25], [25, 75], [75, 25], [75, 75]])
        self.BS_location = loc

    def channel_generation(self):
        channel_matrix = np.zeros((self.UE_num, self.BS_num, self.FrequencyBand_num*self.Subcarrier_num), dtype = complex)
        channel_matrix_module = np.zeros((self.UE_num, self.BS_num, self.FrequencyBand_num*self.Subcarrier_num))
        d0 = 2.5       # 参考距离
        n = 3         # 路径损耗因子
        sigma = 3     # 对数阴影衰落方差
        noise = np.random.normal(loc=0, scale=sigma, size=(self.UE_num, self.BS_num,
                                                           self.FrequencyBand_num*self.Subcarrier_num))
        real = np.random.randn(self.UE_num, self.BS_num, self.FrequencyBand_num*self.Subcarrier_num)
        img = np.random.randn(self.UE_num, self.BS_num, self.FrequencyBand_num*self.Subcarrier_num)
        for i in range(self.UE_num):
            for j in range(self.BS_num):
                for m in range(self.FrequencyBand_num*self.Subcarrier_num):
                    if self.FrequencyBand_num == 2:             # 两个频带
                        if m < self.Subcarrier_num:
                            fc = 1.8e9
                        else:
                            fc = 2.1e9
                    else:                                       # 三个频带
                        if m < self.Subcarrier_num:
                            fc = 9e8
                        elif m < 2*self.Subcarrier_num:
                            fc = 1.8e9
                        else:
                            fc = 2.1e9
                    PL_F = 20 * np.log10(4 * math.pi * d0 * fc / 3e8)   # 大尺度衰落，单位是分贝
                    if self.BS_UE_distance[i][j]/d0 <= 0.1:
                        PL_F = PL_F + 10 * n * np.log10(0.1) + noise[i][j][m]
                    else:
                        PL_F = PL_F+10*n*np.log10(self.BS_UE_distance[i][j]/d0)+noise[i][j][m]      # 添加了对数阴影衰落和噪声
                    PL_F = 10**(-PL_F/10)   # 分贝转换为十进制
                    channel_matrix[i][j][m] = PL_F*(real[i][j][m]+img[i][j][m]*1j)/math.sqrt(2)  # 大尺度+小尺度
                    channel_matrix_module[i][j][m] = abs(channel_matrix[i][j][m])
        self.net_channel = channel_matrix_module

    def channel_alloc(self):
        channel_matrix_temp = np.zeros((self.UE_num, self.BS_num, self.FrequencyBand_num * self.Subcarrier_num))
        UE_order = np.zeros((self.BS_num, self.FrequencyBand_num * self.Subcarrier_num, self.UE_num))  # 到某信道的各用户的信道状况
        SN_BandToUE = np.zeros((self.BS_num, self.FrequencyBand_num * self.Subcarrier_num))       # 连接到某基站某信道的用户序号
        for i in range(self.UE_num):
            for j in range(self.BS_num):
                for m in range(self.FrequencyBand_num * self.Subcarrier_num):
                    channel_matrix_temp[i][j][m] = self.net_channel[i][j][m]*self.AdjacentMatrix[i][j]
        for i in range(self.BS_num):
            for j in range(self.FrequencyBand_num * self.Subcarrier_num):
                UE_order[i][j] = channel_matrix_temp[:, i, j].copy()
        UE_order_val = np.sort(UE_order)        # 信道状况由大到小排序
        UE_order_index = np.argsort(UE_order)   # 返回排序的索引值，该变量反应了到某信道的用户优先级（哪个用户连接到信道效果最好）

        for i in range(self.BS_num):
            for j in range(self.FrequencyBand_num * self.Subcarrier_num):       # 对信道进行分配，初始化
                m = 0
                while UE_order_val[i][j][m] > 0:                                # 当前序号的信道非零，即表示用户与该信道是可相连的
                    k = UE_order_index[i][j][m]                                 # 该信道最倾向的用户
                    if self.BandNumConnectedToUE[k] < self.Max_BandNumConnectedToUE:    # 用户连接信道数未达到最大值
                        SN_BandToUE[i][j] = k                                   # i基站j信道分配给的用户序号为k
                        self.BandNumConnectedToUE[k] += 1                       # 用户连接信道加一
                        break
                    else:                                                       # 用户连接信道数达到最大值
                        m = m+1                                                 # 分配给次优的用户






    def net_start(self):
        self.bs_loc_generation()
        self.UE_location = self.ue_loc_generation()
        self.net_generation()
        self.channel_generation()