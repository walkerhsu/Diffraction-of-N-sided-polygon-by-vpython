from vpython import *
from numpy import *
import math
N = 85
R, lamda0 = 1.0, 500E-9
d = 100E-6
dx, dy = d/N, d/N
lastAperture = -1
lastMedium = -1
aperture = 0
medium = 1

s='\n'
shape_key = [0 , 1 , 2]
shape_value = ["circle" , "rectangle" , "W-sided shape"]
medium_key = [1 , 1.33 , 1.55]
medium_value = ["air" , "water" , "glass"]
shape_dict = dict(zip(shape_key ,shape_value))
medium_dict = dict(zip(medium_key ,medium_value))
scene1 = canvas(title = 'aperture with different shapes and medium' ,  align = 'left', height=600, width=600, center = vector(N*dx/2, N*dy/2, 0) )
scene2 = canvas(align = 'right', x=600, height=600, width=600, center = vector(N*dx/2, N*dy/2, 0))
scene1.lights = []
scene2.lights = []
scene1.ambient = color.gray(0.99)
scene2.ambient = color.gray(0.99)

"""
def keyinput(evt): #keyboard callback function
    global pinhole , medium , lastPinhole , lastMedium
    s = evt.key
    print("Event Key : {}".format(s))
    if s == 'c' : 
        pinhole = 0
    elif s=='r':
        pinhole = 1
    elif s=='s':
        pinhole = 2
    elif s=='w':
        medium = 1.33
    elif s=='a':
        medium = 1
    elif s=='g':
        medium = 1.55
    elif s=='3':
        W = 3
"""

run_1 = True
run_2 = False
run_3 = False

def run_1(b1):
    global run_1
    run_1 = not run_1

b1 = button(text = "circle",pos = scene2.title_anchor,bind=run_1)

def run_2(b2):
    global run_2
    run_2 = not run_2

b2 = button(text = "rectangle",pos = scene2.title_anchor,bind=run_2)

def run_3(b3):
    global run_3
    run_3 = not run_3

b3 = button(text = "W-sided shape",pos = scene2.title_anchor,bind=run_3)

def set_W(Wslider):
    W = Wslider.value
    vtext.text = '{:1d}-sided shape aperture'.format(Wslider.value)
    

Wslider = slider(min = 3 , max = 16 , step = 1 ,value = 3 , length = 300 ,
                            bind = set_W, right = 15 , pos = scene2.title_anchor)
vtext = wtext(text='{:1d}-sided shape aperture'.format(Wslider.value), pos=scene2.title_anchor)
W = Wslider.value
lastW = W

run_4 = False
run_5 = False
run_6 = False

def run_4(b4):
    global run_4
    run_4 = not run_4

b4 = button(text = "air",pos = scene1.title_anchor,bind=run_4)

def run_5(b5):
    global run_5
    run_5 = not run_5

b5 = button(text = "water",pos = scene1.title_anchor,bind=run_5)

def run_6(b6):
    global run_6
    run_6 = not run_6

b6 = button(text = "glass",pos = scene1.title_anchor,bind=run_6)

#scene1.bind('keydown', keyinput) # setting for the binding function
#scene2.bind('keydown', keyinput) # setting for the binding function
def get_E_field(shape1 , medium):
    if shape1 == 0:
        E_field , maxI = circle_E_field(medium)
        return E_field , maxI
    elif shape1 == 1 :
        E_field , maxI = rectangle_E_field(medium)
        return E_field , maxI
    elif shape1 == 2 :
        E_field , maxI = W_sided_poly_E_field(medium)
        return E_field , maxI
    else:
        return 0 , 0

def circle_E_field(medium):
    lamda = lamda0 / medium
    side = linspace(-0.01*pi, 0.01*pi, N)
    x,y = meshgrid(side,side)
    # E_field = cos(10000*((x-0.005)**2 + (y- 0.002)**2 )) # change this to calculate the electric field of diffraction of the aperture
    A = zeros((N,N))
    for i in range(N):
        for j in range(N):
            if(((i-0.5*N)**2+(j-0.5*N)**2)<=(0.5*N)**2):
                A += cos((2*pi/lamda/R)*(x*dx*(i-0.5*N)+y*dy*(j-0.5*N)))
    E_field = A/R
    Inte = abs(E_field)
    maxI = amax(Inte)
    return Inte , maxI

def rectangle_E_field(medium):
    lamda = lamda0 / medium
    side = linspace(-0.01*pi, 0.01*pi, N)
    x,y = meshgrid(side,side)
    # E_field = cos(10000*((x-0.005)**2 + (y- 0.002)**2 )) # change this to calculate the electric field of diffraction of the aperture
    A = zeros((N,N))
    for i in range(N):
        for j in range(N):
            A += cos((2*pi/lamda/R)*(x*dx*(i-0.5*N)+y*dy*(j-0.5*N)))
    E_field = A/R
    Inte = abs(E_field)
    maxI = amax(Inte)
    return Inte , maxI

def W_sided_poly_E_field(medium):
    lamda = lamda0 / medium
    side = linspace(-0.01*pi, 0.01*pi, N)
    x,y = meshgrid(side,side)
    # E_field = cos(10000*((x-0.005)**2 + (y- 0.002)**2 )) # change this to calculate the electric field of diffraction of the aperture
    A = zeros((N , N))
    B = zeros((N , N))
    points_x = []
    points_y = []
    for i in range(W):
        points_x.append(0.5*N + 0.5*N*cos(i*(2*pi/W)))
        points_y.append(0.5*N + 0.5*N*sin(i*(2*pi/W)))
        # print(points_x , points_y)
        
    for i in range(N):
        for j in range(N):
            th = math.atan((j-0.5*N) / (i-0.5*N))
            if(i-0.5*N>=0 and j-0.5*N>=0):
                theta = th
            elif(i-0.5*N<0 and j-0.5*N>=0):
                theta = th + pi
            elif(i-0.5*N<0 and j-0.5*N<0):
                theta = th + pi
            else:
                theta = th + 2*pi
            index = int(theta / (2*pi/W))  # index , index+1
            normal = vec(points_y[(index+1)%W] - points_y[index] , -(points_x[(index+1)%W] - points_x[index]) , 0)
            vec1 = vec(i-points_x[index] , j-points_y[index] , 0)
            if(normal.dot(vec1) <= 0):
                A += cos((2*pi/lamda/R)*(x*dx*(i-0.5*N)+y*dy*(j-0.5*N)))
                B += sin((2*pi/lamda/R)*(x*dx*(i-0.5*N)+y*dy*(j-0.5*N)))
        
    # E_field = A/R
    E_field = sqrt(A**2 + B**2) / R
    Inte = abs(E_field)
    maxI = amax(Inte)
    return Inte , maxI

def draw(aperture , medium , W , lastW):
        print("aperture is in the shape of {} , and the medium is {}".format(shape_dict[pinhole] , medium_dict[medium]))
        Inte , maxI = get_E_field(pinhole , medium)
        for i in range(N):
            for j in range(N):
                if Inte[i,j]/maxI <= 0.03 : 
                    c = 0
                elif  Inte[i,j]/maxI :
                    c = 1
                box(canvas = scene2, pos=vector(i*dx, j*dy, 0), length = dx, height= dy, width = dx,
                color=vector(c,c,c))
                box(canvas = scene1, pos=vector(i*dx, j*dy, 0), length = dx, height= dy, width = dx,
                color=vector(Inte[i,j]/maxI,Inte[i,j]/maxI,Inte[i,j]/maxI))
        print(W)

        # for i in range(int(N/2) , N):
        #     if Inte[int(N/2) , i] < Inte[int(N/2) , i+1]:
        #         print("practical Theta = {}".format(sqrt(x[int(N/2) , i]**2 + y[int(N/2) , i]**2)/R))
        #         break

        # print("theoretical Theta = {}".format(1.22 * lamda0/d))  

while True:
    if run_1:
        pinhole = 0
        run_1 = not run_1
        run_2 = False
        run_3 = False
        draw(aperture , medium , W , lastW)
    elif run_2:
        pinhole = 1
        run_1 = False
        run_2 = not run_2
        run_3 = False
        draw(aperture , medium , W , lastW)
    elif run_3:
        pinhole = 2
        run_1 = False
        run_2 = False
        run_3 = not run_3
        draw(aperture , medium , W , lastW)
    if run_4:
        medium = 1
        run_4 = not run_4
        run_5 = False
        run_6 = False
        draw(aperture , medium , W , lastW)
    elif run_5:
        medium = 1.33
        run_4 = False
        run_5 = not run_5
        run_6 = False
        draw(aperture , medium , W , lastW)
    elif run_6:
        medium = 1.55
        run_4 = False
        run_5 = False
        run_6 = not run_6
        draw(aperture , medium , W , lastW)

    W = Wslider.value
    if(W != lastW):
        draw(aperture , medium , W , lastW)
        lastW = W
    
    
