import os


#csv location
csv_directory = os.getcwd() + '/CSV/Price_Checker_Urls.csv'


#email templates
buy_email_template_dir =  os.getcwd() + '/Email/email_purchase_template.html'

no_price_email_template_dir = os.getcwd() + '/Email/email_no_price_template.html'




#email settings - check the README for more information on what is needed to set this up
email_address = '' #email that will be sent from/to for notification

email_password = '' #passcode received for app by following README

#if false, notifications will be logged rather than emailed
#by defualt, a log will be written if an error occurs while sending an email
email_notifications = True



#runtime - what time the program should execute every day

# 24 hr HH:MM
run_time = '08:00'