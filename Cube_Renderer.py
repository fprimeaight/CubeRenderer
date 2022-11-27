import os
import time
from math import sin,cos,pi

class ScreenPoint:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Screen:
    def __init__(self):
        self.length = 41
        self.width = 21
        self.screen = [['..' for i in range(self.length)] for j in range(self.width)]
    
    def Display(self):
        os.system('cls')
        for i in range(self.width):
            output = ''
            for j in range(self.length):
                output += self.screen[i][j]
            print(output)
        self.screen = [['..' for i in range(self.length)] for j in range(self.width)]

    def DrawEdge(self,point1,point2):
        if point2.x-point1.x == 0:
            gradient = 999
        else:
            gradient = (point2.y-point1.y)/(point2.x-point1.x)

        if abs(gradient) <= 1:
            if point1.x <= point2.x:
                for i in range(point1.x,point2.x+1):
                    line_eqn_y = round(gradient * i - gradient * point1.x + point1.y)
                    self.screen[line_eqn_y][i] = '$$'
            else:
                for i in range(point1.x,point2.x-1,-1):
                    line_eqn_y = round(gradient * i - gradient * point1.x + point1.y)
                    self.screen[line_eqn_y][i] = '$$'
        else:
            if point1.y <= point2.y:
                for i in range(point1.y,point2.y+1):
                    if gradient != 0:
                        line_eqn_x = round((i - point1.y + gradient * point1.x) / gradient)
                        self.screen[i][line_eqn_x] = '$$'
            else:
                for i in range(point1.y,point2.y-1,-1):
                    if gradient != 0:
                        line_eqn_x = round((i - point1.y + gradient * point1.x) / gradient)
                        self.screen[i][line_eqn_x] = '$$'

class Vertex:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def VertexToScreenPoint(self,focal_length,screen_instance):
        screen_x = round(self.x * focal_length / (self.z + focal_length))
        screen_y = round(self.y * focal_length / (self.z + focal_length))
        x_offset = screen_instance.length // 2
        y_offset = screen_instance.width // 2
        return screen_x + x_offset,screen_y + y_offset
    
    def RotateVertexX(self,theta=0):
        y_new = self.y * cos(theta) - self.z * sin(theta)
        z_new = self.y * sin(theta) + self.z * cos(theta)
        self.y = y_new
        self.z = z_new

    def RotateVertexY(self,theta=0):
        x_new = self.x * cos(theta) - self.z * sin(theta)
        z_new = self.x * sin(theta) + self.z * cos(theta)
        self.x = x_new
        self.z = z_new

    def RotateVertexZ(self,theta=0):
        x_new = self.x * cos(theta) - self.y * sin(theta)
        y_new = self.x * sin(theta) + self.y * cos(theta)
        self.x = x_new
        self.y = y_new

    def RotateVertexAllAxis(self,a=0,b=0,c=0):
        self.RotateVertexX(a)
        self.RotateVertexY(b)
        self.RotateVertexZ(c)

def main(length,focal_length,theta_a,theta_b,theta_c):
    scr = Screen()

    vertices = {'v1': Vertex(-length,-length,length),
                'v2': Vertex(length,length,length),
                'v3': Vertex(length,-length,length),
                'v4': Vertex(-length,length,length),
                'v5': Vertex(-length,-length,-length),
                'v6': Vertex(length,length,-length),
                'v7': Vertex(length,-length,-length),
                'v8': Vertex(-length,length,-length)}

    points = {'v1': None,
              'v2': None,
              'v3': None,
              'v4': None,
              'v5': None,
              'v6': None,
              'v7': None,
              'v8': None}

    edges = {'e1': ('v1','v3'),
             'e2': ('v2','v3'),
             'e3': ('v1','v4'),
             'e4': ('v2','v4'),
             'e5': ('v5','v7'),
             'e6': ('v6','v7'),
             'e7': ('v5','v8'),
             'e8': ('v6','v8'),
             'e9': ('v5','v1'),
             'e10': ('v6','v2'),
             'e11': ('v7','v3'),
             'e12': ('v8','v4')}

    while True:
        for vertex in vertices:
            vertices[vertex].RotateVertexAllAxis(theta_a,theta_b,theta_c)
            new_screen_point = vertices[vertex].VertexToScreenPoint(focal_length,scr)
            points[vertex] = ScreenPoint(new_screen_point[0],new_screen_point[1])

        for edge in edges:
            scr.DrawEdge(points[edges[edge][0]],points[edges[edge][1]])

        scr.Display()
        time.sleep(0.05)

if __name__ == '__main__':
    main(4,10,pi/30,pi/24,pi/15)