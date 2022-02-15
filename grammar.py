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

# a = np.array([[2, 3], [2, 5], [6, 4], [6, 9]])
# print(a)
#
# b = np.zeros(2)
# print(b*1j)


a = np.array([[2, 3, 5, 6], [3, 2, 7, 5], [6, 1, 4, 8], [6, 6, 1, 9]])
for i in range(4):
    b = a[:, i].copy()
b[2] = 7
print(a)

# a = np.array([2, 3, 5, 6])
# for i in range(4):
#     print(a[i])