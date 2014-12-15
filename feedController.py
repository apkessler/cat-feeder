


from enum import Enum
import datetime

class State(Enum):
	 WAITING_FOR_MEALTIME = 0
	 WAITING_FOR_TRIGGER_RELEASE = 1
	 WAITING_FOR_TRIGGER_PUSH = 2
	 WAITING_FOR_CATS_TO_SHOW = 3
	 WAITING_FOR_DAY_TO_END = 4
	 ERROR = 5

class Meal():

	def __init__(self, name, hour, servings):
		self.name = name
		self.time = datetime.time(int(hour[0:2]), int(hour[2:4]),  0)
		self.servings = servings

	def __str__(self):
		return self.name + ' @ ' + str(self.time) + ' x' + str(self.servings)


class FeedController():
	"""docstring for FeedController"""

	  

	def __init__(self):
		
		self.currentState = State.WAITING_FOR_DAY_TO_END
		self.mealIndex = 0
		self.mealList = []
		self.catWaitTime = datetime.timedelta(minutes=1)
		self.lastDate = datetime.date.today()

	def update(self):
		if (self.currentState == State.WAITING_FOR_MEALTIME):
			if ( timeNow() > self.mealList[self.mealIndex].time):
				#Its time to feed!
				print("Starting " + self.mealList[self.mealIndex].name)
				
				setMotorState(1)
				self.currentState = State.WAITING_FOR_TRIGGER_RELEASE
				self.nRotations = 0


		elif (self.currentState == State.WAITING_FOR_TRIGGER_RELEASE):
			
			if (isTriggerPushed() == False):
				print("Trigger released!")
				self.currentState = State.WAITING_FOR_TRIGGER_PUSH


		elif (self.currentState == State.WAITING_FOR_TRIGGER_PUSH):
			if (isTriggerPushed() == True):

				self.nRotations +=1 
				print("Trigger pushed: %d rotations completed." % self.nRotations)
		
				if (self.nRotations == self.mealList[self.mealIndex].servings):
					setMotorState(0)
					self.currentState = State.WAITING_FOR_CATS_TO_SHOW
					print("Done feeding - waiting for the cats.")
					endTime = (datetime.datetime.now() + self.catWaitTime).time()
				else:
					#More servings needed!
					self.currentState = State.WAITING_FOR_TRIGGER_RELEASE
					print("Starting another rotation...")

		elif (self.currentState == State.WAITING_FOR_CATS_TO_SHOW):
			if (timeNow() > endTime):
				##TAKE PICTURE, EMAIL
				print("Taking picture!")
				#Increment to next meal
				self.mealIndex += 1

				if (self.mealIndex >= len(self.meanList)):
					currentState = State.WAITING_FOR_DAY_TO_END
					self.lastDate = datetime.date.today()
					print("All done feeding for today- waiting until tomorrow.")
				else:
					currentState = State.WAITING_FOR_MEALTIME
					print("Next meal today will be " + str(self.mealList[self.mealIndex]))

		elif (self.currentState == State.WAITING_FOR_DAY_TO_END):

			if (self.lastDate != datetime.date.today()):
				self.currentState = State.WAITING_FOR_MEALTIME
				self.mealIndex = 0
				print("Its a new day! The first meal will be " + str(self.mealList[0]))
		
		else:
			print ("Error!")

	def addMeal(self, name, hour, servings):
		meal = Meal(name, hour, servings)
		self.mealList.append(meal)
		#print("Adding to list: " + str(meal))

#Return whether or not sense button is pushed...
def isTriggerPushed():
	return True 

#Turn motor on/pff
def setMotorState(m):
	if (m == 1):
		print("Motor turned on!")
	else:
		print("Motor turned off!")
	

def timeNow():
	return datetime.datetime.now().time()