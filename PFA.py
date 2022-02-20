import math
from net import Net


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
        UE_maximum = math.ceil(a.FrequencyBand_num*a.Subcarrier_num/Max_BandNumConnectedToUE)  # 计算基站任意时刻连接的用户数
        self.BS_UE_priority = np.ones((a.BS_num, UE_maximum))*UE_num  #初始化用户序号为最大值，与0区分
        self.BS_UE_priority_index = np.zeros(a.BS_num)
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

        








    def start(self):
        a = self.net_ini               # 最后记得将a回代回net
        a.net_start()
        self.rate_accumulation = np.zeros(a.UE_num)
        self.rate_proportion = np.zeros(a.UE_num)


