import sys
import re
import urllib.request
import datetime
import smtplib
from email.message import EmailMessage

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
    if re.search('To', lines[0]):
        weatherdesc = lines[0].split("<b>")
        daydesc = weatherdesc[1].split("</b>")
        #print (daydesc[0] + daydesc[1])
        f.write(daydesc[0] + daydesc[1])
        f.write("\n")

    if re.search(tomorrowday, lines[0]):
        tomweatherdesc = lines[0].split("<b>")
        tomdesc = tomweatherdesc[1].split("</b>")
        #print (tomdesc[0] + tomdesc[1])
        f.write(tomdesc[0] + tomdesc[1])

# close the email message file - fix this with a unlock/close later
f.close()

# Send the email
with open('weatherfile') as fd:
# Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fd.read())

msg['Subject'] = '[the subject]' # customize subject 
msg['From'] = '[sender]' # customize sender
msg['To'] = '[recipient]' # customize recipient

# connect to local MTA and send
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
