"""
Helper functions for network requests, etc
"""

import time
import sys
import socket
try:
    from concurrent.futures import ThreadPoolExecutor
    from requests_futures.sessions import FuturesSession
except ImportError:
    print("[!] You'll need to pip install requests-futures for this tool.")
    sys.exit()


def get_url_batch(url_list, use_ssl=False, callback='', threads=5):
    """
    Processes a list of URLs, sending the results back to the calling
    function in real-time via the `callback` parameter
    """

    # Start a counter for a status message
    tick = {}
    tick['total'] = len(url_list)
    tick['current'] = 0

    # Break the url list into smaller lists based on thread size
    queue = [url_list[x:x+threads] for x in range(0, len(url_list), threads)]

    # Define the protocol
    if use_ssl:
        proto = 'https://'
    else:
        proto = 'http://'

    # Start a requests object
    session = FuturesSession(executor=ThreadPoolExecutor(max_workers=threads))

    # Using the async requests-futures module, work in batches based on
    # the 'queue' list created above. Call each URL, sending the results
    # back to the callback function.
    for batch in queue:
        batch_pending = {}
        batch_results = {}

        # First, grab the pending async request and store it in a dict
        for url in batch:
            batch_pending[url] = session.get(proto + url)

        # Then, grab all the results from the queue
        for url in batch_pending:
            batch_results[url] = batch_pending[url].result()
        
        # Now, send all the results to the callback function for analysis
        for url in batch_results:
            callback(batch_results[url])

        # Refresh a status message
        tick['current'] += threads
        sys.stdout.flush()
        sys.stdout.write("    {}/{} complete..."
                         .format(tick['current'], tick['total']))
        sys.stdout.write('\r')

    # Clear the status message
    sys.stdout.write('                            \r')

def fast_dns_lookup(names):
    """
    Helper function to resolve DNS names.

    This is not actually fast yet. A future improvement should be threading
    and raw socket DNS lookups, as opposed to host system calls.
    """
    total = len(names)
    current = 0
    valid_names = []

    print("[*] Brute-forcing a list of {} possible DNS names".format(total))

    for name in names:
        # Refresh a status message
        current += 1
        sys.stdout.flush()
        sys.stdout.write("    {}/{} complete...".format(current, total))
        sys.stdout.write('\r')

        # Try to resolve the DNS name, continue on failure
        try:
            socket.gethostbyname(name)
            valid_names.append(name)
        except socket.gaierror:
            continue

    return valid_names

def printc(text, color):
    """
    Prints colored text to screen
    """
    # ANSI escape sequences
    green = '\033[92m'
    orange = '\033[93m'
    bold = '\033[1m'
    end = '\033[0m'

    if color == 'orange':
        sys.stdout.write(bold + orange + text + end)
    if color == 'green':
        sys.stdout.write(bold + green + text + end)
    if color == 'black':
        sys.stdout.write(bold + text + end)

def start_timer():
    """
    Starts a timer for functions in main module
    """
    # Start a counter to report on elapsed time
    start_time = time.time()
    return start_time

def stop_timer(start_time):
    """
    Stops timer and prints a status
    """
    # Stop the timer
    elapsed_time = time.time() - start_time
    formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    # Print some statistics
    print("")
    printc("    DONE", 'black')
    print(" Elapsed time: {}".format(formatted_time))
    print("")