import os

#----------------------------------------------------------------------------#
#                            Directory Locations                             #  
#----------------------------------------------------------------------------#
#leave these the defualt unless you wish to use another folder elsewhere

#csv location
csv_directory = os.getcwd() + '/CSV/Price_Checker_Urls.csv'

#email templates
buy_email_template_dir =  os.getcwd() + '/Email/email_purchase_template.html'
no_price_email_template_dir = os.getcwd() + '/Email/email_no_price_template.html'


#----------------------------------------------------------------------------#
#                               Email Settings                               #
#----------------------------------------------------------------------------#

#check the README for more information on what is needed to set this up

gmail_from_address = '' #email that will be sent from / email used from setup in README

email_password = '' #passcode received for app by following README

to_email_addresses = [] #comma seperated list of addresses to send to -> ['johndoe@gmail.com','doejohn@hotmail.com',...]

email_notifications = True #whether notifications should be emailed or just logged. By default a log will be written if an error occurs



#----------------------------------------------------------------------------#
#                               Execution Time                               #
#----------------------------------------------------------------------------#

#run_time = '08:00' #what time the program should execute every day (24 hr HH:MM)
#run_time_two = '15:30'

#what time(s) the program should run at (24 hr HH:MM) -> ['08:00', '15:30'] (run everyday at 8:00am and 3:30pm)
run_times = ['08:00','12:00','15:30', '17:00'] 


#----------------------------------------------------------------------------#
#                                 Log Settings                               #
#----------------------------------------------------------------------------#

log_file = 'Price_Checker_Log.txt'

kilabytes = 5 #size the log file will reach before resetting
purge_size =  kilabytes * 1024