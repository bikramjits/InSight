import websocket
import threading
import time
import json
import argparse
import pandas as pd
import csv
import jsonify
import datascience

data = []

def on_message(ws, message):
    data.append(message)

def on_error(ws, error):
   print(error)

def parseToList():
    res = []
    exec('res=[' + data[0]+']')
    for i in range(1, len(data)):
        exec('res.append('+data[i]+')')
    return res

def on_close(ws):
    a = parseToList()
    df_dict = {}
    keys = list(a[0].keys())
    for i in range(len(keys)):
        df_dict[keys[i]] = []
    for i in range(len(a)):
        d = a[i]
        for j in range(len(keys)):
            df_dict[keys[j]].append(d[keys[j]])

    my_table = pd.DataFrame(df_dict)

    my_table.to_csv('nasdata.csv')

    print("### closed ###")

def on_open(ws):
   def run():
       ws.send("")
       time.sleep(1)
       ws.close()
   threading.Thread(target=run).start()

def main():
   parser = argparse.ArgumentParser(description='gettin some market data')
   parser.add_argument('--start_date', required=True, help="Enter a valid start date in YYYYMMDD format")
   parser.add_argument('--end_date', required=True, help="Enter a valid end date in YYYYMMDD format")
   parser.add_argument('--symbols', required=True, help="Enter a ticker symbol or list of tickers. E.g. NDAQ or NDAQ,AAPL,MSFT")

   args = parser.parse_args()

   websocket.enableTrace(True)

   symbols = args.symbols.split(',')

   for symbol in symbols:
       url = 'ws://34.214.11.52/stream?symbol={}&start={}&end={}'.format(symbol,args.start_date,args.end_date)

       ws = websocket.WebSocketApp(url,
                                   on_message = on_message,
                                   on_error = on_error,
                                   on_close = on_close)
       ws.on_open = on_open
       ws.run_forever()


if __name__ == "__main__":
  main()
