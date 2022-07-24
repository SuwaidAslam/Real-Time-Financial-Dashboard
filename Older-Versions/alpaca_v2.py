import alpaca_trade_api as tradeapi
import mysql.connector
from mysql.connector import Error
import time
from datetime import datetime
from pytz import timezone


# a
API_KEY_a = 'a'
SECRET_KEY_a = 'a'

# b
API_KEY_b = 'b'
SECRET_KEY_b = 'b'

# c
API_KEY_c = 'c'
SECRET_KEY_c = 'c'

# d
API_KEY_d = 'd'
SECRET_KEY_d = 'd'


base_url = 'https://paper-api.alpaca.markets'
api_1 = tradeapi.REST(API_KEY_a, SECRET_KEY_a, base_url, api_version='v2')
api_2 = tradeapi.REST(API_KEY_b, SECRET_KEY_b, base_url, api_version='v2')
api_3 = tradeapi.REST(API_KEY_c, SECRET_KEY_c, base_url, api_version='v2')
api_4 = tradeapi.REST(API_KEY_d, SECRET_KEY_d, base_url, api_version='v2')
APIs = [api_1, api_2, api_3, api_4]
# specify Time zone
tz = timezone('US/Eastern')
#Mysql Connection with database
connection = mysql.connector.connect(host='localhost',
                                    database='dashboard',
                                    user='root',
                                    password='')

account_tables = ['yyyy_mm_dd_a', 'yyyy_mm_dd_b', 'yyyy_mm_dd_c', 'yyyy_mm_dd_d']
def insertData():
    accounts = []
    for index, api in enumerate(APIs):
        try:
            accounts.append(api.get_account())
        except:
            print('Something went wrong with Account {0} API'.format(index+1))
            
    cursor = connection.cursor()
    timeNow = datetime.now(tz)

    for (account, account_table) in zip(accounts, account_tables):
        try:
            if connection.is_connected():
                sql = """INSERT INTO {} (account_blocked, account_number, accrued_fees, buying_power, cash, created_at, crypto_status,
                        currency, daytrade_count, daytrading_buying_power, equity, id, initial_margin, last_equity, last_maintenance_margin
                        , long_market_value, maintenance_margin, multiplier, non_marginable_buying_power, pattern_day_trader, 
                        pending_transfer_in, portfolio_value, regt_buying_power, short_market_value, shorting_enabled,
                        sma, status, trade_suspended_by_user, trading_blocked, transfers_blocked, pl_last_equity, ts, cash_last_equity,
                        daytrading_buying_power_last_equity, initial_margin_last_equity, last_maintenance_margin_last_equity,
                        long_market_value_last_equity, maintenance_margin_last_equity, portfolio_value_last_equity,
                        regt_buying_power_last_equity, short_market_value_last_equity) VALUES (%s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(account_table)
                
                # calculating all additional column values
                current_pl_value = (float(account.equity)/float(account.last_equity) - 1)
                cursor.execute('SELECT entry_id, pl_last_equity FROM {} ORDER BY entry_id DESC LIMIT 1;'.format(account_table))
                
                prev_pl_value_row = cursor.fetchall()
                
                if not prev_pl_value_row:
                    pl_value = current_pl_value
                else:
                    prev_pl_value = float(prev_pl_value_row[0][1])
                    pl_value = current_pl_value
                    diff = current_pl_value - prev_pl_value
                    if diff > 0.1 or diff < -0.1:
                        pl_value = prev_pl_value
                cash_last_equity = (float(account.cash)/float(account.last_equity))
                daytrading_buying_power_last_equity = (float(account.daytrading_buying_power)/float(account.last_equity))
                initial_margin_last_equity = (float(account.initial_margin)/float(account.last_equity))
                last_maintenance_margin_last_equity = (float(account.last_maintenance_margin)/float(account.last_equity))
                long_market_value_last_equity = (float(account.long_market_value)/float(account.last_equity))
                maintenance_margin_last_equity = (float(account.maintenance_margin)/float(account.last_equity))
                portfolio_value_last_equity = (float(account.portfolio_value)/float(account.last_equity))
                regt_buying_power_last_equity = (float(account.regt_buying_power)/float(account.last_equity))
                short_market_value_last_equity = (float(account.short_market_value)/float(account.last_equity))
                # inserting all values to database
                val = (account.account_blocked, account.account_number, account.accrued_fees, account.buying_power, account.cash,
                account.created_at, account.crypto_status, account.currency, account.daytrade_count, account.daytrading_buying_power,
                account.equity, account.id, account.initial_margin, account.last_equity, account.last_maintenance_margin,
                account.long_market_value, account.maintenance_margin, account.multiplier, account.non_marginable_buying_power, account.pattern_day_trader,
                account.pending_transfer_in, account.portfolio_value, account.regt_buying_power, account.short_market_value, account.shorting_enabled,
                account.sma, account.status, account.trade_suspended_by_user, account.trading_blocked, account.transfers_blocked,
                pl_value, timeNow.strftime('%Y-%m-%d %H:%M:%S'), cash_last_equity, daytrading_buying_power_last_equity, 
                initial_margin_last_equity, last_maintenance_margin_last_equity, long_market_value_last_equity, maintenance_margin_last_equity,
                portfolio_value_last_equity, regt_buying_power_last_equity, short_market_value_last_equity)
                cursor.execute(sql, val)
                connection.commit()
        except Error as e:
            print("Error while connecting to MySQL", e)
    time.sleep(5)

def insert():
    while True:
        insertData()

def main():
    insert()

if __name__ == "__main__":
    main()