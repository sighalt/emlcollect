# emlcollect
The script searches in a mailbox directory for emails with .eml-attachments and save these attachments as new files into another directory so another program e.g. sa-learn can use it.


# Use-case
You can create a mailbox to which your customers can send false-negative spam emails as .eml attachments. With a simple cronjob like the following these spam mails can get passed to sa-learn automatically.

    0 *    * * *   root    /opt/emlcollect.py /var/vmail/mydomain.com/spamcollect/new/ /var/lib/spamassassin/learning && sudo -u amavis -i sa-learn --spam /var/lib/spamassassin/learning/ >/dev/null
