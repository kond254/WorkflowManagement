import smtplib, ssl

port = 465  # For SSL

# Create a secure SSL context
context = ssl.create_default_context()

port = 587 # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "wbig.wfm@gmail.com"  # Enter your address
receiver_email = "konstantin.dreesen@live.de"  # Enter receiver address
password = "Passw0rd1."
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()

# Try to log in to server and send email
try:
    print("test")
    server = smtplib.SMTP(smtp_server,port)
    print("test")
    server.ehlo() # Can be omitted
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
except Exception as e:
    # Print any error messages to stdout
    print(e)

