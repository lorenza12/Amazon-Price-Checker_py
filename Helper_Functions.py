from string import Template
import os
import datetime
import Email_Service
import Config

def compare_titles(html_title, csv_title):
    #Check if the item title has changed on Amazon from what is in the csv already
    if html_title != None:
        if html_title.strip() != csv_title.strip():
            return html_title.strip()
        else:
            return csv_title.strip()
    else:
        return None


def compare_current_prices(html_price, current_price):
    #Check if the price has changed on Amazon from what is in the csv already
    if html_price != None:
        if html_price.strip() != current_price.strip():
            return html_price.strip()
        else:
            return current_price.strip()
    else:
        return None



def compare_sale_price(item_price, sale_price):
    #if the item is not on sale the sale_price will be None
    if sale_price != None:
        if price_to_float(sale_price) < price_to_float(item_price):
            return sale_price
        else:
            return item_price
    else:
        return item_price

 
def compare_purchase_price(html_price, current_purchase_price, url, item_title):
    #Compres the items price to the desired price and will return True if it is at or below it, false otherwise
    if (current_purchase_price != None and current_purchase_price.strip() != '') and html_price != None:
        if price_to_float(html_price) <= price_to_float(current_purchase_price):
            return True
        else:
            return False
    else:
        no_purchase_price_notification(item_title, url)
        return False



def purchase_notification(item_title, new_price, url):
    #try and email the error. If fail, write to log
    if Config.email_notifications:    
        try:
            subject = f'Your item {item_title} is ready to purchase!'
            temp_html  = open_email_template(Config.buy_email_template_dir)
            
            updated_html = update_purchase_tempalte(temp_html, item_title, new_price, url)
            
            Email_Service.email_html(subject, updated_html)
        
        except Exception as e:
            #log the error and also log the notification since it failed to send
            message = f'Error sending email notification within Helper_Functions.buy_email \n\n{str(e)}'
            buy_message = f'Your item {item_title} is ready to purchase! \nIt now has a price of {format_price(new_price)} that is at or below your asking price'
            
            write_log(message,0)
            write_log(buy_message,1)
            
    else:
        message = f'Your item {item_title} is ready to purchase! \nIt now has a price of {format_price(new_price)} that is at or below your asking price'
        write_log(message,1)
        
        


def no_purchase_price_notification(item_title, url):
    #try and email the error. If fail, write to log 
    if Config.email_notifications:    
        try:
            item = item_title if item_title != None else url
            
            subject = f'Your item  {item_title} has no purchase price!'
            temp_html  = open_email_template(Config.no_price_email_template_dir)
            
            updated_html = update_price_tempalte(temp_html, item_title, url)
            
            Email_Service.email_html(subject, updated_html)
            
        except Exception as e:
            #log the error and also log the notification since it failed to send
            message = f'Error sending email notification within Helper_Functions.no_purchase_price_email \n\n {str(e)}'
            price_message = f'Your item {item_title} has no purchase price!\nPlease fill in a purchase price so I can notify you when to buy it!'
       
            write_log(message,0)
            write_log(price_message,1)
            
    else:
        message = f'Your item {item_title} has no purchase price!\nPlease fill in a purchase price so I can notify you when to buy it!'
        write_log(message,1)



def open_email_template(template_dir):
    #return string representation of the email template
    try:
        with open(template_dir, 'r') as email_template:
            str_tempalte = ''
            for line in email_template:
                str_tempalte += line

        return str_tempalte
    
    except Exception as e:
        message = f'open_email_template error {str(e)}'
        write_log(message,0)

def update_purchase_tempalte(email_template, item_name, item_price, url):
    #fill the email tempalte with the item title, price, and link to the item
    temp_href = """<center><a href="$URL" style="Margin-top: 16px;Margin-bottom: 12px;font-style: normal;font-weight: normal;color: #ffc773;font-size: 50px;line-height: 32px;text-align: center;">Buy it before it's too late!</a></center>"""
    
    amazon_link = temp_href.replace('$URL', url)

    updated_tempalte = Template(email_template).safe_substitute(ITEM_NAME=item_name, Item_Price=item_price, LINK=amazon_link)

    return updated_tempalte


def update_price_tempalte(email_template, item_name, url):
    #if there is no item title use the url as reference
    item = item_name if item_name != '' else url
    
    updated_tempalte = Template(email_template).safe_substitute(ITEM_NAME=item)

    return updated_tempalte


def write_log(log_message, type=1):
    # 1==alert, 0==error
    log_head = '[ALERT]' if type == 1 else '[ERROR]'
    
    date_time = datetime.datetime.now()
    
    header = log_head + ': ' + date_time.strftime('%Y-%m-%d %I:%M')
    message = f'Message: {log_message} \n'

    #append logs to the end of the file. a means append to file + means create file if it doesn't exist
    with open('Price_Checker_Log.txt', 'a+') as log_file:
        log_file.write(header)
        log_file.write('\n')
        log_file.write(message)
        log_file.write('\n')
    

def price_to_float(price):
    #formats a string price into a float so we can perform equality operations
    if '$' in price:
        price = price.strip('$')
    
    return float(price)



def format_price(price):
    #formats a floating number into a string dollar amount
    try:
        if '$' not in price:
            dollar_price = '$' + str(price)
            return dollar_price
        else:
            return price
    except:
        return price
    
