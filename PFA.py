from net import Net


class PF:
    def __init__(self, net1=Net, cycle=5):
        self.net_ini = net1
        self.cycle = cycle
        self.rate_accumulation = []
        self.rate_proportion = []

    def PF_algorithm(self):         # 单位应该是用户
        a = self.net_ini
        self.rate_accumulation += log2(1+sinr)
        for i in range(a.BS_num):
            for j in range(a.FrequencyBand_num*a.Subcarrier_num):
                if self.rate_accumulation[i][j] == 0:
                    self.rate_proportion[i][j] = 0
                else:
                    self.rate_proportion[i, j] = log2(1+sinr[i, j])/self.rate_accumulation[i, j]



    def start(self):
        a = self.net_ini               # 最后记得将a回代回net
        a.net_start()
        self.rate_accumulation = np.zeros(a.UE_num)
        self.rate_proportion = np.zeros(a.UE_num)


