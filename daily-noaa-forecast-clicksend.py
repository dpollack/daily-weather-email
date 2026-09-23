from __future__ import print_function
import sys
import re
import urllib.request
import datetime

# import sendgrid librarires
import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException

# get string name for tomorrows day
tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
tomorrowday = tomorrow.strftime("%A")

# fetch the local weather URL from NOAA
url = 'https://forecast.weather.gov/MapClick.php?lat=38.9386&lon=-77.3957&unit=0&lg=english&FcstType=text&TextType=1'
html = urllib.request.urlopen(url)
doc = html.read().decode()

# open the email message file - fix this with a lock/open later
f = open("weatherfile", "w")

# split on line HTML line breaks to get separate days and look through the days for today and the next days weather
parts = doc.split("<br>")

# split on <b> and <br> html tags to remove them
for each in parts:
    lines = each.split("<br>")
    if re.search('Today', lines[0]):
        weatherdesc = lines[0].split("<b>")
        daydesc = weatherdesc[1].split("</b>")
        #print (daydesc[0] + daydesc[1])
        f.write(daydesc[0] + daydesc[1])
        f.write("\n")

    if re.search('Tonight', lines[0]):
        weatherdesc = lines[0].split("<b>")
        nightdesc = weatherdesc[1].split("</b>")
        #print (nightdesc[0] + nightdesc[1])
        f.write(nightdesc[0] + nightdesc[1])
        f.write("\n")

    if re.search(tomorrowday, lines[0]):
        tomweatherdesc = lines[0].split("<b>")
        tomdesc = tomweatherdesc[1].split("</b>")
        #print (tomdesc[0] + tomdesc[1])
        f.write(tomdesc[0] + tomdesc[1])

# close the email message file - fix this with a unlock/close later
f.close()

# set SMS body
with open('weatherfile') as fd:
    msgbody = fd.read()

# Configure HTTP basic authorization: BasicAuth
configuration = clicksend_client.Configuration()
configuration.username = 'danpollack@gmail.com'
configuration.password = '3111A0A7-CFD2-55F1-536A-E239E308A931'

# create an instance of the API class
api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))

# If you want to explictly set from, add the key _from to the message.
sms_message = SmsMessage(source="sdk", body=msgbody, to="+17039016464")

sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])

try:
    # Send sms message(s)
    api_response = api_instance.sms_send_post(sms_messages)
    #print(api_response)
except ApiException as e:
    print("Exception when calling SMSApi->sms_send_post: %s\n" % e)
