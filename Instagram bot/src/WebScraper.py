import json

def findJson(data ,startTag, endTag):
	returnData = ''
	startStringFound = False
	startIndex = findString(data, startTag)['endIndex'] + 1
	endIndex = findString(data, endTag)['startIndex']

	i = startIndex
	while i < endIndex:
		returnData += data[i]
		i += 1
		
	return json.loads(returnData)	

def findText(data ,startTag, endTag):
	returnData = ''
	startStringFound = False
	startIndex = findString(data, startTag)['endIndex'] + 1
	endIndex = findString(data, endTag)['startIndex']

	i = startIndex
	while i < endIndex:
		returnData += data[i]
		i += 1

	return str(returnData)	
			
def findString(data, tag):
	i = 0
	j = 0
	startIndex = -1
	endIndex = -1
	search = True
	found = False

	while search:
		j = i
		found = True

		if (i + (len(tag)-1)) < (len(data)):
			for char in tag:
				if char == data[j]:
					if startIndex == -1:
						startIndex = j
					j += 1
				else:
					found = False
					startIndex = -1
		else:
			search = False
			found = False
			startIndex = -1
			endIndex = -1

		if found:
			search = False
			endIndex = startIndex + (len(tag)-1)
		else:
			startIndex = -1
			endIndex = -1

		i += 1

	return {'startIndex' : startIndex, 'endIndex' : endIndex}