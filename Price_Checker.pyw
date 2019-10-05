import schedule
import timeit
import time
import multiprocessing

import Config
import Modules.Scraper as Scraper
import Modules.CSV_Helper as CSV_Helper
import Modules.Helper_Functions as Helper_Functions


def main():

    try:
        timer_start = timeit.default_timer()
        csv_out = []
        result_queue = multiprocessing.Queue()

        csv_list = CSV_Helper.open_csv_file(Config.csv_directory)
        header = csv_list[0]

        #start building the data to write out including the header
        csv_out.append(header)

        processes = []

        for item in csv_list[1:]:
            #information from the csv file
            url = item[0]
            current_title = item[1]
            current_price = item[2]
            purchase_price = item[3]

            #create the process
            proc = multiprocessing.Process(target=request_worker, args=(result_queue,url,current_title,current_price,purchase_price,))

            processes.append(proc)
            #start the process
            proc.start()

        #join the processes together to get all results
        for proc in processes: 
            proc.join()

        while result_queue.qsize() > 0:
            item = result_queue.get() #.get pops the item from the queue
            compare_price_email(item) #check price of item and send email if needed
            csv_out.append(item)

        #Write the file
        CSV_Helper.write_csv_file(csv_out, Config.csv_directory)   

        timer_end = timeit.default_timer()
        Helper_Functions.write_log(f'Amazon Price Checker Run Complete - {round(timer_end - timer_start, 2)} seconds')

    except Exception as e:
        message = f'Fatal! main: {str(e)} \n'
        Helper_Functions.write_log(message,0)


def request_worker(result_queue,url,current_title,current_price,purchase_price):
    try:
        if url != None and url != '':

            item_title = None

            #amazon.com sometimes thinks the call is from a robot.. ;) so we can
            #switch up our request headers to trick them in thinking it is normal use
            header_counter = 1
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

            #item_list.extend((url, current_title, Helper_Functions.format_price(current_price), Helper_Functions.format_price(purchase_price)))
            result_queue.put((url, current_title, Helper_Functions.format_price(current_price), Helper_Functions.format_price(purchase_price)))
            
        else:
            #we were able to get html back      
            updated_title = Helper_Functions.compare_titles(item_title, current_title)
            updated_price = Helper_Functions.compare_sale_price(Helper_Functions.compare_current_prices(item_price, current_price), item_sale_price)

            #create list to update csv file
            #if the titles or prices we got back in html happen to be blank, write out the old values that were already there
            result_queue.put([url, 
                            (updated_title if updated_title != None or updated_title == '' else current_title), 
                            (Helper_Functions.format_price(updated_price) if updated_price != None or updated_price == '' else Helper_Functions.format_price(current_price)),
                            Helper_Functions.format_price(purchase_price)])

    except Exception as e:
        message = f'request_worker: {str(e)} \n'
        Helper_Functions.write_log(message,0)
            

def compare_price_email(result_list):
    try:
        #URL, Title, Current Price, Purcahse Price
        url = result_list[0]
        title = result_list[1]
        current_price = result_list[2]
        purchase_price = result_list[3]

        should_buy = Helper_Functions.compare_purchase_price(current_price, purchase_price, url, title)

        if should_buy:
            #send email to buy
            Helper_Functions.purchase_notification(title, Helper_Functions.format_price(current_price), url)

    except Exception as e:
        message = f'compare_price_email: {str(e)} \n'
        Helper_Functions.write_log(message,0)





if __name__ == "__main__":
    try:
        for exec_time in Config.run_times:
            schedule.every().day.at(exec_time).do(main)

        while True:
            schedule.run_pending()
            time.sleep(60)

    except Exception as e:
        message = f'Fatal! __main__: {str(e)} \n'
        Helper_Functions.write_log(message,0)
