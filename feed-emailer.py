import feedparser
import html2text
import smtplib
import ruamel.yaml as yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

#def open_config_file(filename="config.yml"):
#    """Opens a YAML config file.
#       Default filename: "config.yml"
#    """

filename = "config.yml"
with open(filename, 'r') as ymlfile:
    config = yaml.safe_load(ymlfile)
#    return config


# login to the email server
sender = smtplib.SMTP_SSL(
    config['gmail']['smtp_server'],
    config['gmail']['smtp_port'])
sender.login(config['from'], config['password'])


def create_feed_email(feed, item):
    """Creates and returns a MIME email for the feed item.
    """

    Email = MIMEMultipart('alternative')
    # Item title - Feed title
    Email['Subject'] = item['title'] + " - " + feed['channel']['title']

    Email['From'] = config['from']
    Email['To'] = config['to']

    email_text = (item['title'] + "\n"
        + item['link'] + "\n"
        + item['published'] + "\n\n"
        + item['summary'] + "\n\n"
        + "This post appeared first on [" + feed['channel']['title'] + "]("
        + feed['channel']['link'] + ").")

    email_html = ("<h2><a href='" + item['link'] + "'>"
        + item['title'] + "</a></h2>"
        + "<span>" + item['published'] + "</span><p>"
        + item['summary']
        + "</p><p>This post appeared first on "
        + "<a href='" + feed['channel']['link'] + "'>"
        + feed['channel']['title'] + "</a>.</p>")

    email_text = MIMEText(email_text, 'plain')
    email_html = MIMEText(email_html, 'html')
    Email.attach(email_text)
    Email.attach(email_html)

    return Email

def create_invalid_feed_email(feed):
    """Creates a MIME email saying that `feed` is invalid.
    """
    Email = MIMEMultipart('alternative')
    Email['Subject'] = "Invalid feed: " + feed['href']

    Email['From'] = config['from']
    Email['To'] = config['to']

    email_text = "The feed '" + feed['href'] + \
        "' is not a valid ATOM/RSS feed."

    email_html = "The feed <a href='" + feed['href'] + "'>" + feed['href'] + \
        "</a> is not a valid ATOM/RSS feed."

    email_text = MIMEText(email_text, 'plain')
    email_html = MIMEText(email_html, 'html')
    Email.attach(email_text)
    Email.attach(email_html)

    return Email


i = 0
for feed_url in config['feeds']:
    feed = feedparser.parse(feed_url)
    if feed['bozo'] != 1:
        for item in feed['items']:
            if item['published_parsed'] > config['last_accessed']:
                sender.send_message(create_feed_email(feed, item))
                i += 1
                print("sent " + str(i) + " email(s)")
    else:
        sender.send_message(create_invalid_feed_email(feed))

config['last_accessed'] = datetime.now()

yaml.round_trip_dump(config, open(filename, 'w'))

sender.quit()
