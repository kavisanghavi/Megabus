
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import calendar
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date


cal= calendar.Calendar()
count=0
#Enter the start Year
year=date.today().year
#Enter the start month
month=date.today().month
output=""
prices=[]
dates=[]
while count<5:
    for day in cal.itermonthdates(year,month):
        date = day.strftime('%Y-%m-%d')
        name=calendar.day_name[day.weekday()]
        #Enter the days for which you want to Search
        days=["Friday","Saturday"]
        if name not in days:
            continue
        url="https://us.megabus.com/journey-planner/journeys?days=1&concessionCount=0&departureDate="+date+"&destinationId=123&inboundDepartureDate="+date+"&inboundOtherDisabilityCount=0&inboundPcaCount=0&inboundWheelchairSeated=0&nusCount=0&originId=95&otherDisabilityCount=0&pcaCount=0&totalPassengers=1&wheelchairSeated=0"
        options = Options()
        options.headless = True
        driver = webdriver.Chrome('D:\imagecrawler\chromedriver.exe',options=options)
        driver.get(url)
        try:
            soup=BeautifulSoup(driver.page_source, 'lxml')
            cheapest = soup.find("div", {"class": "panel panel-default ticket ng-tns-c9-1 cheapest ng-star-inserted"})
            price = cheapest.find("div",{"class":"col-xs-4 ticket__price"})
            output+=date +" "+name +": "+ price.text + "\n"
            x=float(price.text[1:])
            prices.append(x)
            dates.append(date)
        except:
            driver.quit()
    if(month%12==0):
        month=1
        year=2019
    else:
        month=month+1
    count+=1

minpos = prices.index(min(prices))
message="Subject: The Cheapest bus found on " + dates[minpos] + " at $"+ str(min(prices)) +"\n"

email = 'Enter your Email'
password = 'Enter your Password'
send_to_email = 'Whom do you want to send the whole list?'
subject = message
message2 = output

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject

msg.attach(MIMEText(message2, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)
text = msg.as_string()
server.sendmail(email, send_to_email, text)
server.quit()


