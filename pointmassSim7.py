print(' ')
import random as rand
import math
import numpy as np

## Class MASS framework
class Mass(object): #Mass template object
    def __init__(self, i):
        # SET MASS
        if (i==0):
            self.mass = 100#rand.uniform(100,1000) #generate mass; random number between 0,10
        if (i==1):
            self.mass = 50
        if (i==2):
            self.mass = 1

        # SET POSITION
        posit = 400 #range of possible positions
        self.position = np.random.uniform(-posit,posit,3)  #generate X position; random number between 0,1


    def CalcAccel(self):   #CALCULATE ACCERATION DUE TO OTHER OBJECTS
        self.acceleration = np.array([0.,0.,0.])
        self.UE = 0
        for massindex in range(masses):  #go through each objec to find accel from that object
            self.totalaccel = 0
            nam = objlist[massindex]  #find object
            if nam.mass != self.mass:
                diff = nam.position - self.position
                radius = np.linalg.norm(diff) #find the difference in the X positions
                preradius = radius**2
                epsilon = .7 #softening factor
                self.totalaccel = nam.mass/(preradius + epsilon) #find the total amount of acceleration
                self.acceleration +=  self.totalaccel*diff/radius # Calculate acceleration in x-direction
                self.UE = self.UE - self.totalaccel*radius*self.mass       

    def InitVelo(self):
        xyrad = math.sqrt(self.position[0]**2 + self.position[1]**2) #calculate the distance away from center if in xy plane
        totalvelocity = math.sqrt(xyrad*self.totalaccel) #calculate velocity needed given radius and acceleration (v**2/r = a)
        self.velocity = np.array([rand.uniform(0,1),rand.uniform(0,1), rand.gauss(0,.05)])#totalvelocity*self.Yposition/(xyrad) #velo in x direction given by total velo/ (slope^2+1)

    def CalcVelo(self): #CALCULATE CHANGE IN VELOCITY
        self.velocity = self.velocity + self.acceleration*dtime # vf = vi + At

    def CalcPos(self): #CALCULATE CHANGE IN POSITION
        self.position = self.position + self.velocity*dtime + (dtime**2)*(self.acceleration)/2 #Xf = Xi + Vt + .5at^2

    def calcKE(self):
        v = np.linalg.norm(self.velocity)
        KE = .5*self.mass*v
        return KE

#Constants
masses = 3  #number of masses
rand.seed(86) #make results somewhat consistant
dtime = .2 #resolution for time interval
total_time = 100.0 # "length of time" simulaiton will run for
iterations = int(total_time/dtime) #number of cycles checked
size = 1000
## Generate objects
objlist = [Mass(i) for i in range(masses)] # Create a list of point masses
DATA = np.array(["masses", masses, "total_time", total_time,"dtime",dtime,"size",size])
DATA_FILE = '../frames10/SIMULATION_SPEC.npy'
np.save(DATA_FILE,DATA)
## Use objects
for i in range(masses): #Give initial conditions
    objlist[i].CalcAccel() #Calculate initial Acceleration
    objlist[i].InitVelo() #Calculate initial Velocity

#fig = plt.figure(figsize=(12,6))
KE = []
UE = []
x = np.zeros(masses)
y = np.zeros(masses)
z = np.zeros(masses)
times = []
for t in range(iterations):

    KEsum = 0
    UEsum = 0

    for i in range(masses):   #find Caracteristics for each particle
        objlist[i].CalcPos()  #calculate position
        objlist[i].CalcAccel()  #calculate acceleration
        objlist[i].CalcVelo() #calculate velocity
        #objlist[i].CheckBoundries(objlist[i].Xposition,objlist[i].Yposition,objlist[i].Zposition,size)

        # Add position values to array
        x[i] = objlist[i].position[0] #update x position
        y[i] = objlist[i].position[1] #update y position
        z[i] = objlist[i].position[2] #update z position
        #if t%10 == 0:
        #    KEsum = KEsum + objlist[i].calcKE()
        #    UEsum = UEsum + objlist[i].UE

    #plotting each data point
    if t%10 == 0:
        #KE.append(KEsum)
        # print "KE: ", KEsum, "UE: ",UEsum
        # UE.append(UEsum/2)
        times.append(t)
        #print(KE)

        #fig = plt.figure(figsize=(6,6))
        # ax=fig.add_subplot(1, 1, 1, projection='3d')
        # ax.scatter(x, y, z,'ro')
        # ax.view_init(elev = 45, azim = (t%2)*5+45)
        # ax.set_xlabel('X-Axis')
        # ax.set_ylabel('Y-Axis')
        # ax.set_zlabel('Z-Axis')

        # ax.set_xlim3d(-size,size);
        # ax.set_ylim3d(-size,size);
        # ax.set_zlim3d(-size,size);

        # ax1=fig.add_subplot(1, 2, 2)
        # line = ax1.plot(times,KE,'r-',times,UE,'b-',times,[a+b for a,b in zip(KE,UE)],'g-')
        # ax1.axis([0,iterations,0,1000])
        # ax1.plot() 

        namex = '../frames10/' + 'x' + '0'*(4-len(str(t/10))) + str(t/10) + '.npy'
        namey = '../frames10/' + 'y' + '0'*(4-len(str(t/10))) + str(t/10) + '.npy'
        namez = '../frames10/' + 'z' + '0'*(4-len(str(t/10))) + str(t/10) + '.npy'
        np.save(namex, x)
        np.save(namey, y)
        np.save(namez, z)

        #plt.savefig(name)
        #plt.show()
