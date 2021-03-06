from net import Net
import matplotlib.pyplot as plt
from PFA import PF

def draw_net(net):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.scatter(net.BS_location[:, 0], net.BS_location[:, 1], marker='^', c='r')
    plt.scatter(net.UE_location[:, 0], net.UE_location[:, 1], marker='o', c='b')
    plt.title('基站，用户位置')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(['基站', '用户'])
    plt.xlim([0, 100])
    plt.ylim([0, 100])



if __name__ == '__main__':
    network = Net()
    network.net_start()
    # network_1 = PF(network)
    # network_1.start()
    plt.figure(1)
    draw_net(network)
    network.update()
    plt.figure(2)
    draw_net(network)
    plt.show()

