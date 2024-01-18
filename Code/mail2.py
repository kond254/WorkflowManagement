import yagmail

receiver = "wbig.wfm+1@gmail.com"
body = "Hello there from Yagmail"


yag = yagmail.SMTP("wbig.wfm@gmail.com", "Passw0rd1.")
yag.send(
    to=receiver,
    subject="Yagmail test with attachment",
    contents=body, 
)