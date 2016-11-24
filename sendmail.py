# https://cloud.google.com/appengine/docs/python/mail/
# anything@[APP_NAME].appspotmail.com
# noreply@mgouin.appspotmail.com

from google.appengine.api import mail
import webapp2


def sendMail(fromAddress, toAddress, subject, body):
    mail.send_mail(
            sender = "noreply@mgouin.appspotmail.com", # Enforced by google app engine
            reply_to = fromAddress,
            to = toAddress,
            bcc = "mgouin@gmail.com",  # for debug purposes
            subject = subject,
            body = body,
            #headers = {
            #    "References": 12345 # email_thread_id
            #}
    )

def sendMailTest():
    #         From                       To                  Subject                  Body
    sendMail("mathieu.gouin@yahoo.com", "mgouin@gmail.com", "test email app engine", "this is the body")

if __name__ == '__main__':
    sendMailTest()

