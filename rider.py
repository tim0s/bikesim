class Rider:
  def __init__(self, name, mass=70, frontalArea=0.32, dragCoeff=0.88, driveEfficiency=0.97, CdA=None):
    self.name = name
    self.mass = mass
    self.velocity = 0
    self.position = 0
    self.frontalArea = frontalArea
    self.dragCoeff = dragCoeff
    self.CdA = CdA
    self.driveEfficiency = driveEfficiency

  def getCdA(self):
    if self.CdA is not None:
      return self.CdA
    return self.frontalArea * self.dragCoeff

  def getCurrentPower(self):
    return 300


