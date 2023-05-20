import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from rider import Rider
from course import Course

class Params:
  def __init__(self):
    self.dt = 0.1 # timestep length in seconds


class Environment:
  def __init__(self, rho=1.2, g=9.81):
    self.rho = rho
    self.g = g


class Simulation:
  def __init__(self, course, environment=Environment(), params=Params(), riders=[]):
    self.env = environment
    self.riders = riders
    self.course = course
    self.params = params
    self.iter = 0

  def conv(self, from_units, to_units, value):
    if from_units == "m/s" and to_units == "km/h":
      return (value * 60 * 60) / 1000.0
    else:
      raise ValueError("Conversion from %s to %s not implemented" % (from_units, to_units))

  def addRider(self, rider):
    self.riders += [rider]

  def print_header(self, outfile):
    header_elems = ["Iter", "Time"]
    for rider in self.riders:
      rider_elems = ["position", "velocity", "power", "grade", "height"]
      for elem in rider_elems:
        header_elems += [ rider.name + "_" + elem ]
    for he in header_elems:
      print("%-16.15s" % he, end="", file=outfile)
    print("", file=outfile)

  def print_state(self, outfile):
    values = [self.iter, self.iter*self.params.dt] 
    for rider in self.riders:
      height, grade = self.course.getHeightAndGrade(rider.position)
      rider_values = [rider.position, self.conv("m/s", "km/h", rider.velocity), rider.getCurrentPower(), grade, height]
      values += rider_values
    for v in values:
      print("%-16.6f"% v, end="", file=outfile)
    print("", file=outfile)


  def done(self):
    # Simulation is done when all riders are done
    for r in self.riders:
      if r.position < self.course.length:
        return False
    return True


  def timestep(self):
    self.iter += 1
    for rider in self.riders:
      totalForce = self.fDrag(rider) + self.fGravity(rider, self.course)
      powerUsed = totalForce * rider.velocity / rider.driveEfficiency
      netPower = rider.getCurrentPower() - powerUsed
      rider.v_new = math.sqrt(rider.velocity*rider.velocity+2*netPower*self.params.dt*rider.driveEfficiency / rider.mass)
    for rider in self.riders:
      new_position = rider.position + self.params.dt*(rider.velocity+rider.v_new)/2.0;
      if new_position > self.course.length:
        rider.position = self.course.length
        rider.velocity = 0.0
      else:
        rider.position = new_position
        rider.velocity = rider.v_new
      
  def fDrag(self, rider):
    return 0.5*self.env.rho*rider.getCdA()*rider.velocity*rider.velocity

  def fGravity(self, rider, course):
    height, grade = course.getHeightAndGrade(rider.position)
    return self.env.g*math.sin(math.atan(grade))*rider.mass


if __name__ == "__main__":
  course = Course(20000)
  course.from_gpx_segments('ride.gpx')
  rider1 = Rider(name="Alice", mass=70)
  sim = Simulation(course=course, riders=[rider1])

  with open("out.dat", "w") as outfile:
    sim.print_header(outfile)
    while (not sim.done()):
      sim.print_state(outfile)
      sim.timestep()
  
  df = pd.read_csv("out.dat", sep="\s+")
  figure, axis = plt.subplots(2, 2)
  axis[0,0].set_title("Course Elevation")
  df.plot(kind='line',x='Alice_position',y='Alice_height',ax=axis[0, 0])
  axis[0,1].set_title("Velocity")
  df.plot(kind='line',x='Alice_position',y='Alice_velocity',ax=axis[0, 1])
  axis[1,0].set_title("Gradient")
  df.plot(kind='line',x='Alice_position',y='Alice_grade',ax=axis[1, 0])
  axis[1,1].set_title("Power output")
  df.plot(kind='line',x='Alice_position',y='Alice_power',ax=axis[1, 1])


  plt.show()
 
