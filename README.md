# Amazon Price Checker

Amazon Price Checker is a pyhton script that allows you to monitor items on Amazon and alert you when they are at your desired price.

### Installation

Amazon Price Chekcer uses 3 external modules that are required to be installed before running.

To install these modules, open a command promopt within the project's directoy and run the following: 

```sh
$ pip install -r requirements.txt
```

This should install BeautifulSoup, fake_useragent, and the schedule modules.

### Setup

###### - CSV
Amazon Price Checker uses a csv file to hold the url of items you wish to be monitored. Within the CSV folder, open the Price_Checker_Urls.csv file and add in the desired urls. The only two required fields needed are the 'Url' and the 'Purchase Price'. The 'Title' and 'Current Price' sections will be updated automatically when the script scrapes data from Amazon. 

###### - Email
If an item's price reaches or falls below your desired purchase price, Amazon Price Checker will need to notify you of this. The most practical way to achieve this is by setting up email. 

* The email functionality is built using Gmail. In order to setup the option to send mail, you must have Google's 2 step verification setup for your account. To set this up, go to the site here: https://www.google.com/landing/2step/

* Once 2-step verification is setup, we need to get an app specefic password that we can use for the program. To do this, go to https://myaccount.google.com/apppasswords

    * Select mail from the first dropdown, then 'Other' from the seconds dropdown and give it a name. For example : Price Checker - Python 
    * Once you click generate, a password will be displayed on screen. Save that somewhere as it will be the password used for the application so we can send emails

* Open the Congif.py file and enter the email address associated with the account from step 2, and enter the app specific password you just received in the email_password variable.

* Email should now be setup for the application. By default it will log any notifcations/errors if the email fails to send 

If you wish to turn off the email notifactions, you can set the email_notifications boolean to False within the Config.py file. This will in turn log all notifications to a log file that will need to be manually checked for updates. 

###### - Run time
Within the Config.py file there is a run_time varaible that is the time the program will run on a daily basis. This is a 24 hour time setting and by default it is set to run every day at 8 am. 


### Execution

To start the program, right click on Price_Checker.pyw and open it with Python.

Since it is a .pyw file, no terminal window will be displayed. The program will run in the background and be executed on a daily based on the run_time varaible described above. 

To verify that the program is indeed running, open up task manager and there should be a Python program listed.

If you wish to run the program manually without a scheduled runtime, open a command prompt and navigate to the repository folder.
 
run the command:
```sh
$ py Price_Checker_Manual.py
```

This will immediately execute the script regardless of the Config file run_time setting. 
