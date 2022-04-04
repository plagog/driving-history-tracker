#Python v3.8.10
import sys
import re
import math

class DriversData:
  def __init__(self, name):
    self._name = name
    self._totalMilesDriven = 0
    self._weightedAverageMPH = 0
    self._totalTripDuration = 0

  def setTotalMilesDriven(self,miles)->None:
    self._totalMilesDriven = miles
  
  def getTotalMilesDriven(self)->float:
    return self._totalMilesDriven

  def setWeightedAverageMPH(self,mph)->None:
    self._weightedAverageMPH = mph
  
  def getWeightedAverageMPH(self)->float:
    return self._weightedAverageMPH

  def setTotalTripDuration(self,minutes)->None:
    self._totalTripDuration = minutes
  
  def getTotalTripDuration(self)->int:
    return self._totalTripDuration
  
  def __repr__(self)->str:
    if self._totalMilesDriven > 0:
      return '{0}: {1} miles @ {2} mph'.format(self._name,round(self._totalMilesDriven),round(self._weightedAverageMPH))
    else:
      return '{0}: 0 miles'.format(self._name)

#receives array of str
#if length of array is equal to 2 and the first element is equal to "Driver" returns True
#False otherwise
def isValidDriverCommand(lineArray:"list[str]")->bool:
  command = lineArray[0]
  if len(lineArray) == 2 and command == "Driver":
    return True
  return False

#receives array of str
#if length of array is equal to 5 and the first element is equal to "Trip" returns True
#False otherwise
def isValidTripCommand(lineArray:"list[str]")->bool:
  command = lineArray[0]
  if len(lineArray) == 5 and command == "Trip":
    return True
  return False

#receives dictionary of key->value and driver of type str
#if driver is a key in dictionary returns True, False otherwise
def isRegisteredDriver(DRIVERS_HISTORY_MAP:"dict[str,DriversData]",driver:str)->bool:
  if DRIVERS_HISTORY_MAP.get(driver):
    return True
  return False 

#receives time as str
#checks whether str is in format "hh:mm" where h is a single digit int and m is a single digit int
#if true returns True, False otherwise
def isValidTime(time:str)->bool:
  if re.match(r"^([0-9]|[0-1]?[0-9]|2[0-3]):[0-5][0-9]$",time):
    return True
  return False

#receives a float
#returns True if miles is a finite positive float, False otherwise
def isValidMiles(miles:float)->bool:
  if type(miles) != str and miles > 0:
    return True
  return False

#receives dictionary of type str->DriversData key-values, driver of type str
#creates DriversData object
#assigns DriversDataObject to Dictionary with driver as key
def registerDriver(DRIVERS_HISTORY_MAP:"dict[str,DriversData]",driver:str)->None:
  DRIVERS_HISTORY_MAP[driver] = DriversData(driver)

#receives startTime and stopTime as strings in "hh:mm" format where h is a single digit int representing an hour and m a minute
#converts startTime and stopTime to ints that represent minutes
#returns the difference of startTime from stopTime if it's positive, 0 otherwise.
def computeTripDuration(startTime:str, stopTime:str)->int:
  startTimeArray = startTime.split(":")
  stopTimeArray = stopTime.split(":")
  startHours = int(startTimeArray[0])
  startMinutes = int(startTimeArray[1])
  endHours = int(stopTimeArray[0])
  endMinutes = int(stopTimeArray[1])
  minutCountAtStart = 60 * startHours + startMinutes
  minuteCountAtStop = 60 * endHours + endMinutes
  duration = minuteCountAtStop - minutCountAtStart
  if (duration > 0): 
    return duration
  return 0

#receives miles (float) representing a distance and duration representing the time spent to drive that distance
#if both are positive numbers calculate and return average mph
#return 0 otherwise
def computeAverageMPH(miles:float, duration:int)->float:
  if duration and miles and math.isfinite(duration) and math.isfinite(miles) and duration > 0 and miles > 0:
    return (miles / duration) * 60
  return 0

#receives durations and avg mph for two trips
#calculates the average mph by creating weights based on each duration compared to the total duration
def computeWeightedAverageMPH(duration1:int, avgMPH1:float, duration2:int, avgMPH2:float)->float:
  totalDuration = duration1 + duration2
  if totalDuration <= 0: return 0
  weight1 = duration1 / totalDuration
  weight2 = duration2 / totalDuration
  weightedMPH = weight1 * avgMPH1 + weight2 * avgMPH2
  return weightedMPH
       
#receives DRIVERS_HISTORY_MAP dictionary (dict[str,DriversData]), driver (str), tripDuration(int), avgMPH(float), miles(float)
#retrieves DriversData object associated with 'driver'
#calculates the new weighted average mph so far
#updates miles,duration and average mph attributes
def addDriversData(DRIVERS_HISTORY_MAP:"dict[str,DriversData]",driver:str,tripDuration:int,avgMPH:float,miles:float)->None:
  driversData = DRIVERS_HISTORY_MAP[driver]
  currentTotalTripDuration = driversData.getTotalTripDuration()
  currentWeightedAverageMPH = driversData.getWeightedAverageMPH()
  newWeightedAverageMPH = computeWeightedAverageMPH(tripDuration,avgMPH, currentTotalTripDuration,currentWeightedAverageMPH)
  driversData.setWeightedAverageMPH(newWeightedAverageMPH)
  driversData.setTotalMilesDriven(driversData.getTotalMilesDriven() + miles)
  driversData.setTotalTripDuration(currentTotalTripDuration + tripDuration)

#receives dictionary with key->value
#sorts dictionary based on value.totalMilesDriven
#prints value
def orderAndPrintReport(DRIVERS_HISTORY_MAP:"dict[str,DriversData]")->None:
  for driversData in sorted(DRIVERS_HISTORY_MAP.values(), key=lambda driversData: driversData.getTotalMilesDriven(),reverse=True):
    print(driversData)

# Extra function for math logic verification
# receives DRIVERS_HISTORY_MAP dictionary
# checks if totalDuration (in hours) of each object is equal to totalMilesDriven divided by the avgMPH
# prints "Something doesn't add up" if they are not equal
def validateData(DRIVERS_HISTORY_MAP:"dict[str,DriversData]"):
  for key,value in DRIVERS_HISTORY_MAP.items():
    if (value._weightedAverageMPH != 0):
      if (round(value._totalMilesDriven/value._weightedAverageMPH) != round(value._totalTripDuration/60)):
        print("Something doesn't add up")
    if (key != value._name):
      print("Invalid Registration")


def main():
  input_file = open(sys.argv[1],'r')
  DRIVERS_HISTORY_MAP = dict({})
  for line in input_file:
    lineArray = line.split()
    if len(lineArray) < 2: continue
    driver = lineArray[1]
    if isValidDriverCommand(lineArray) and not isRegisteredDriver(DRIVERS_HISTORY_MAP,driver):
      registerDriver(DRIVERS_HISTORY_MAP,driver)
    elif isValidTripCommand(lineArray) and isRegisteredDriver(DRIVERS_HISTORY_MAP,driver):
      startTime = lineArray[2]
      stopTime = lineArray[3]
      try: miles = float(lineArray[4])
      except: continue
      if not isValidMiles(miles): continue
      if not isValidTime(startTime): continue
      if not isValidTime(stopTime): continue
      tripDuration = computeTripDuration(startTime, stopTime)
      avgMPH = computeAverageMPH(miles, tripDuration)
      if avgMPH < 5 or 100 < avgMPH or tripDuration <= 0: continue
      addDriversData(DRIVERS_HISTORY_MAP,driver,tripDuration,avgMPH,miles)
      
  input_file.close()
  orderAndPrintReport(DRIVERS_HISTORY_MAP)
  validateData(DRIVERS_HISTORY_MAP)






###################################################
###################################################
###################################################
#######################TESTS#######################
###################################################
###################################################
###################################################

def test_isValidDriverCommand():
  #array will always either be empty or consist of non-empty strings
  array = ["Driver", "Panos"]
  falseArrays = [
    ["Driver","Panos","a"],
    ["Driver","",""],
    ["Driverr","Panos"],
    ["driver","Panos"],
    ["driveR","Panos"],
    ["Trip","a","b","c","d"]
  ]
  assert isValidDriverCommand(array) == True, "Should be True"
  for array in falseArrays:
    assert isValidDriverCommand(array) == False, "Should be False" 
  
def test_isValidTripCommand():
  #array will always either be empty or consist of non-empty strings
  trueArrays = [
    ["Trip","Panos","04:03","3:23","22"],
    ["Trip","Any","04:03","3:23","22"],
    ["Trip","123","1","s","d"]
  ]
  falseArrays = [
    ["Driver","Panos","04:03","3:23","22"],
    ["Trip","a","b","c"],
    ["Driver","Panos"],
    ["Trip","Panos"],
    ["Trip","a","b"]
  ]
  for array in trueArrays:
    assert isValidTripCommand(array) == True, "Should be True"
  for array in falseArrays:
    assert isValidTripCommand(array) == False, "Should be False"

def test_isRegisteredDriver():
  #name will always be a non-empty string
  registeredNames = ["John","123","a"]
  nonRegisteredNames = ["Jimmy","13","A","b"]
  MAP = dict({})
  for name in registeredNames:
    driversHistoryObject = DriversData(name)
    MAP[name] = driversHistoryObject
    assert isRegisteredDriver(MAP,name) == True, "Should be True"

  for name in nonRegisteredNames:
    assert isRegisteredDriver(MAP,name) == False, "Should be False"  

def test_isValidTime():
  validTimes = ["00:00","23:59","3:59"]
  invalidTimes = ["00:60","24:00","24:0","24:5","-24:00","AB:CD","**:**","ab:cd","abcd","","0000",""]
  for time in validTimes:
    assert isValidTime(time) == True, "Should be True"
  for time in invalidTimes:
    assert isValidTime(time) == False, "Should be False"

def test_isValidMiles():
  validMiles = [5,1,0.1]
  invalidMiles = [float("nan"), -5,0,-0.1,"abc"]
  for miles in validMiles:
    assert isValidMiles(miles) == True, "Should be True"
  for miles in invalidMiles:
    assert isValidMiles(miles) == False, "Should be False"

def test_computeTripDuration():
  #startTime and stopTime will always be a string with the format "NN:NN" when N is a number
  #computeTripDuration(startTime,stopTime)
  assert computeTripDuration("00:00","00:10") == 10, "Should be 10"
  assert computeTripDuration("13:10","15:15") == 125, "Should be 125"
  assert computeTripDuration("15:15","15:10") == 0, "Should be 0"
  assert computeTripDuration("15:15","15:15") == 0, "Should be 0"
  assert computeTripDuration("15:15","15:15") == 0, "Should be 0"

def test_computeAverageMPH():
  #miles will always be a float
  #duration will always be a non-negative integer
  #computeAverageMPH(miles, duration)
  assert computeAverageMPH(0, 0) == 0, "Should be 0"
  assert computeAverageMPH(10, 0) == 0, "Should be 0"
  assert computeAverageMPH(0, 10) == 0, "Should be 0"
  assert computeAverageMPH(None, 40) == 0, "Should be 0"
  assert computeAverageMPH(40, None) == 0, "Should be 0"
  assert computeAverageMPH(None, None) == 0, "Should be 0"
  assert computeAverageMPH(50, 60) == 50, "Should be 50"
  assert computeAverageMPH(10, 10) == 60, "Should be 60"
  assert computeAverageMPH(150, 120) == 75, "Should be 75"

def test_computeWeightedAverageMPH():
  #avgMPH will always be a non-negative float
  #durations will always be non-negative integers
  #computeWeightedAverageMPH(duration1,avgMPH1,duration2,avgMPH2)
  assert computeWeightedAverageMPH(60, 30, 30, 15) == 25, "Should be 25"
  assert computeWeightedAverageMPH(0, 30, 30, 17) == 17, "Should be 17"
  assert computeWeightedAverageMPH(30, 12, 0, 30) == 12, "Should be 12"
  assert computeWeightedAverageMPH(0, 30, 0, 30) == 0, "Should be 0"
  assert computeWeightedAverageMPH(0, 0, 0, 0) == 0, "Should be 0"
  assert computeWeightedAverageMPH(15, 0, 120, 0) == 0, "Should be 0"
  
if __name__ == "__main__":
  test_isRegisteredDriver()
  test_isValidTripCommand()
  test_isValidDriverCommand()
  test_isValidTime()
  test_isValidMiles()
  test_computeTripDuration()
  test_computeAverageMPH()
  test_computeWeightedAverageMPH()

main()