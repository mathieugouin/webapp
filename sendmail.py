# https://cloud.google.com/appengine/docs/python/mail/
# anything@[APP_NAME].appspotmail.com
# noreply@mgouin.appspotmail.com
# "Albert Johnson <Albert.Johnson@example.com>"

from google.appengine.api import mail
import webapp2

def emailAddName(email, name):
    if len(name) > 0:
        email = name + " <" + email + ">"
    return email

def sendMail(fromAddress, toAddress, subject, body, fromName=""):
    mail.send_mail(
            sender = emailAddName("noreply@mgouin.appspotmail.com", fromName), # Enforced by google app engine
            reply_to = emailAddName(fromAddress, fromName),
            to = toAddress,
            #bcc = "mgouin@gmail.com",  # for debug purposes
            subject = subject,
            body = body,
            #headers = {
            #    "References": 12345 # email_thread_id
            #}
    )

def sendMailTest():
    #         From                       To                  Subject                  Body                Name
    sendMail("mathieu.gouin@yahoo.com", "mgouin@gmail.com", "test email app engine", "this is the body", "Auto Mailer")

