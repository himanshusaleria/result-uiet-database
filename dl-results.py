import MySQLdb
import urllib2
import urllib
import ssl
db = MySQLdbconnect(host="localhost", # your host, usually localhost
                     user="user", # your username
                      passwd="PASSWORD", # your password
                      db="DATABASE") # name of the data base

cursor = db.cursor()

url = 'https://uwp.puchd.ac.in/common/viewmarks.aspx'
key1 = "__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwUKLTMzMTUyNjUzMA9kFgJmD2QWAgIDD2QWBAIBDw8WAh4EVGV4dAUKVmlldyBNYXJrc2RkAgMPZBYCAgEPZBYCAhUPZBYEAg8PPCsADQBkAhEPPCsADQBkGAMFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYGBSBjdGwwMCRtaWRkbGVDb250ZW50JFJhZGlvQnV0dG9uRwUhY3RsMDAkbWlkZGxlQ29udGVudCRSYWRpb0J1dHRvbk5HBSFjdGwwMCRtaWRkbGVDb250ZW50JFJhZGlvQnV0dG9uTkcFIGN0bDAwJG1pZGRsZUNvbnRlbnQkUmFkaW9CdXR0b24xBSBjdGwwMCRtaWRkbGVDb250ZW50JFJhZGlvQnV0dG9uMgUgY3RsMDAkbWlkZGxlQ29udGVudCRSYWRpb0J1dHRvbjIFHWN0bDAwJG1pZGRsZUNvbnRlbnQkR3JpZFZpZXcyD2dkBR1jdGwwMCRtaWRkbGVDb250ZW50JEdyaWRWaWV3MQ9nZO7cAGc2QXOLUQaauey%2Bl91SR1Yi&__VIEWSTATEGENERATOR=F368589A&__EVENTVALIDATION=%2FwEWFQKStte1AQLKm%2F%2FKDwKwzYbXDQKxzYbXDQKyzYbXDQKzzYbXDQK0zYbXDQK1zYbXDQK2zYbXDQKnzYbXDQKozYbXDQKwzcbUDQLgzbrJDQKyqe3pBgLdzbrJDQKs9fOJAQKJ27%2BqBwLtmLvJDAL2wcuTDwL2wb%2B3BgKSyNCHBunfT8LihqgqsAWHKGWvkBRdcf8n&ctl00%24middleContent%24TextBox1=ue"
key2 = "&ctl00%24middleContent%24DropDownList1="
key3 = "&ctl00%24middleContent%24DropDownList2="
key4 = "&ctl00%24middleContent%24type=RadioButtonG&ctl00%24middleContent%24resulttype=RadioButton1&ctl00%24middleContent%24cmdsubmit=Show+Marks"
context = ssl._create_unverified_context()

def getpage(rollno,sem,course):
	data = key1 + str(rollno) + key2 + str(sem) + key3 + course + key4
	#print data
	req = urllib2.Request(url,data)
	response = urllib2.urlopen(req, context=context)
	return response.read()
for rollno in range (133001,133061):  #rollnumber range here
	for sem in range (1,4): # semester range here
		course = 'BE'  # course here
		istring = getpage(rollno,sem,course)
		i = 0
		finddata = False
		captureid = ''
		capturedata = ''
		data = []
		while i < len(istring):
			c = istring[i]
			if istring[i:i+29] == 'id="ctl00_middleContent_Label':
				i+=4
				while istring[i] != '"':
					captureid+=istring[i]
			 		finddata=True
			 		i+=1
			if finddata == True and istring[i] == '>':
				i+=1
				while istring[i] != '<':
					capturedata+=istring[i]
					i+=1
				data.append(capturedata)
				finddata=False
			capturedata = ''
			captureid = ''
			i+=1
		print data
		sgpa = data[6][-4:len(data[6])]
		data.append(sgpa)
		data[6] = data[6][7:11]
		data = '("'+data[0]+'","'+data[1]+'","'+data[2]+'","'+data[3]+'","'+data[4]+'","'+data[5]+'","'+data[6]+'","'+data[7]+'")'
		print data
		#for key, value in idNdata.iteritems() :
			#print key, ":" , value
		sql = "insert into details values" + data
		print sql

		# Prepare SQL query to INSERT a record into the database.

		try:
		   # Execute the SQL command
		   cursor.execute(sql)
		   # Commit your changes in the database
		   db.commit()
		except:
		   # Rollback in case there is any error
		   db.rollback()

		# disconnect from server
db.close()