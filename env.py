from net import Net
import math
import numpy as np

class env:
    def __init__(self, BS_flag, net1=Net, ):
        self.net_env= net1
        self.BS_flag = BS_flag
        self.state_dim = net1.Subcarrier_num*net1.FrequencyBand_num+net1.BS_num-1
        self.action_dim = net1.Subcarrier_num*net1.FrequencyBand_num


    def step(self,action):
        self.net_env.power[self.BS_flag] = action
        reward = 1- math.e**self.net_env.compute_rate_on_system()
        bs_state =[]
        for i in range(self.net_env.BS_num):
            if i!=self.BS_flag:
                bs_state.append(self.net_env.rate_for_BS[i])
        next_state = np.hstack((self.net_env.sinr[self.BS_flag],bs_state ))









