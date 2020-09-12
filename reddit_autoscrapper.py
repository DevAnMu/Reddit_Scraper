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



def subredditname(num):

    listz = []
    for x in range(num):
        x = reddit.subreddit(
            ((input("what is the name of the subreddit you would like results from ")).lower()).strip())
        listz.append(x)

    return listz

def compileall(list, num_results):

    listy = []
    for x in list:
        listy.append(return_hot_subs(x, num_results))

    num = len(listy)

    return '\n'.join(''.join(listy[i:i + 1]) for i in range(num))



def send_email(sender_email, password, receiver_email, num_results, subreddit_names):

    print("running")
    x = subreddit_names
    y = compileall(x, num_results)

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = sender_email
    receiver_email = receiver_email
    password = password
    message = """\
Subject: Hi there
    
{results}
    
"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email,
                        receiver_email,
                        message.format(results=y))

    print("complete")


howmany_subreddits = int((input("how many subreddits: ")).strip())
subreddit_names = subredditname(howmany_subreddits)
num_results = int((input("how many submissions per subreddit: ")).strip())
sender_email = input("what is the sender email address: ").strip()
password = input("what is the password of sender email: ").strip()
receiver_email = input("what email should they be sent to: ").strip()
time1 = input("at what time should the email be sent everyday in YY:ZZ format: ").strip()


schedule.every().day.at(time1).do(send_email, sender_email, password, receiver_email, num_results, subreddit_names)

while True:
    schedule.run_pending()
    time.sleep(1)

