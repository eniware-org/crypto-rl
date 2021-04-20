import json

from configurations import COINBASE_ENDPOINT, LOGGER
from data_recorder.coinbase_connector.coinbase_orderbook import CoinbaseOrderBook
from data_recorder.connector_components.client import Client
from datetime import datetime as dt
from configurations import TIMEZONE




class CoinbaseClient(Client):

    def __init__(self, **kwargs):
        """
        Constructor for Coinbase Client.
        """
        super(CoinbaseClient, self).__init__(exchange='coinbase', **kwargs)
        self.request = json.dumps(dict(type='subscribe',
                                       product_ids=[self.sym],
                                       channels=['full']))
        self.request_unsubscribe = json.dumps(dict(type='unsubscribe',
                                                   product_ids=[self.sym],
                                                   channels=['full']))
        self.book = CoinbaseOrderBook(sym=self.sym)
        self.trades_request = None
        self.ws_endpoint = COINBASE_ENDPOINT

    def run(self):
        """
        Handle incoming level 3 data on a separate thread or process.
        Returns
        -------
        """

        curr_tim = dt.now(tz=TIMEZONE)
        next_min = curr_tim.hour + 1

        super(CoinbaseClient, self).run()
        while True:
            msg = self.queue.get()

            curr_tim = dt.now(tz=TIMEZONE)
            curr_min = curr_tim.hour 

            # Min = hour in this case

            if curr_min == next_min == 0:
                self.book.load_book()
                print("RELOADING BOOK")
                next_min = 4
                continue

            if curr_min == next_min == 2:
                self.book.load_book()
                print("RELOADING BOOK")
                next_min = 6
                continue

            if curr_min == next_min == 4:
                self.book.load_book()
                print("RELOADING BOOK")
                next_min = 8
                continue

            if curr_min == next_min == 6:
                self.book.load_book()
                print("RELOADING BOOK")
                next_min = 10
                continue

            if curr_min == next_min == 8:
                self.book.load_book()
                print("RELOADING BOOK")
                next_min = 12
                continue

            if curr_min == next_min == 10:
                self.book.load_book()
                print("RELOADING BOOK")
                next_min = 14
                continue

            if curr_min == next_min == 12:
                self.book.load_book()
                print("RELOADING BOOK")
                next_min = 16
                continue

            if curr_min == next_min == 14:
                self.book.load_book()
                print("RELOADING BOOK")
                next_min = 18
                continue

            if curr_min == next_min == 16:
                self.book.load_book()
                print("RELOADING BOOK")
                next_min = 20
                continue

            if curr_min == next_min == 18:
                self.book.load_book()
                print("RELOADING BOOK")
                next_min = 22
                continue

            if curr_min == next_min == 20:
                self.book.load_book()
                print("RELOADING BOOK")
                next_min = 0
                continue

            if curr_min == next_min == 22:
                self.book.load_book()
                print("RELOADING BOOK")
                next_min = 2
                continue





            if self.book.new_tick(msg) is False:
                # Coinbase requires a REST call to GET the initial LOB snapshot
                self.book.load_book()
                self.retry_counter += 1
                LOGGER.info('\n[%s - %s] ...going to try and reload the order '
                            'book\n' % (self.exchange.upper(), self.sym))
                continue