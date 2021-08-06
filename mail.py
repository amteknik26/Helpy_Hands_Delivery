# TATTICKS just did it
import smtplib
import imghdr
import os
import pandas as pd
from email.message import EmailMessage


maildid = "amaanakhil@gmail.com"  # enter your email id here
password = "project008010"  # enter your password here



def Send_mail(val):

    message = EmailMessage()
    message['From'] = maildid
    message['To'] = val[2]
    # replace the subject
    message['Subject'] = 'Your Delivery details from Helpy Hands ;)'

    message.set_content("""
            Hi {}
            Thank you for ordering groceries from {}
            
            ORDER ID: {}
            Order details: {}

            Delivery ID : {}
            Delivery date : {}
            Delivery time : {}

            Paid: ₹{}
            Payment type : {}
            

            
            Thank You for buying from Helpy Hands. We can't wait to serve you again !

        """.format(val[3], val[5], val[0], val[1], val[6], val[7], val[8], val[10], val[9]))  

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(maildid, password)
        try:
            smtp.send_message(message)

            # if the mail is Successfully sent then this statement will be printed
            print("\n\nS u c c e s s f u l l y  S e n t !!!")

        except:
            print('\n\nMail failed to send')