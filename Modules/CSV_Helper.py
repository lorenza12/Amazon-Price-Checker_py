import csv
import sys

sys.path.append('../')
import Config
import Modules.Helper_Functions as Helper_Functions        



def open_csv_file(csv_file):
    """Returns a list of lists holding Url, Title, Current Price, Purchase Price
       header is included -> csv_list[0] is the header
    """
    try:
        csv_list = []
        with open(csv_file, newline='') as csv_urls:
            csv_reader = csv.reader(csv_urls, delimiter=',')
            for row in csv_reader:
                csv_list.append(row)

        return csv_list
    
    except Exception as e:
        
        message = f'open_csv_file error {str(e)} \n paramaters: csv_file - {csv_file}'
        Helper_Functions.write_log(message,0)
                


def write_csv_file(csv_data_list, csv_file):
    """Writes the data to the csv file 

       Params: a lists of lists containing Url, Title, Current Price, Purcahse Price
       Title and Current Price are upadated automatically where Url and Purchase Price are manually entered

       header is included -> csv_list[0] is the header
    """
    try:
        with open(csv_file, 'w', newline='') as csv_urls_out:
            csv_writer = csv.writer(csv_urls_out, delimiter=',')

            for list_item in csv_data_list:
                csv_writer.writerow(list_item)
            
    except Exception as e:
        
        message = f'write_csv_file error {str(e)} \n paramaters: csv_data_list - {csv_data_list} csv_file - {csv_file}'
        Helper_Functions.write_log(message,0)
                



if __name__ == "__main__":
    #testing
    import os
    csv_directory = os.path.dirname(os.getcwd()) + '/CSV/Price_Checker_Urls.csv'
    
    file_in = open_csv_file(csv_directory)
    
    for item in file_in:
        print(item)