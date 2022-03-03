import math
from net import Net
import numpy as np


class PF:
    def __init__(self, net1=Net, cycle=5):
        self.net_ini = net1
        self.cycle = cycle
        self.rate_accumulation = []
        self.rate_proportion = []
        self.BS_UE_priority = []   # 某基站倾向连接的用户，内容为用户序号
        self.BS_UE_priority_index = []  # 倾向连接用户在数组中的位置

    def PF_algorithm(self):         # 单位应该是用户
        a = self.net_ini
        UE_maximum = math.ceil(a.FrequencyBand_num*a.Subcarrier_num/a.Max_BandNumConnectedToUE)  # 计算基站任意时刻连接的用户数
        self.BS_UE_priority = np.ones((a.BS_num, UE_maximum), dtype=np.int16)*a.UE_num  # 初始化用户序号为最大值，与0区分
        # self.BS_UE_priority = self.BS_UE_priority.astype(int)
        self.BS_UE_priority_index = np.zeros(a.BS_num, dtype=np.int16)
        self.rate_accumulation += a.rate_for_UE
        for i in range(a.UE_num):                                     # 比例函数=当前速率/累计速率
            if self.rate_accumulation[i] == 0:
                self.rate_proportion[i] = 0
            else:
                self.rate_proportion[i] = a.rate_for_UE[i]/self.rate_accumulation[i]
        rate_proportion_index = np.argsort(self.rate_proportion)       # 根据比例函数由大到小排序，返回索引值
        rate_proportion_index_reverse = rate_proportion_index[:: -1]   # 排序的逆序
        rate_proportion_val = np.sort(self.rate_proportion)
        for i in range(a.UE_num):                                       # 比例为0说明该用户之前未连接信道，优先分配
            if rate_proportion_val[i] != 0:
                break
            k = rate_proportion_index[i]
            for j in range(a.BS_num):
                if a.AdjacentMatrix[k][j] == 1:
                    if rate_proportion_val[i] == 0 and self.BS_UE_priority_index[j] <UE_maximum:
                        m = self.BS_UE_priority_index[j]
                        self.BS_UE_priority[j][m] = k
                        self.BS_UE_priority_index[j] += 1

        for i in range(a.UE_num):                                        # 优先分配比例值大的用户
            k = rate_proportion_index_reverse[i]
            for j in range(a.BS_num):
                if a.AdjacentMatrix[k][j] == 1:
                    if self.BS_UE_priority_index[j] < UE_maximum:
                        m = self.BS_UE_priority_index[j]
                        self.BS_UE_priority[j][m] = k
                        self.BS_UE_priority_index[j] += 1
        b = self.channel_realloc(a)                                         # 基站信道分配给哪些用户在BS_UE_priority中显示
        return b

    def channel_realloc(self, net1=Net):
        b = net1
        channel_matrix_temp = np.zeros((b.UE_num, b.BS_num, b.FrequencyBand_num * b.Subcarrier_num))
        UE_order = np.zeros((b.BS_num, b.FrequencyBand_num * b.Subcarrier_num, b.UE_num))  # 到某子载波的各用户的信道状况
        BandNumConnectedToUE = np.zeros(b.UE_num)
        SN_BandToUE = np.zeros((b.BS_num, b.FrequencyBand_num * b.Subcarrier_num))  # 连接到某基站某子载波的用户序号
        for i in range(b.UE_num):
            for j in range(b.BS_num):
                for m in range(b.FrequencyBand_num * b.Subcarrier_num):
                    channel_matrix_temp[i][j][m] = b.net_channel[i][j][m] * b.AdjacentMatrix[i][j]
        for i in range(b.BS_num):
            for j in range(b.FrequencyBand_num * b.Subcarrier_num):
                UE_order[i][j] = channel_matrix_temp[:, i, j].copy()
        UE_order_val = np.sort(UE_order)  # 子载波状况由大到小排序
        UE_order_index = np.argsort(UE_order)

        for i in range(b.BS_num):                                    # 参考net类中信道分配的函数
            for j in range(b.FrequencyBand_num * b.Subcarrier_num):  # 对子载波进行分配，初始化
                m = b.UE_num - 1  # 上面排序实则为由小到大，要逆序
                while UE_order_val[i][j][m] > 0:  # 当前序号的子载波非零，即表示用户与该子载波是可相连的
                    k = UE_order_index[i][j][m]  # 该子载波最倾向的用户
                    if BandNumConnectedToUE[k] < b.Max_BandNumConnectedToUE and (k in self.BS_UE_priority[i]):
                        #  用户连接子载波数未达到最大值且该用户在基站的优先用户调用之内
                        SN_BandToUE[i][j] = k  # i基站j子载波分配给的用户序号为k
                        BandNumConnectedToUE[k] += 1  # 用户连接子载波数加一
                        break
                    else:  # 用户连接子载波数达到最大值
                        m = m - 1  # 分配给次优的用户
        b.BandNumConnectedToUE = BandNumConnectedToUE
        b.SN_BandToUE = SN_BandToUE
        return b

    def recompute_SINR_on_bs_sub(self, n, k):
        c = self.net_ini
        if c.SN_BandToUE[n][k] == 0:
            sinr = 0
        else:
            power_on_sub = c.BS_max_power/(c.FrequencyBand_num*c.Subcarrier_num)
            i = int(c.SN_BandToUE[n][k])
            sinr = power_on_sub*c.net_channel[i][n][k]/((np.sum(c.net_channel[i, :, k]) -
                                                            c.net_channel[i][n][k]) * power_on_sub + c.N0)
        return sinr

    def recompute_rate_on_bs(self, n):
        c = self.net_ini
        assert 0 <= n < c.BS_num
        for k in range(c.FrequencyBand_num * c.Subcarrier_num):
            c.sinr[n][k] = c.recompute_SINR_on_bs_sub(n, k, c)        # 计算sinr
        bandwidth = c.B/(c.FrequencyBand_num*c.Subcarrier_num)
        self.net_ini.sinr = c.sinr
        return bandwidth * np.sum(log2(1+c.sinr[n, :]))

    def recompute_rate_on_UE(self):       # 对于每个用户的信干噪比进行计算
        c = self.net_ini
        bandwidth = c.B / (c.FrequencyBand_num * c.Subcarrier_num)
        for i in range(c.BS_num):
            for j in range(c.FrequencyBand_num*c.Subcarrier_num):
                if c.SN_BandToUE[i, j]!= 0:
                    k = c.SN_BandToUE[i, j]
                    c.rate_for_UE[k] += bandwidth * log2(1+c.sinr[i, j])    # 计算用户级速率
        self.net_ini.rate_for_UE = c.rate_for_UE

    def recompute_rate_on_system(self):
        c = self.net_ini
        system_rate = 0
        for n in range(c.BS_num):
            system_rate += c.recompute_rate_on_bs(n)
        c.recompute_rate_on_UE(c)
        return system_rate

    def start(self):
        # a = self.net_ini               # 最后记得将a回代回net
        self.rate_accumulation = np.zeros(self.net_ini.UE_num)
        self.rate_proportion = np.zeros(self.net_ini.UE_num)
        for i in range(self.cycle):
            a = self.PF_algorithm()
            a.sinr = np.zeros((a.BS_num, a.FrequencyBand_num * a.Subcarrier_num))
            a.rate_for_UE = np.zeros(a.UE_num)
            self.net_ini = a
            system_rate = self.recompute_rate_on_system()