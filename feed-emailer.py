# feed-emailer: Email RSS feeds to yourself
# Author: Abitha K Thyagarajan <abitha@pm.me>
# Copyright (C) 2018 Abitha K Thyagarajan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import feedparser
from html2text import html2text
import smtplib
import gnupg
import ruamel.yaml as yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from time import mktime


# open the config file
with open("config.yml", 'r') as ymlfile:
    config = yaml.safe_load(ymlfile)


# login to the email server
sender = smtplib.SMTP_SSL(
    config['smtp_server'],
    config['smtp_port'])
sender.login(config['from'], config['password'])


# gnupg
gpg = gnupg.GPG(
    binary=config['gnupg'],
    homedir=config['gpg-home'],
    keyring=config['keyring'],
    secring=config['secring'])


def create_feed_email(feed, item):
    """Creates and returns a MIME email for the feed item.
    """

    Email = MIMEMultipart('alternative')
    # Item title - Feed title
    Email['Subject'] = item['title'] + " - " + feed['channel']['title']

    Email['From'] = config['from']
    Email['To'] = config['to']

    email_text = str(gpg.encrypt(item['title'] + "\n"
        + item['link'] + "\n"
        + item['published'] + "\n\n"
        + html2text(item['summary']) + "\n\n", # message content
        config['recipient-key'],
        default_key=config['sender-key'],
        passphrase=config['passphrase'],
        encrypt=True
    ))

    """email_html = ("<h2><a href='" + item['link'] + "'>"
        + item['title'] + "</a></h2>"
        + "<span>" + item['published'] + "</span><p>"
        + item['summary']
        + "</p><p>This post appeared first on "
        + "<a href='" + feed['channel']['link'] + "'>"
        + feed['channel']['title'] + "</a>.</p>"
    )"""

    email_text = MIMEText(email_text, 'plain')
    #email_html = MIMEText(email_html, 'html')
    Email.attach(email_text)
    #Email.attach(email_html)

    return Email


def create_invalid_feed_email(feed):
    """Creates a MIME email saying that `feed` is invalid.
    """
    Email = MIMEMultipart('alternative')
    Email['Subject'] = "Invalid feed: " + feed['href']

    Email['From'] = config['from']
    Email['To'] = config['to']

    email_text = str(gpg.encrypt("The feed '" + feed['href'] + \
        "' is not a valid ATOM/RSS feed.", # message content
        config['recipient-key'],
        default_key=config['sender-key'],
        passphrase=config['passphrase'],
        encrypt=True
    ))

    """
    email_html = "The feed <a href='" + feed['href'] + "'>" + feed['href'] + \
        "</a> is not a valid ATOM/RSS feed."
    """

    email_text = MIMEText(email_text, 'plain')
    #email_html = MIMEText(email_html, 'html')
    Email.attach(email_text)
    #Email.attach(email_html)

    return Email


for feed_url in config['feeds']:
    feed = feedparser.parse(feed_url)
    if feed['bozo'] != 1:
        for item in feed['items']:
            if datetime.fromtimestamp(mktime(item['published_parsed'])) > config['last_accessed']:
                sender.send_message(create_feed_email(feed, item))
                #print(item['published_parsed'])
    else:
        sender.send_message(create_invalid_feed_email(feed))

# Update time last accessed
config['last_accessed'] = datetime.now()
yaml.round_trip_dump(config, open(filename, 'w'))

# Log out from the email server
sender.quit()
