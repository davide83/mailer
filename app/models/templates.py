# Author: Alex Ksikes

import web
import config
from config import db

from app.models import recipients

import re

def send(to_tpl, subject_tpl, message_tpl, sql_query='', reply_to='', send_copy=False):
    headers = {}
    if reply_to: headers['Reply-To'] = reply_to

    bcc = ''
    if send_copy: bcc = config.mail_bcc
    
    count = 1
    if not sql_query:
        web.sendmail(config.mail_sender, to_tpl, subject_tpl, message_tpl, bcc=bcc, headers=headers)
    else:    
        recipients_ = recipients.get_all(sql_query)
        count = len(recipients_)
        for recipient in recipients_:
            to = instantiate_from_template(to_tpl, recipient)
            subject = instantiate_from_template(subject_tpl, recipient)
            message = instantiate_from_template(message_tpl, recipient)

            web.sendmail(config.mail_sender, to, subject, message, bcc=bcc, headers=headers)
    return count  
        
def instantiate_from_template(tpl, recipient):
    # we can't do this! web.template.Template('$def with (**recipient)\n %s' % tpl)(**recipient)
    tpl = re.sub('\$(\w+)', '$recipient.\\1', tpl, re.S)
    tpl = '$def with (recipient)\n%s' % tpl
    
    return web.template.Template(tpl)(recipient).__body__[:-1]
