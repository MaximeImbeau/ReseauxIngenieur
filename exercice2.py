import smtplib


from email.mime.text import MIMEText
# Remplissage des champs par lutilisateur
mailfrom = input("Mail from : ")
rcptto = input("Rcpt to : ")
subject = input ("Subject : ")
print("Data: ")
text = ""
temp = input()
while temp != ".":
    text += temp + "\n"
    temp = input()
# Creation dun objet courriel avec MIMEText msg = MIMEText ( text )
msg = MIMEText(text)
msg["From"] = mailfrom
msg["To"] = rcptto
msg["Subject"] = subject
# Envoi du courriel grace au protocole SMTP et au serveur de luniversite Laval
try:
    smtpConnection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
    smtpConnection.sendmail(mailfrom, rcptto, msg.as_string())
    smtpConnection.quit()
    print("Message envoye")
except:
    print("Lenvoi na pas pu etre effectue.")