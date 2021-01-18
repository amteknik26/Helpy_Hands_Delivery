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
    message['Subject'] = 'Enter the sub'

    message.set_content("""
            TraSafe, Traffic Violation Fine Generator
            Name : {}
            Ord Id : {}
            ord det : {}
            store id : {}
            store name : {}
            del id : {}
            del date : {}
            del time : {}
            payment type : {}
            total price : {}
            The above details has to be paid before 6 months of the report generation,
            Thank you.
        """.format(val[3], val[0], val[1], val[4], val[5],  val[6], val[7], val[8], val[9], val[10] ))  

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(maildid, password)
        try:
            smtp.send_message(message)

            # if the mail is Successfully sent then this statement will be printed
            print("\n\nS u c c e s s f u l l y  S e n t !!!")

        except:
            print('\n\nMail failed to send')


