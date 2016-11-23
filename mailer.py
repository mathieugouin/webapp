import mgouinlib as mgl
import sendmail as sendmail

from google.appengine.api import app_identity
from google.appengine.api import mail
import webapp2
import logging


################################################################################
# http://localhost:8080/mailer?txtweb-message=Hardware+store+near+St-Hubert%2C+Qc
# http://mgouin.appspot.com/gmls?txtweb-message=Hardware+store+near+St-Hubert%2C+Qc
#
# NOTES:
# Need post form method
################################################################################

def validateInput(args):
    # TBD test if required minimum argKey (from, to, ...)
    pass
    return True

class MainPage(webapp2.RequestHandler):

    def post(self):
        mgl.myLog("post()")
        print repr(self.request.POST)

        id = self.request.POST['thread_id']

        appId = app_identity.get_application_id()

        sendmail.sendMailTest()

        self.response.content_type = 'text/plain'
        self.response.write('Sent an email')


    def get(self):
        mgl.myLog("get()")

        self.response.headers["Content-Type"] = "text/html; charset=utf-8"

        self.response.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n')
        self.response.write('  "http://www.w3.org/TR/html4/loose.dtd">\n')
        self.response.write('<html>\n' +
            '<head>\n' +
            '<title>Mailer</title>\n' +
            '<meta http-equiv="Content-type" content="text/html;charset=UTF-8">\n' +
            '</head>\n' +
            '<body>\n\n')

        lines = []

        args = {}
        for argKey in self.request.arguments():
            argVal = self.request.get(argKey)
            mgl.myLog(argKey + " = " + argVal)
            args[argKey] = argVal
            lines.append(argKey + " = " + argVal)

        mgl.myLog(args)

        if not validateInput(args):
            lines.extend([
                "Bad attributes",
                ])
        # Good attributes
        else:
            #TBD send mail here...
            #sendmail.sendMail(args["from"], args["to"], args["subject"], args["body"])

            #TBD test for now...
            sendmail.sendMailTest()

        for l in lines:
            mgl.myLog(l)
            self.response.write(mgl.processLine(l))

        self.response.write('\n')
        self.response.write('<div><img alt="Powered by Google" src="powered-by-google-on-white.png" width="104" height="16"></div>\n')

        self.response.write('\n')
        self.response.write(r"""<script type="text/javascript">""" + "\n")
        self.response.write(r"""    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){""" + "\n")
        self.response.write(r"""    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),""" + "\n")
        self.response.write(r"""    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)""" + "\n")
        self.response.write(r"""    })(window,document,'script','//www.google-analytics.com/analytics.js','ga');""" + "\n")
        self.response.write(r"""    ga('create', 'UA-1787000-3', 'mgouin.appspot.com');""" + "\n")
        self.response.write(r"""    ga('send', 'pageview');""" + "\n")
        self.response.write(r"""</script>""" + "\n")

        self.response.write("\n</body>\n</html>\n")

app = webapp2.WSGIApplication([(r'/.*', MainPage)], debug=True)

