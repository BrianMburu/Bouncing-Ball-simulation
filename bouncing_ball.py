#Importing Necessary libraries
import turtle
import random
import time
import matplotlib.pyplot as plt
import numpy as np

#Class to create a ball object
class Ball(turtle.Turtle):
    gravity = 9.8   #Gravity effects
    rho = 0.85      #coefficient of restitution
    mu = 0.80      #coefficient of friction
    cd = 0.5        #Drag coefficient of a sphere
    drag = 0        #Total drag **to be updated

    def __init__(self, x=0, y=0):
        super().__init__() #enables easymultiple inheritance from turtle.Turtle parent class
        self.penup()
        self.hideturtle()
        self.drag = 0

        # Velocities initialization comment/uncomment required pair velocities
        #Constant velocity
        self.y_velocity = 0     #from rest.
        self.x_velocity = 0.3   #Initialize sideways motion

        self.h_init = x         #initial height

        self.setposition(x, y)  #initializing ball position
        self.size = int(random.gammavariate(25, 0.8)) #generating ball sizes.
        self.color(random.choice(['blue','orange','red','green','violet','black','purple','pink'])) #Ball color
        
    # Draw function to generate a ball of size self.size(from the gammavariate random function)
    def draw(self):
        self.clear()
        self.dot(self.size)

    #function to simulate loss of energy per bounce on the floor
    def tfle_lost(self,vel):
        tfle=self.rho*vel    #increasing total energy lost per bounce (on ground) with ball size.v2 = Rv1, R=rho
        return tfle
    
    #function to simulate loss of energy per bounce on the wall    
    def twe_lost(self,vel):
        twe=self.rho*vel    #increasing total energy lost per bounce(at wall) with ball size. v2 = Rv1 , R=rho
        return twe
        
    #function to calculate mass of the inflattable ball
    def t_mass_gen(self):
        r = self.size/2 * 10**-2
        bv= 4/3 * np.pi * r**3 
        m=1.225*bv
        return m

    #function to calculate total drag from air resistance
    def set_drag(self,velocity):
        a_density=1.225
        r = self.size/2 * 10**-2    #Ball radius
        b_a = 4 * np.pi * r**2        #Ball area
        self.drag= 0.5 * self.cd * a_density * velocity * b_a
        return self.drag
    
    #Function to move ball in the x-y plane
    def move(self):
        self.y_velocity = self.y_velocity + 1/2*(-self.gravity*pow(10,-2)) #adding the effects of gravity
        ydrag=self.set_drag(self.y_velocity)
        xdrag=self.set_drag(self.x_velocity)
        self.sety(self.ycor() + self.y_velocity - ydrag)
        self.setx(self.xcor() + self.x_velocity - xdrag)

    #function to get y position
    def get_y(self):
        return self.ycor()

    #function to get x position
    def get_x(self):
        return self.xcor()

    #implementing a bounce when ball hitts floor
    def bounce_floor(self, floor_y):
        if self.ycor() < floor_y:
            ydrag=self.set_drag(self.y_velocity)
            self.y_velocity = -self.tfle_lost(self.y_velocity) + ydrag   #change direction of the ball
            self.x_velocity = self.x_velocity * (self.mu-(1-self.mu)*self.t_mass_gen())
            self.sety(floor_y)
         
    #implementing a bounce when ball hitts side walls
    def bounce_walls(self, wall_x):
        if abs(self.xcor()) > wall_x:
            xdrag=self.set_drag(self.x_velocity)
            sign = self.xcor() / abs(self.xcor())
            self.x_velocity = -self.twe_lost(self.x_velocity) + (sign*xdrag)
            self.setx(wall_x * sign)
            
if __name__== '__main__':
    # Sizes of the window
    width = 1200
    height = 600

    window = turtle.Screen()
    window.setup(width, height)     #Turtle sreen with specified height and width
    window.tracer(0)                #Turtle Screen Centre (0,0)

    #Simulation choice "graph" or "2D" simulation.
    print("If you want to generate the graph then input 'graph', if you want to generate a 2d simulation input '2D'\n")
    sim_choice=input("Input what you want to simulate: ")

    figure, axis = plt.subplots(2)


    #2D Simulation
    if (sim_choice== "2D"):
        balls = []
        def add_ball(x, y):
            balls.append(Ball(x, y))

        #adding click action to the screen (to generate a new ball)
        window.onclick(add_ball) 
        b_x=[]
        while True:
            for ball in balls:
                ball.draw()
                ball.move()
                ball.bounce_floor(-height/2+20)
                ball.bounce_walls(width/2)
            window.update()

    #graph plot simulation
    elif (sim_choice=="graph"):
        
        #Function To draw line graph
        def plt_graph(x,y,title):
            for i in range(2):
                axis[i].plot(x[i],y[i]) 
                axis[i].set_title(title[i])
            plt.subplots_adjust(left=0.1,
                            bottom=0.1, 
                            right=0.9, 
                            top=0.9, 
                            wspace=0.4, 
                            hspace=0.4)
            plt.show()

        #function to centralize data
        def centlzr(data):
            min_hs=min(data) #min height

            #New list of ascending Heights with a minimum value of 0
            new_data=[i+abs(min_hs) for i in data] 
            return new_data

        #Function to generate the graph data
        def graphSim(i):
            len=i
            y_s=[]
            t_s=[]
            b_sizes=[]
            dist_covered=[]

            while len>0:
                ycor=[]
                xcor=[]
                ball = Ball(-width/2+100,height/2-200)
                times=[]
                b_sizes.append(ball.size)
                start_time = time.time()
                
                #The following autosimulates the bouncing of one ball.
                #  Then records all the heights at respective time.
                if len==0:
                    break
                while True:
                    ball.draw()
                    ball.move()
                    ball.bounce_floor(-height/2+20)
                    ball.bounce_walls(width/2)
                    ycor.append(ball.get_y())   #record heights
                    xcor.append(ball.get_x())   #record lengths
                    current_time = time.time()
                    times.append(current_time - start_time)     #Record times
                    window.update()     #update the window
                    #condition to terminate the loop if the x and y velocity < 0.25 
                    # whose motion is almost undetectable
                    if (ball.get_y() <= -height/2+20):
                        if (ball.y_velocity<2.5*pow(10,-2) and ball.x_velocity< 2.5*pow(10,-2)):
                            break
                
                t_s.append(times)
                y_s.append(centlzr(ycor))
                dist_covered.append(max(centlzr(xcor))-min(centlzr(xcor)))
                len-=1
            return y_s,t_s, dist_covered, b_sizes

        graphsim = graphSim(20)
        heights = graphsim[0][0]
        times = graphsim[1][0]
        dist_covered = graphsim[2]
        b_size = graphsim[3]

        b_size.sort()                   # sort ball size in ascending order
        dist_covered.sort(reverse=True) # sort distance in descending order
        
        #The Matplotlib Graph Simulation
        plt_graph([times,b_size],[heights,dist_covered],
            ["Bouncing Ball Height vs Time Graphical Simulation", 
        "Bouncing Ball Distance covered vs Ball_size Graphical Simulation"],
        )
        
    else:
        #If the user inputs any other word other than "graph" or "sim", 
        # print the following and do nothing.
        print("\n!!Something is wrong please check your input and run the code again")

