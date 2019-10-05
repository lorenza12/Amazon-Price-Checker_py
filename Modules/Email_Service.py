import smtplib
from email.message import EmailMessage

import sys
sys.path.append('../')
import Config
import Modules.Helper_Functions


def email_html(subject, html, to_addresses=Config.to_email_addresses, from_address=Config.gmail_from_address):
        """Sends out an html based  email to a list of desired addresses
        
           Params: subject of the email, html to send, list of addresses to send to (optional), email address sending from (optional)
        """
        try:
                
                msg = EmailMessage()

                msg['Subject'] = subject

                #optional to and from address. by defualt use what is in the config file
                msg['From'] = from_address
                msg['To'] = ','.join(to_addresses)

                msg.add_alternative(html, subtype='html')

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(Config.gmail_from_address, Config.email_password)
                        smtp.send_message(msg)
                
        except Exception as e:
                
                message = f'email_html error {str(e)} \n paramaters: subject - {subject} html - {html} to_address - {to_addresses} from_address - {from_address}'
                Helper_Functions.write_log(message,0)
                
        
def email_txt(subject, body, to_addresses=Config.to_email_addresses, from_address=Config.gmail_from_address):
        """Sends out an text based  email to a list of desired addresses
        
           Params: subject of the email, email body to send, list of addresses to send to (optional), email address sending from (optional)
        """ 
        try:
    
                msg = EmailMessage()

                msg['Subject'] = subject
                
                #optional to and from address. by defualt use what is in the config file
                msg['From'] = from_address
                msg['To'] = ','.join(to_addresses)

                msg.set_content(body)

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(Config.gmail_from_address, Config.email_password)
                        smtp.send_message(msg)        

        except Exception as e:
                
                message = f'email_txt error {str(e)} \n paramaters: subject - {subject} body - {body}  to_address - {to_addresses} from_address - {from_address}'
                Helper_Functions.write_log(message,0)
                