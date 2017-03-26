## See Jupiter Notebook:
## https://apsportal.ibm.com/analytics/notebooks/c29364f4-5804-4587-b29b-22aa35e4ed8b/view?access_token=94cf83c757ec699c339a44b37e7dfb36dbed242f8ccdbfafe07bfc808ceadade

## Generate promotion based on weather

import random

indoorPromotions = ["10% off Arrival movie ticket"]
outdoorPromotions = ["15% off Bruno Mars concert"]

def getPromotionMessage(willRain, userInCrisis, userFriend):
    template = "Congratulations {}! You have recieved a {} to enjoy with {}! Click here to redeem!"
    promotions = indoorPromotions if willRain else outdoorPromotions
    promotion = random.choice(promotions)
    return template.format(userFriend, promotion, userInCrisis)

willRain = False
userInCrisis = "Donald Trump"
userFriend = "Barack Obama"

message = getPromotionMessage(willRain, userInCrisis, userFriend)
message


## Send promotion out to friend

import smtplib
from email.mime.text import MIMEText

def sendPromotion(name, email, message):
    sender = "zephyr.mail.alert@gmail.com"

    msg = MIMEText(message, 'plain')
    msg['From'] = sender
    msg['To'] = email
    msg['Subject'] = "Share this coupon with your friend: {}".format(name)
    mail = msg.as_string()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, "shareapromotion")
        server.sendmail(sender, email, mail)
        server.quit()
        print("Mail sent successfully!")

    except Exception as exc:
        print("Failed to send mail")

friendName = "Andy Zhu"
friendEmail = "andy.l.j.zhu@gmail.com"

sendPromotion(friendName, friendEmail, message)
