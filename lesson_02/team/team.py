
"""
Course: CSE 351 
Lesson: L02 team activity
File:   prove.py
Author: Kyle Davies

Purpose: Retrieve Star Wars details from a server

Instructions:

- This program requires that the server.py program be started in a terminal window.
- The program will retrieve the names of:
    - characters
    - planets
    - starships
    - vehicles
    - species

- the server will delay the request by 0.5 seconds

TODO
- Create a threaded class to make a call to the server where
  it retrieves data based on a URL.  The class should have a method
  called get_name() that returns the name of the character, planet, etc...
- The threaded class should only retrieve one URL.
  
- Speed up this program as fast as you can by:
    - creating as many as you can
    - start them all
    - join them all

"""

from datetime import datetime, timedelta
import threading

from common import *

# Include cse 351 common Python files
from cse351 import *

# global
call_count = 0

class GetUrl(threading.Thread):

    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.name = ''

    def get_name(self):
        return self.name

    def run(self):
        item = get_data_from_server(self.url)
        self.name = item['name']

def get_urls(film6, kind):
    global call_count

    urls = film6[kind]
    print(kind)

    threads = []
    for url in urls:
        thread = GetUrl(url)
        call_count += 1
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
        print(f'  {thread.get_name()}')

def main():
    global call_count

    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    film6 = get_data_from_server(f'{TOP_API_URL}/films/6')
    call_count += 1
    print_dict(film6)

    # Retrieve people
    get_urls(film6, 'characters')
    get_urls(film6, 'planets')
    get_urls(film6, 'starships')
    get_urls(film6, 'vehicles')
    get_urls(film6, 'species')

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')

if __name__ == "__main__":
    main()
    # This is the main entry point of the program.  It will call the main function.