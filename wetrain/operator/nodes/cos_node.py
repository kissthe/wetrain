import sys
import os

import numpy as np

# path = os.path.dirname(__file__)
# sys.path.append(path)
from wetrain.operator.nodes.bases.cal_node import cal_node
from wetrain.wtensor.wtensor import wtensor

class cos_node(cal_node):

    def __init__(self,data_1:wtensor,data_2:wtensor):

        super().__init__()

        self._node_attr['type'] = 'cos'

        self.data_1 = data_1 #设置当前节点需要的前后运算节点
        self.data_2 = data_2

        self.children.append(data_1) #加载到节点图中
        self.parent.append(data_2)

        self.data_1.parent.append(self)
        self.data_2.children.append(self)

    def forward(self):

        # 如果还有子节点没有前向传播，则直接返回
        for item in self.children:
            if item.is_forward == False:
                item.forward()

        #计算节点值
        self.data_2.data = np.cos(self.data_1.data)
        self.data_2.grad = np.zeros_like(self.data_2.data)
        #设置节点状态
        self.is_forward = True
        self.is_backward = False

        # 继续前向传播
        for item in self.parent:
            if item.is_forward == False:
                item.forward()

        return

    def backward(self):

        # 若还有父节点没有反向传播，则退出
        for item in self.parent:
            if item.is_backward == False:
                item.backward()

        #设置梯度
        self.data_1.grad += - np.sin(self.data_1.data) * self.data_2.grad
        self.data_1._node_attr['backward_type'] = 'cos_backward'

        #设置节点状态
        self.is_backward = True
        self.is_forward = False

        for item in self.children:
            if item.is_backward == False:
                item.backward()

        return

if __name__ == '__main__':
    input1 = wtensor([[1,2],[2,3]])
    input2 = wtensor()

    adder = cos_node(input1, input2)
    adder.forward()

    input2.grad += 0.1

    print(input2.data)
    print(input2.grad)

    adder.backward()

    print(input1.grad)