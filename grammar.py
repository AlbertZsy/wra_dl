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
# b = np.ones((5, 2))                                                       # np.ones 初始化为小数
# print(type(a[0, 1]))
# print(type(a[0][1]))
# print(b[0, 1])
# print(b[0][1])

# a = np.array([2, 6, 4, 5])                                              # argsort不改变原数组的顺序
# b = np.argsort(a)
# print(b)
# print(a)

# a = 5                                                                       # 向上取整函数
# b = 2
# print(math.ceil(a/b))

# a = np.ones((2, 5))                                                        # 定义一个数组，其中数组元素为固定值
# b = a * 12
# print(b)

# a = [1, 2, 3, 4]
# b = 4
# if b in a:
#     print("yes")
# else:
#     print("no")

# a = np.array([[2, 3, 5, 6], [3, 3, 3, 3], [6, 1, 4, 8], [6, 6, 1, 9]])   # 输出矩阵第一列
# print(a[1,:])

# b = np.sum(np.log2(1+a[1, :]))
# print(b)

a = np.array([2, 3, 5, 6])
b = np.array([1, 3, 5, 2])
print(a*b)
