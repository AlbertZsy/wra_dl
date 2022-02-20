import math
from net import Net


class PF:
    def __init__(self, net1=Net, cycle=5):
        self.net_ini = net1
        self.cycle = cycle
        self.rate_accumulation = []
        self.rate_proportion = []
        self.BS_UE_priority = []   #某基站倾向连接的用户，内容为用户序号

    def PF_algorithm(self):         # 单位应该是用户
        a = self.net_ini
        UE_maximum = math.ceil(a.FrequencyBand_num*a.Subcarrier_num/Max_BandNumConnectedToUE)  # 计算基站任意时刻连接的用户数
        self.BS_UE_priority = np.ones((a.BS_num, UE_maximum))*UE_num  #初始化用户序号为最大值，与0区分
        self.rate_accumulation += a.rate_for_UE
        for i in range(a.UE_num):
                if self.rate_accumulation[i] == 0:
                    self.rate_proportion[i] = 0
                else:
                    self.rate_proportion[i] = a.rate_for_UE[i]/self.rate_accumulation[i]
        rate_proportion_index = np.argsort(self.rate_proportion)
        for i in range(a.UE_num):
            for j in range(a.BS_num):
                if



    def start(self):
        a = self.net_ini               # 最后记得将a回代回net
        a.net_start()
        self.rate_accumulation = np.zeros(a.UE_num)
        self.rate_proportion = np.zeros(a.UE_num)


