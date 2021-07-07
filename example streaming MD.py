import pandas as pd
from ib.opt import ibConnection, message as ib_message_type
from ib.opt import Connection
import datetime as dt
import time
from classes.ib_util import IBUtil
from classes.stock_data import StockData
import params.ib_data_types as datatype
from params.strategy_parameters import StrategyParameters
from classes.chart import Chart
import threading
import sys


def __request_streaming_data(self, ib_conn):
    # Stream market data
    for index, (key, stock_data) in enumerate(
            self.stocks_data.iteritems()):
        ib_conn.reqMktData(index,
                           stock_data.contract,
                           datatype.GENERIC_TICKS_NONE,
                           datatype.SNAPSHOT_NONE)
        time.sleep(1)

    # Stream account updates
    ib_conn.reqAccountUpdates(True, self.account_code)


def __request_historical_data(self, ib_conn):
    self.lock.acquire()
    try:
        for index, (key, stock_data) in enumerate(
                self.stocks_data.iteritems()):
            stock_data.is_storing_data = True
            ib_conn.reqHistoricalData(
                index,
                stock_data.contract,
                time.strftime(datatype.DATE_TIME_FORMAT),
                datatype.DURATION_1_HR,
                datatype.BAR_SIZE_5_SEC,
                datatype.WHAT_TO_SHOW_TRADES,
                datatype.RTH_ALL,
                datatype.DATEFORMAT_STRING)
            time.sleep(1)
    finally:
        self.lock.release()



    def start(self, symbols, trade_qty):
        print "HFT model started."

        self.trade_qty = trade_qty

        self.conn.connect()  # Get IB connection object
        self.__init_stocks_data(symbols)
        self.__request_streaming_data(self.conn)

        print "Bootstrapping the model..."
        start_time = time.time()
        self.__request_historical_data(self.conn)
        self.__wait_for_download_completion()
        self.strategy_params.set_bootstrap_completed()
        self.__print_elapsed_time(start_time)

        print "Calculating strategy parameters..."
        start_time = time.time()
        self.__calculate_strategy_params()
        self.__print_elapsed_time(start_time)

        print "Trading started."
        try:
            self.__update_charts()
            while True:
                time.sleep(1)

        except Exception, e:
            print "Exception:", e
            print "Cancelling...",
            self.__cancel_market_data_request()

            print "Disconnecting..."
            self.conn.disconnect()
            time.sleep(1)

            print "Disconnected."