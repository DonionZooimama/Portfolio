import sys
from datetime import datetime

argList = sys.argv

if len(argList) <= 1 or argList[1] == 'help':
	print('HELP')
	print('\tGet info from start of file to end of file')
	print('\texample: userinfo.py username\n')
	print('\tGet info from input date')
	print('\texample: userinfo.py username [input date dd/mm/yy]\n')
	print('\tGet info from a start date to end date')
	print('\texample: userinfo.py username [start date dd/mm/yy] [end date dd/mm/yy]\n')
	print('\tOptions')
	print("\ttoday - uses today's date")
	print("\tyesterday - uses yesterday's date\n")
	print("\texample: userinfo.py username yesterday today")
	print("\twill return all the info the happened from yesterday till today\n")

else:
	username = argList[1]

	try:
		startDate = argList[2]
	except:
		startDate = None
	try:
		endDate = argList[3]
	except:
		endDate = None

	currentDateTime = str(datetime.now())
	splitBySpace = currentDateTime.split(' ')
	date = splitBySpace[0].split('-')
	year = date[0]
	month = date[1]
	day = date[2]

	if startDate == 'today' or startDate == 'yesterday':
		if startDate == 'today':
			startDate = int(date[0]) + int(date[1]) + int(date[2])
		else:
			startDate = int(date[0]) + int(date[1]) + int(date[2]) - 1
	elif startDate != None:
		startDate = int(startDate.split('/')[0]) + int(startDate.split('/')[1]) + int(startDate.split('/')[2])

	if endDate == 'today' or endDate == 'now' or endDate == 'yesterday':
		if endDate == 'today' or endDate == 'now':
			endDate = int(date[0]) + int(date[1]) + int(date[2])
		else:
			endDate = int(date[0]) + int(date[1]) + int(date[2]) - 1
	elif endDate != None:
		endDate = int(endDate.split('/')[0]) + int(endDate.split('/')[1]) + int(endDate.split('/')[2])


	print ('-')*80

	directory = 'users/' + username + '/'

	f = open(directory + "logs.csv","r")

	csvList = [];
	for lines in f:
		tempList = lines.split(',')
		csvList.append(tempList)

	errors = 0
	errorsList = []
	follows = 0
	unfollows = 0
	likes = 0

	
	if startDate != None and endDate != None:
		for log in csvList:
			currentdate = int(log[0]) + int(log[1]) + int(log[2])
			if currentdate >= startDate and currentdate <= endDate:
				if log[6] == 'success':
					if log[7] == 'follow':
						follows += 1
					elif log[7] == 'unfollow':
						unfollows += 1
					elif log[7] == 'like':
						likes += 1
				else:
					errors += 1
					errorsList.append(log)
		print('Followed: ' + str(follows) + ' users')
		print('Unfollowed: ' + str(unfollows) + ' users')
		print('Liked: ' + str(likes) + ' pictures')
		print('Errors: ' + str(errors))
		if errors > 0:
			print('\nHere are the logs:')
			for error in errorsList:
				formattedDate = '['+ error[0] + '/' + error[1] + '/' + error[2] + ' ' + error[3] + ':' + error[4] + ':'+ error[5] + ']'
				print (formattedDate + "Error when action '" + error[7] + "' was preformed. Error code: " + error[8][:-1])
	elif startDate != None:
		for log in csvList:
			currentdate = int(log[0]) + int(log[1]) + int(log[2])
			if currentdate == startDate:
				if log[6] == 'success':
					if log[7] == 'follow':
						follows += 1
					elif log[7] == 'unfollow':
						unfollows += 1
					elif log[7] == 'like':
						likes += 1
				else:
					errors += 1
					errorsList.append(log)
		print('Followed: ' + str(follows) + ' users')
		print('Unfollowed: ' + str(unfollows) + ' users')
		print('Liked: ' + str(likes) + ' pictures')
		print('Errors: ' + str(errors))
		if errors > 0:
			print('\nHere are the logs:')
			for error in errorsList:
				formattedDate = '['+ error[0] + '/' + error[1] + '/' + error[2] + ' ' + error[3] + ':' + error[4] + ':'+ error[5] + ']'
				print (formattedDate + "Error when action '" + error[7] + "' was preformed. Error code: " + error[8][:-1])
	else:
		for log in csvList:
			if log[6] == 'success':
				if log[7] == 'follow':
					follows += 1
				elif log[7] == 'unfollow':
					unfollows += 1
				elif log[7] == 'like':
						likes += 1
			else:
				errors += 1
				errorsList.append(log)
		print('From file creation till now\n')
		print('Followed: ' + str(follows) + ' users')
		print('Unfollowed: ' + str(unfollows) + ' users')
		print('Liked: ' + str(likes) + ' pictures')
		print('Errors: ' + str(errors))
		if errors > 0:
			print('\nHere are the logs:')
			for error in errorsList:
				formattedDate = '['+ error[0] + '/' + error[1] + '/' + error[2] + ' ' + error[3] + ':' + error[4] + ':'+ error[5] + ']'
				print (formattedDate + "Error when action '" + error[7] + "' was preformed. Error code: " + error[8][:-1])

	print ('-')*80