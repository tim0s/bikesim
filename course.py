class Course:
  def __init__(self, length):
    self.length = length
    self.heights = []

  def from_gpx_segments(self, filename):
    import gpxpy
    import gpxpy.gpx
    import geopy.distance
    self.length = None
    self.heights = []
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)
    last = None
    total_length = 0
    for track in gpx.tracks:
      for segment in track.segments:
        for point in segment.points:
          if last is None:
            last = point
            self.add_height(0, point.elevation)
            continue
          coords_1 = (last.latitude, last.longitude)
          coords_2 = (point.latitude, point.longitude)
          dist = geopy.distance.geodesic(coords_1, coords_2).meters
          total_length += dist
          self.add_height(total_length, point.elevation)
          last = point
    self.length = total_length


  def add_height(self, pos, height):
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


