import smtplib, ssl
import schedule
import time
import praw

reddit = praw.Reddit(client_id="RQZNy6656XVfmw",
                     client_secret="6BRNJAKXHqJO0YZ9pv-P7MgKy5g",
                     redirect_uri="http://localhost:8080",
                     user_agent="redditscraper by /u/anmu_")


def return_hot_subs(subreddit, num_subs):

    listx = [("Today's HOT submissions on r/{subreddit} include...".format(subreddit=subreddit))]
    for submission in subreddit.hot(limit = num_subs):
        if not submission.stickied:
            listx.append('link: http://redd.it/{}, title: {}, ups: {}'.format(submission.id,
                                                                              submission.title,
                                                                              submission.ups))

    return '\n'.join(''.join(listx[i:i+1]) for i in range(num_subs))


def send_email(sub1, sub2, sub3, sender_email, password, receiver_email, num_results):

    result1 = return_hot_subs(sub1, num_results)

    result2 = return_hot_subs(sub2, num_results)

    result3 = return_hot_subs(sub3, num_results)

    # print(len(result1))

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = sender_email
    receiver_email = receiver_email
    password = password
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
                        message.format(result1=result1,
                                       result2=result2,
                                       result3=result3),
                        )


subreddit1 = reddit.subreddit(((input("what is the first subreddit you would like results from ")).lower()).strip())
subreddit2 = reddit.subreddit(((input("what is the second subreddit you would like results from ")).lower()).strip())
subreddit3 = reddit.subreddit(((input("what is the third subreddit you would like results from ")).lower()).strip())
num_results = int((input("how many results per subreddit ")).strip())
sender_email = input("what is the sender email address ").strip()
password = input("what is the password of sender email ").strip()
receiver_email = input("what email should they be sent to ").strip()
time1 = input("at what time should the email be sent everyday in YY:ZZ format ").strip()

schedule.every().day.at(time1).do(send_email, subreddit1, subreddit2, subreddit3, sender_email, password, receiver_email, num_results)

while True:
    schedule.run_pending()
    time.sleep(1)


