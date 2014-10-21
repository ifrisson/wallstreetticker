#!/usr/bin/env python

import os
import pprint

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from threading import Thread
from functools import reduce
import time
import urllib

# ************* BEGIN STOCK SCRIPT **************

symlist = ["AAPL", "GOOG", "TSLA", "AAL", "JBLU"] #Insert stock ticker symbols here
                 
def __request(symbol, stat):
        url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
        return urllib.urlopen(url).read().strip().strip('"')
         
def get_all(symbol):
        
        # Get all available quote data for the given ticker symbol.
                 
        # Returns a dictionary.
        
        values = __request(symbol, 'l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7').split(',')
        stock_data = {}
        stock_data['price'] = values[0]
        stock_data['change'] = values[1]
        stock_data['volume'] = values[2]
        stock_data['avg_daily_volume'] = values[3]
        stock_data['stock_exchange'] = values[4]
        stock_data['market_cap'] = values[5]
        stock_data['book_value'] = values[6]
        stock_data['ebitda'] = values[7]
        stock_data['dividend_per_share'] = values[8]
        stock_data['dividend_yield'] = values[9]
        stock_data['earnings_per_share'] = values[10]
        stock_data['52_week_high'] = values[11]
        stock_data['52_week_low'] = values[12]
        stock_data['50day_moving_avg'] = values[13]
        stock_data['200day_moving_avg'] = values[14]
        stock_data['price_earnings_ratio'] = values[15]
        stock_data['price_earnings_growth_ratio'] = values[16]
        stock_data['price_sales_ratio'] = values[17]
        stock_data['price_book_ratio'] = values[18]
        stock_data['short_ratio'] = values[19]
        return stock_data
         
def get_price(symbol):
        return __request(symbol, 'l1') # get Last Trade (Price Only)
         
def get_change(symbol):
        return __request(symbol, 'c1') # get Change
         
def get_volume(symbol):
        return __request(symbol, 'v') # get more info
         
def get_avg_daily_volume(symbol):
        return __request(symbol, 'a2') # get Average Daily Volume
         
def get_stock_exchange(symbol):
        return __request(symbol, 'x') # get Stock Exchange
         
def get_market_cap(symbol):
        return __request(symbol, 'j1') # get Market Capitalization
         
def get_book_value(symbol):
        return __request(symbol, 'b4') # get Book Value
         
def get_ebitda(symbol):
        return __request(symbol, 'j4') # get EBITDA
         
def get_dividend_per_share(symbol):
        return __request(symbol, 'd') # get Divident per share
         
def get_dividend_yield(symbol):
        return __request(symbol, 'y') # get Dividend Yield
         
def get_earnings_per_share(symbol):
        return __request(symbol, 'e') # get Earnings per Share
         
def get_52_week_high(symbol):
        return __request(symbol, 'k') # get 52 Week High
         
def get_52_week_low(symbol):
        return __request(symbol, 'j') # get 52 week Low
         
def get_50day_moving_avg(symbol):
        return __request(symbol, 'm3') # get 50 Day Moving Average
         
def get_200day_moving_avg(symbol): # get 200 Day Moving Average
        return __request(symbol, 'm4')
         
def get_price_earnings_ratio(symbol):
        return __request(symbol, 'r') # get P/E Ratio
         
def get_price_earnings_growth_ratio(symbol):
        return __request(symbol, 'r5') # get PEG Ratio
         
def get_price_sales_ratio(symbol):
        return __request(symbol, 'p5') # get Price / Sales
         
def get_price_book_ratio(symbol):
        return __request(symbol, 'p6') # get Price / Book
         
def get_short_ratio(symbol):
        return __request(symbol, 's7') # get Short Ratio
         
def get_prev_close(symbol):
        return __request(symbol, 'p') # get Prev close
         
def get_open(symbol):
        return __request(symbol, 'o') # get Open

while True:
	all_text = ''
	stock_symbol_colour = (95, 158, 160)
	stocks = []
	for sym in symlist:
	    stock_symbol = (sym + ' ', stock_symbol_colour)

	    if float(get_change(sym)) > 0: 
		stock_value = ('${} {}'.format(get_price(sym), get_change(sym)), (0, 255, 0))
	    elif float(get_change(sym)) < 0:
		stock_value = ('${} {}'.format(get_price(sym), get_change(sym)), (255, 0, 0))
	    else:
		stock_value = ('${} {}HGIG'.format(get_price(sym), get_change(sym)), (0, 0, 255))

	    stocks.append( (stock_symbol, stock_value) )

	# Determine the width of the stock symbols combined
	all_text = reduce(lambda x, y: x + y[0][0] + y[1][0] + ' ', stocks, '')
	font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 16)
	width, ignore = font.getsize(all_text)
	print width, all_text

	pprint.pprint(stocks)

	im = Image.new("RGB", (width + 30, 16), "black")
	draw = ImageDraw.Draw(im)
	x = 0
	for stock in stocks:
	    # Draw the stock symbol
	    stock_symbol_text = stock[0][0]
	    stock_symbol_colour = stock[0][1]
	    draw.text( (x, 0), stock_symbol_text, stock_symbol_colour, font=font)
	    x = x + font.getsize(stock_symbol_text)[0]
	    
	    # Draw the stock value
	    stock_value_text = stock[1][0] + ' '
	    stock_value_colour = stock[1][1]
	    draw.text( (x, 0), stock_value_text, stock_value_colour, font=font)
	    x = x + font.getsize(stock_value_text)[0]

	im.save("test.ppm")

	# Scroll stock feed image on 3 panel, 16-row display for 5 min
	os.system("./rpi-rgb-led-matrix/led-matrix -c3 -r16 -D1 -t 300 test.ppm")
	#time.sleep(15*60) # Sleep for 15 min
