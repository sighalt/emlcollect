#!/usr/bin/env python3
"""
This script searches in a mailbox directory for emails with .eml-attachments and save these attachments as new
files into another directory so sa-learn can use it for learning.
"""
import os
import sys
import email
import logging
import argparse
from uuid import uuid4

logger = logging.getLogger()

log_handler = logging.StreamHandler(stream=sys.stdout)
log_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
log_handler.setLevel(logging.DEBUG)

logger.setLevel(logging.ERROR)
logger.addHandler(log_handler)

parser = argparse.ArgumentParser(description="This script searches in a mailbox directory for emails with "
                                             ".eml-attachments and save these attachments as new files into "
                                             "another directory so sa-learn can use it for learning.")
parser.add_argument('mailbox_dir', type=str, help='the path to the mailbox directory')
parser.add_argument('learning_dir', type=str, help='the path to the learning directory')
parser.add_argument('--verbose', dest='verbose', action='store_true', help='enable verbose output')
args = parser.parse_args()

if args.verbose:
    logger.setLevel(logging.INFO)

try:
    file_names = os.listdir(args.mailbox_dir)
except (IOError, OSError):
    logger.critical("Mailbox directory %s does not exist" % args.mailbox_dir)
    sys.exit(1)

for file_name in file_names:
    try:
        with open(os.path.join(args.mailbox_dir, file_name)) as mail_file:
            # open the mail
            logger.info("Found mail %s" % file_name)
            mail = email.message_from_file(mail_file)

    except (IOError, OSError):
        logger.error("Could not open file %s for reading" % file_name)
        continue

    else:
        # iterate over attachments
        for attachment in mail.get_payload():
            attachment_name = attachment.get_filename()

            # if attachment is an eml file process
            if attachment_name is not None and attachment_name.endswith(".eml"):
                logger.info("Found eml attachment %s" % attachment.get_filename())
                learning_file_name = str(uuid4())

                try:
                    # save eml file to learning directory
                    with open(os.path.join(args.learning_dir, learning_file_name), "w") as learning_file:
                        logger.info("Saving %s as %s to lerning directory" % (file_name, learning_file_name))
                        learning_file.write(attachment.as_string())
                except (IOError, OSError):
                    logger.error("Could not open file %s for writing" % learning_file_name)

    # remove the mail
    logger.info("Unlinking %s" % os.path.join(args.mailbox_dir, file_name))
    try:
        os.unlink(os.path.join(args.mailbox_dir, file_name))
    except (IOError, OSError):
        logger.warning("Could not unlink file %s" % file_name)
        continue

