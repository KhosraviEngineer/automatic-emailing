#C:\Users\khosravi\PycharmProjects\EmailProject
import smtplib
import csv
import requests
import io
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# my email info
SENDER_EMAIL = "amirmohkhosravi@gmail.com"
APP_PASSWORD = "wlki xdlb niub bbxy"

# Email body template
EMAIL_BODY_TEMPLATE = """
Dear Professor  {name},

I am a master's student in bioinformatics. The title of my thesis is "Meta-analysis of Bladder Cancer Cell Lines with the Aim of Comprehensively Investigating the Effect of gene co-expression in gene regulatory networks." I read your article titled "{Title}" and it was very interesting to me. I want to use your data.

I have two brief questions that I hope you can clarify:

1. Are the control samples of bladder cancer cell lines in your dataset, even if they were treated with scrambled siRNA or siControl or shControl or non-targeting siRNA, etc, considered the same for the meta-analysis purposes as the intact and unaltered cell lines?

2. How can we determine what real biological sample or condition a particular cell line represents? I am trying to figure out how I can reliably extrapolate the meta-analysis performed on the cell lines in my research to real-world biological contexts.

Could you help me, please?

Sincerely,
AmirMohammad Khosravi
M.Sc. Student in Bioinformatics
"""

def send_email(to_email, contact_name, title):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = title  # Set email subject to article title

    body = EMAIL_BODY_TEMPLATE.format(name=contact_name, Title=title)
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
            print(f"✅ Email sent to {contact_name} ({to_email}) with title: {title}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

def main():
    # لینک Google Sheets به صورت CSV
    #RNA-readyToEmail: done.
    #https://docs.google.com/spreadsheets/d/1A1YaJXbo4M5jUM2u0A19GP3EWS3is6N1aSqj9hWSpDI/edit?usp=sharing
    #Use:"https://docs.google.com/spreadsheets/d/1A1YaJXbo4M5jUM2u0A19GP3EWS3is6N1aSqj9hWSpDI/export?format=csv"
    #MicroReadyToEmail: doing
    #https://docs.google.com/spreadsheets/d/14n9F5ZoMNbTEI6Xub1ajOumf-QX2H8myttQ0oqi--l4/edit?usp=sharing
    #Use:"https://docs.google.com/spreadsheets/d/14n9F5ZoMNbTEI6Xub1ajOumf-QX2H8myttQ0oqi--l4/export?format=csv"
    #help example:
    #https://docs.google.com/spreadsheets/d/1XShF-uRHazMNb1gV_xWqTtO10ywPkQ0reRLc7ybuJu8/edit?usp=sharing
    #use:https://docs.google.com/spreadsheets/d/1XShF-uRHazMNb1gV_xWqTtO10ywPkQ0reRLc7ybuJu8/--export?format=csv
    #url = "https://docs.google.com/spreadsheets/d/1XShF-uRHazMNb1gV_xWqTtO10ywPkQ0reRLc7ybuJu8/export?format=csv"
    url = "https://docs.google.com/spreadsheets/d/14n9F5ZoMNbTEI6Xub1ajOumf-QX2H8myttQ0oqi--l4/export?format=csv"
    response = requests.get(url)
    response.encoding = 'utf-8'
    #response.encoding = 'latin1'  # یا 'utf-8' در صورت نیاز

    csv_file = io.StringIO(response.text)
    reader = csv.DictReader(csv_file)

    for row in reader:
        email = row['E-mail(s)'].split(',')[0].strip()
        title = row['Title'].strip()

        if len(title) > 150:
            title = title[:147] + "..."

        if email and title:
            send_email(
                to_email=email,
                contact_name=row['Contact name'] or "Researcher",
                title=title
            )

if __name__ == "__main__":
    main()
