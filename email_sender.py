from settings import FRONTEND_URL, GMAIL_ACCOUNT_PASS


def generate_email_body(email_address, session_id):
    subject = 'Your analytics are ready ✨'
    body = f'''
Hey there,

You can view your analytics here {FRONTEND_URL}/recording?session_id={session_id}

Cheers,
Your Clubcord team
'''
    return '\r\n'.join(['To: %s' % email_address,
                        'From: Clubcord Team',
                        'Subject: %s' % subject,
                        '', body])


def send_email(email, session_id):
    import smtplib

    gmail_sender = 'clubcord.team@gmail.com'
    gmail_passwd = GMAIL_ACCOUNT_PASS

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    server.sendmail(gmail_sender, [email], generate_email_body(email, session_id).encode("utf-8"))
    print('Email sent to {}'.format(email))
    server.quit()
