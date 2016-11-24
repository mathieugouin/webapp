# User libs
import mgouinlib as mgl
import sendmail as sendmail

# System libs
import webapp2


#*******************************************************************************
# http://localhost:8080/mailer?from=me@acme.com&to=mgouin@gmail.com&message=hello&subject=test&name=Mat%20Gouin&redirect=redir
# http://mgouin.appspot.com/mailer?from=me@acme.com&to=mgouin@gmail.com&message=hello&subject=test&name=Mat%20Gouin&redirect=redir
#
# NOTES:
# Need post form method
#*******************************************************************************

def validateInput(args):
    ret = True
    requiredArgs = [
        "to",
        "from"
    ]

    for a in requiredArgs:
        if not a in args.keys() or len(args[a]) == 0:
            ret = False
            break

    return ret

class MainPage(webapp2.RequestHandler):

    #********************************************************************************
    def commonHandler(self):
        mgl.myLog("commonHandler()")

        lines = []

        args = {}
        for argKey in self.request.arguments():
            argVal = self.request.get(argKey)
            args[argKey] = argVal
            lines.append(argKey + " = " + argVal)
        mgl.myLog(args)

        if not validateInput(args):
            lines.extend([
                "Bad attributes: email is not sent",
                ])
        # Good attributes
        else:
            #Real email sending
            sendmail.sendMail(
                self.request.get("from"),
                self.request.get("to"),
                self.request.get("subject"),
                self.request.get("message"),
                self.request.get("name"),
                #args["from"], args["to"], args["subject"], args["message"], args["name"]
            )

            #TBD test
            #sendmail.sendMailTest()

        redirectURL = self.request.get("redirect").encode('ascii', 'ignore')
        if len(redirectURL) > 0:
            mgl.myLog("Performing redirection to " + redirectURL)
            self.redirect(redirectURL)
        else:
            # Normal page display
            self.response.headers["Content-Type"] = "text/html; charset=utf-8"

            self.response.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"\n')
            self.response.write('  "http://www.w3.org/TR/html4/loose.dtd">\n')
            self.response.write('<html>\n' +
                '<head>\n' +
                '<title>Mailer</title>\n' +
                '<meta http-equiv="Content-type" content="text/html;charset=UTF-8">\n' +
                '</head>\n' +
                '<body>\n\n')

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


    #********************************************************************************
    def post(self):
        mgl.myLog("********************************************************************************")
        mgl.myLog("post()")
        self.commonHandler()


    #********************************************************************************
    def get(self):
        mgl.myLog("********************************************************************************")
        mgl.myLog("get()")
        self.commonHandler()


app = webapp2.WSGIApplication([(r'/.*', MainPage)], debug=True)

