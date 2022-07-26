Create Database dashboard;

use dashboard;

create Table yyyy_mm_dd_a(
entry_id int Not Null AUTO_INCREMENT,
account_blocked varchar(6),
account_number varchar(20),
accrued_fees varchar(8),
buying_power float,
cash float,
created_at varchar(50),
crypto_status varchar(15),
currency varchar(8),
daytrade_count int,
daytrading_buying_power BIGINT,
equity float,
id varchar(100),
initial_margin float,
last_equity float,
last_maintenance_margin int,
long_market_value float,
maintenance_margin float,
multiplier int,
non_marginable_buying_power float,
pattern_day_trader varchar(6),
pending_transfer_in int,
portfolio_value float,
regt_buying_power float,
short_market_value float,
shorting_enabled varchar(6),
sma int,
status varchar(15),
trade_suspended_by_user varchar(6),
trading_blocked varchar(6),
transfers_blocked varchar(6),
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
pl_last_equity float,
cash_last_equity float,
daytrading_buying_power_last_equity float,
initial_margin_last_equity float,
last_maintenance_margin_last_equity float,
long_market_value_last_equity float,
maintenance_margin_last_equity float,
portfolio_value_last_equity float,
regt_buying_power_last_equity float,
short_market_value_last_equity float,
long_market_value_stock float,
short_market_value_stock float,
Primary Key (entry_id)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;


create Table yyyy_mm_dd_b(
entry_id int Not Null AUTO_INCREMENT,
account_blocked varchar(6),
account_number varchar(20),
accrued_fees varchar(8),
buying_power float,
cash float,
created_at varchar(50),
crypto_status varchar(15),
currency varchar(8),
daytrade_count int,
daytrading_buying_power BIGINT,
equity float,
id varchar(100),
initial_margin float,
last_equity float,
last_maintenance_margin int,
long_market_value float,
maintenance_margin float,
multiplier int,
non_marginable_buying_power float,
pattern_day_trader varchar(6),
pending_transfer_in int,
portfolio_value float,
regt_buying_power float,
short_market_value float,
shorting_enabled varchar(6),
sma int,
status varchar(15),
trade_suspended_by_user varchar(6),
trading_blocked varchar(6),
transfers_blocked varchar(6),
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
pl_last_equity float,
cash_last_equity float,
daytrading_buying_power_last_equity float,
initial_margin_last_equity float,
last_maintenance_margin_last_equity float,
long_market_value_last_equity float,
maintenance_margin_last_equity float,
portfolio_value_last_equity float,
regt_buying_power_last_equity float,
short_market_value_last_equity float,
long_market_value_stock float,
short_market_value_stock float,
Primary Key (entry_id)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;


create Table yyyy_mm_dd_c(
entry_id int Not Null AUTO_INCREMENT,
account_blocked varchar(6),
account_number varchar(20),
accrued_fees varchar(8),
buying_power float,
cash float,
created_at varchar(50),
crypto_status varchar(15),
currency varchar(8),
daytrade_count int,
daytrading_buying_power BIGINT,
equity float,
id varchar(100),
initial_margin float,
last_equity float,
last_maintenance_margin int,
long_market_value float,
maintenance_margin float,
multiplier int,
non_marginable_buying_power float,
pattern_day_trader varchar(6),
pending_transfer_in int,
portfolio_value float,
regt_buying_power float,
short_market_value float,
shorting_enabled varchar(6),
sma int,
status varchar(15),
trade_suspended_by_user varchar(6),
trading_blocked varchar(6),
transfers_blocked varchar(6),
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
pl_last_equity float,
cash_last_equity float,
daytrading_buying_power_last_equity float,
initial_margin_last_equity float,
last_maintenance_margin_last_equity float,
long_market_value_last_equity float,
maintenance_margin_last_equity float,
portfolio_value_last_equity float,
regt_buying_power_last_equity float,
short_market_value_last_equity float,
long_market_value_stock float,
short_market_value_stock float,
Primary Key (entry_id)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

create Table yyyy_mm_dd_d(
entry_id int Not Null AUTO_INCREMENT,
account_blocked varchar(6),
account_number varchar(20),
accrued_fees varchar(8),
buying_power float,
cash float,
created_at varchar(50),
crypto_status varchar(15),
currency varchar(8),
daytrade_count int,
daytrading_buying_power BIGINT,
equity float,
id varchar(100),
initial_margin float,
last_equity float,
last_maintenance_margin int,
long_market_value float,
maintenance_margin float,
multiplier int,
non_marginable_buying_power float,
pattern_day_trader varchar(6),
pending_transfer_in int,
portfolio_value float,
regt_buying_power float,
short_market_value float,
shorting_enabled varchar(6),
sma int,
status varchar(15),
trade_suspended_by_user varchar(6),
trading_blocked varchar(6),
transfers_blocked varchar(6),
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
pl_last_equity float,
cash_last_equity float,
daytrading_buying_power_last_equity float,
initial_margin_last_equity float,
last_maintenance_margin_last_equity float,
long_market_value_last_equity float,
maintenance_margin_last_equity float,
portfolio_value_last_equity float,
regt_buying_power_last_equity float,
short_market_value_last_equity float,
long_market_value_stock float,
short_market_value_stock float,
Primary Key (entry_id)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;


create Table Stocks_account_a(
stock_id int Not Null AUTO_INCREMENT,
entry_id int Not Null,
symbol varchar(20),
open_pl float,
position_percentage float,
open_pl_percentage float,
parent varchar(30),
CONSTRAINT entry_const_a Foreign Key (entry_id) References yyyy_mm_dd_a(entry_id) ON DELETE CASCADE,
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
Primary Key (stock_id)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

create Table Stocks_account_b(
stock_id int Not Null AUTO_INCREMENT,
entry_id int Not Null,
symbol varchar(20),
open_pl float,
position_percentage float,
open_pl_percentage float,
parent varchar(30),
CONSTRAINT entry_const_b Foreign Key (entry_id) References yyyy_mm_dd_a(entry_id) ON DELETE CASCADE,
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
Primary Key (stock_id)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

create Table Stocks_account_c(
stock_id int Not Null AUTO_INCREMENT,
entry_id int Not Null,
symbol varchar(20),
open_pl float,
position_percentage float,
open_pl_percentage float,
parent varchar(30),
CONSTRAINT entry_const_c Foreign Key (entry_id) References yyyy_mm_dd_a(entry_id) ON DELETE CASCADE,
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
Primary Key (stock_id)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

create Table Stocks_account_d(
stock_id int Not Null AUTO_INCREMENT,
entry_id int Not Null,
symbol varchar(20),
open_pl float,
position_percentage float,
open_pl_percentage float,
parent varchar(30),
CONSTRAINT entry_const_d Foreign Key (entry_id) References yyyy_mm_dd_a(entry_id) ON DELETE CASCADE,
ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
Primary Key (stock_id)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;