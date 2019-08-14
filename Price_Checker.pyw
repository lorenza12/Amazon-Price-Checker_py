import schedule
import time
import Scraper
import CSV_Helper
import Helper_Functions
import Config



def main():
    
    try:
        csv_out = []

        csv_list = CSV_Helper.open_csv_file(Config.csv_directory)
        header = csv_list[0]

        #start building the data to write out including the header
        csv_out.append(header)


        for item in csv_list[1:]:
            #URL, Title, Current Price, Purcahse Price
            item_list = []

            item_title = None
            current_price = None
            purchase_price = None

            #amazon.com sometimes thinks the call is from a robot.. ;) so we can
            #switch up our request headers to trick them in thinking it is normal use
            header_counter = 1

            #information from the csv file
            url = item[0]
            current_title = item[1]
            current_price = item[2]
            purchase_price = item[3]
            
            if url != None and url != '':
                while item_title == None and header_counter < 11:
                    response_html = Scraper.request_html(url, header_counter)

                    item_title = Scraper.get_title(response_html)
                    item_price = Scraper.get_price(response_html)
                    item_sale_price = Scraper.get_deal_price(response_html)

                    #if amazon thought we were a robot, try a different header fromat
                    header_counter += 1

                if item_title == None or item_price == None:
                    #couldn't get html but still need to rewrite the unchanged data to the csv
                    no_html = f'Unable to get html for {current_title}'
                    Helper_Functions.write_log(no_html,0)

                    item_list.extend((url, current_title, Helper_Functions.format_price(current_price), Helper_Functions.format_price(purchase_price)))

                else:
                    #we were able to get html back
                    
                    updated_title = Helper_Functions.compare_titles(item_title, current_title)
                    updated_price = Helper_Functions.compare_sale_price(Helper_Functions.compare_current_prices(item_price, current_price), item_sale_price)

                    #create list to update csv file 
                    #if the titles or prices we got back in html happen to be blank, write out the old values that were already there
                    item_list.extend((url,
                                    (updated_title if updated_title != None and updated_title != '' else current_title),
                                    (Helper_Functions.format_price(updated_price) if updated_price != None and updated_price != '' else Helper_Functions.format_price(current_price)),
                                    Helper_Functions.format_price(purchase_price)))

                    should_buy = Helper_Functions.compare_purchase_price(updated_price, purchase_price, url, updated_title)

                    if should_buy:
                        #send email to buy
                        
                        Helper_Functions.purchase_notification(item_title, Helper_Functions.format_price(updated_price), url)

                    csv_out.append(item_list)
        

        #Write the file
        CSV_Helper.write_csv_file(csv_out, Config.csv_directory)
        
    except Exception as e:
        
        message = f'Fatal! main error {str(e)} \n'
        Helper_Functions.write_log(message,0)


if __name__ == "__main__":
    
    schedule.every().day.at(Config.run_time).do(main)
    
    while True:

        schedule.run_pending()
        time.sleep(60)
