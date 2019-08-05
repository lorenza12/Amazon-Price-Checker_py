import smtplib
from email.message import EmailMessage
import Config
import Helper_Functions


EMAIL_ADDRESS = Config.email_address
EMAIL_PASSWORD = Config.email_password


def email_html(subject, html, to_address='', from_address=''):
        
        try:
                msg = EmailMessage()

                msg['Subject'] = subject

                #optional to and from address. by defualt use what is in the config file
                msg['From'] = EMAIL_ADDRESS if to_address == '' else to_address
                msg['To'] = EMAIL_ADDRESS if from_address == '' else from_address

                msg.add_alternative(html, subtype='html')

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(msg)
                
        except Exception as e:
                
                message = f'email_html error {str(e)} \n paramaters: subject - {subject} html - {html} to_address - {to_address} from_address - {from_address}'
                Helper_Functions.write_log(message,0)
                
        
def email_txt(subject, body, to_address='', from_address=''):
        try:
    
                msg = EmailMessage()

                msg['Subject'] = subject
                
                #optional to and from address. by defualt use what is in the config file
                msg['From'] = EMAIL_ADDRESS if to_address == '' else to_address
                msg['To'] = EMAIL_ADDRESS if from_address == '' else from_address

                msg.set_content(body)

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(msg)        

        except Exception as e:
                
                message = f'email_txt error {str(e)} \n paramaters: subject - {subject} body - {body}  to_address - {to_address} from_address - {from_address}'
                Helper_Functions.write_log(message,0)
                