from net import Net
import math
import numpy as np

class env:
    def __init__(self, BS_flag,power_level,net1=Net, ):
        self.net_env= net1
        self.BS_flag = BS_flag
        self.power_level = power_level
        self.state_dim = net1.Subcarrier_num*net1.FrequencyBand_num+net1.BS_num-1
        self.action_dim = net1.Subcarrier_num*net1.FrequencyBand_num *self.power_level


    def step(self,action):
        temp = self.net_env.power[self.BS_flag][action[0]]
        self.net_env.power[self.BS_flag][action[0]] = action[1]/self.power_level *0.2
        if np.sum(self.net_env.power[self.BS_flag]) > self.net_env.BS_max_power:      # 执行这次动作后功率超出，则取消这次动作
            self.net_env.power[self.BS_flag][action[0]] = temp

        reward = 1- math.e**self.net_env.compute_rate_on_system()
        bs_state =[]
        for i in range(self.net_env.BS_num):
            if i!=self.BS_flag:
                bs_state.append(self.net_env.rate_for_BS[i])
        next_state = np.hstack((self.net_env.sinr[self.BS_flag],bs_state ))
        return next_state, reward

    def reset(self,net1=Net):
        self.net_env = net1










