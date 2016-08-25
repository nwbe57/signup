import webapp2
import re
import cgi


form = """
<form method="post">
    <html>
    <head>
        <title>Signup</title>
    </head>
    <body>
    <h1>Signup:</h1><br>
    <label>
        Username:
        <input type="text" name="username" value="%(username)s">
        <div style="color: red; display: inline-block;">%(error_name)s</div>
    </label>
    <br>
    <label>
        Password:
        <input type="text" name="password">
        <div style="color: red; display: inline-block;">%(error_pwd)s</div>
    </label>
    <br>
    <label>
        Verify Password:
        <input type="text" name="verify">
        <div style="color: red; display: inline-block;">%(error_match)s</div>
    </label>
    <br>
    <label>
        Email(Optional):
        <input type="text" name="email" value="%(email)s">
        <div style="color: red; display: inline-block;">%(error_email)s</div>
    </label>
    <br>
    <input type="submit">
    </body>
    </html>
</form>
"""


EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)
#######################################################
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)
#########################################################
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)



class MainPage(webapp2.RequestHandler):

    def write_form(self, error_name="", error_pwd="", error_match="", error_email="", username="", email=""):
        self.response.out.write(form %{"error_name": error_name, "error_pwd": error_pwd, "error_match": error_match,
                                       "error_email": error_email, "username": username, "email": email})

    def get(self):
        self.write_form()

    def post(self):
        global username
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        name = valid_username(username)
        pwd = valid_password(password)
        mail = valid_email(email)

        errname_escaped = ""
        errpwd_escaped = ""
        errmatch_escaped = ""
        errmail_escaped = ""

        if not name:
            error_name = "Username is not valid.".format(username)
            errname_escaped = cgi.escape(error_name, quote=True)

        if username == "":
            error_noname = "Username is blank.".format(username)
            errname_escaped = cgi.escape(error_noname, quote=True)

        if not pwd:
            error_pwd = "Password is not valid.".format(password)
            errpwd_escaped = cgi.escape(error_pwd, quote=True)

        if password != verify:
            error_match = "Passwords don't match.".format(verify)
            errmatch_escaped = cgi.escape(error_match, quote=True)

        if not mail:
            error_email = "Email is not valid.".format(email)
            errmail_escaped = cgi.escape(error_email, quote=True)



        self.write_form(errname_escaped, errpwd_escaped, errmatch_escaped, errmail_escaped, username, email)




        if (name and pwd and mail and (password == verify)):

             self.redirect("/welcome")



class Welcome(webapp2.RequestHandler):

    def get(self):

        response = "<p style='font-size:30px;'>" "Welcome " + username + "!" "</p>"
        self.response.write(response)


app = webapp2.WSGIApplication([('/', MainPage),('/welcome', Welcome)], debug=True)
