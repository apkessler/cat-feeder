#!usr/bin/env python

import sys
import datetime
import os
import json
import feedController
import argparse

def main():

	if (sys.version_info[0] < 3):
		print ("This requires Python3!")
		return

	parser = argparse.ArgumentParser(description='Run the automatic food dispenser.')
	parser.add_argument('jsonFile', help='A JSON file with mealtimes.')
	args=parser.parse_args()


	jsonData = json.loads(open(args.jsonFile, 'r', encoding='UTF-8').read().replace('\n',''))


	controller = feedController.FeedController()

	for meal in jsonData["data"]:
		controller.addMeal(meal["name"], meal["time"], meal["servings"])
	
	print("Registered meals:")
	for meal in controller.mealList:
		print(meal)		


	print("Starting state machine!")
	
	while (1):
		controller.update()



if __name__ == '__main__':
	main()


















