import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import praw

reddit = praw.Reddit(client_id="RQZNy6656XVfmw",
                     client_secret="6BRNJAKXHqJO0YZ9pv-P7MgKy5g",
                     redirect_uri="http://localhost:8080",
                     user_agent="redditscraper by /u/anmu_")


def return_hot_subs(subreddit):

    listx = [("Today's HOT submissions on r/{subreddit} include...".format(subreddit=subreddit))]
    for submission in subreddit.hot(limit = 6):
        if not submission.stickied:
            listx.append('link: http://redd.it/{}, title: {}, ups: {}'.format(submission.id,
                                                                              submission.title,
                                                                              submission.ups))

    return '\n'.join(''.join(listx[i:i+1]) for i in range(6))


subreddit1 = reddit.subreddit(((input("what is the first subreddit you would like results from")).lower()).strip())
subreddit2 = reddit.subreddit(((input("what is the second subreddit you would like results from")).lower()).strip())
subreddit3 = reddit.subreddit(((input("what is the third subreddit you would like results from")).lower()).strip())

result1 = return_hot_subs(subreddit1)

result2 = return_hot_subs(subreddit2)

result3 = return_hot_subs(subreddit3)

# print(len(result1))

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = input("what is the sender email address").strip() # Enter your address
receiver_email = input("what is the receiver email address").strip() # Enter receiver address
password = input("what is the password for the sender email").strip()
message = """\
Subject: Hi there

{result1}

{result2}

{result3}
"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email,
                    receiver_email,
                    message.format(result1=result1[0:],
                                   result2=result2,
                                   result3=result3),
                    )
