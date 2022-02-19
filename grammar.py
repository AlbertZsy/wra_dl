import math

import numpy as np
# a=6                                 #将一个值复制到一个数组
# b=a*np.ones(7)
# print(b)
#
# c= np.array([[3,4,4],[5,8,9],[6,1,2]])          ##np.where函数，以及使用后需要vstack
# d= [np.where(i==min(i),1,0) for i in c]
# print(d)
# d=np.vstack(d)
# print(d)

# a = np.array([[2, 3], [2, 5], [6, 4], [6, 9]])         # 虚数定义
# print(a)
#
# b = np.zeros(2)
# print(b*1j)


# a = np.array([[2, 3, 5, 6], [3, 2, 7, 5], [6, 1, 4, 8], [6, 6, 1, 9]])     # copy()是样本的复制，否则是直接在原函数上修改
# for i in range(4):
#     b = a[:, i].copy()
# b[2] = 7
# print(a)

# a = np.array([2, 3, 5, 6])      # 变量可以放进数组的索引
# for i in range(4):
#     print(a[i])

# a = np.array([[2, 3, 5, 6], [3, 2, 7, 5], [6, 1, 4, 8], [6, 6, 1, 9]])      # sum函数
# b = np.sum(a, axis=1)
# c = np.sum(a, axis=0)
# print(b)
# print(c)

# a = np.array([[[2, 3], [3, 5]], [[4, 1], [6, 9]]])                      # sum函数
# b = np.sum(a[:, 1, 0])
# print(b)

# a = np.array([[2, 3], [4, 5]])                                            # a[0][1]和a[0,1]无区别
# print(a[0, 1])
# print(a[0][2])

a = np.ones(5)
print(a)