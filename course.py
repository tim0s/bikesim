class Course:
  def __init__(self, length):
    self.length = length
    self.heights = []

  def add_height(self, pos, height):
    if (pos < 0) or (pos > self.length):
      raise ValueError("pos invalid")
    self.heights += [(pos, height)]
    self.heights = sorted(self.heights)

  def getHeightAndGrade(self, pos):
   pos_before = 0
   height_before = 0
   pos_after = 0
   height_after = 0 
   for (p,h) in self.heights:
     if p>pos:
       pos_after = p
       height_after = h
       break
     else:
       pos_before = p
       height_before = h
   grade = (height_after - height_before) / (pos_after - pos_before)
   height = height_before + (pos-pos_before)*grade
   return (height, grade)


