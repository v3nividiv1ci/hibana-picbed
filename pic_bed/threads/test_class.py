# 定义一个类描述平面上的点并提供移动点和计算到另一个点距离的方法。

from math import sqrt

# 继承了object类
# 但是python3里面默认所有类继承object类，所以可以省略
class Spot(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.distance = 0

    def move(self, t_x, t_y):
        self.x = t_x
        self.y = t_y

    def dis(self, other):
        self.distance = sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return self.distance


def main():
    p1 = Spot(1, 2)
    p2 = Spot()
    print(p1)
    print(p2)
    p2.move(1, -2)
    print(p2)
    print(p1.dis(p2))


if __name__ == '__main__':
    main()