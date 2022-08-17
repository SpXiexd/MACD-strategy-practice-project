# -*- coding: utf-8 -*-
# from jqdatasdk import *
from time import sleep
from datetime import datetime, time, timedelta
from dateutil import parser
import numpy as np
import pandas as pd
from pandas import *
from numpy import *
import os
from jqdatasdk import *


# ----------------------------------------------------------------------------
# backtrade system
class backtrade(object):
    def __init__(self):
        self._Open = []
        self._High = []
        self._Low = []
        self._Close = []
        self._Dt = []
        self._tick = []
        self._bar_path = None

    def getdata(self, ETFcode):
         auth('Your jquant account', 'password')
         df = get_price("513330.XSHG", start_date="2021-01-01", end_date="2022-04-15",
                        frequency="daily", fields=['open', 'close', 'high', 'low', 'volume', 'money'])
         df.to_csv('hengshenghulian_daily2.csv')


TRY = backtrade()
bar_path = 'E:\\postgraduate_life\\1A金融\\量化\\pythonProject\\venv\\hengshenghulian.csv'
backtrade.getdata(TRY, '513330.XSHG')