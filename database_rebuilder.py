#!/bin/python3
from tinydb import TinyDB, Query
import glob
import os
from datetime import datetime
import configparser

sub_msg_ids = ['sub', 'resub', 'subgift', 'giftpaidupgrade', 'anongiftpaidupgrade']
sub_dictionary = ['prime', 'tier1', 'tier2', 'tier3']
charity = 158062

database = TinyDB('thorlar_charity_tracker.json', indent=4)
database.default_table_name = 'daily_stats'
daily_db = Query()
setup_dictionary = {}
config = configparser.ConfigParser()
config.read('config.ini')
charity_amount_file = config['TwitchBot']['charity_amount_file']
obs_rounded_amount_file = config['TwitchBot']['obs_rounded_amount_file']
# Setup config items for the bot class
message_price = float(config['TwitchBot']['message_price'])
follow_price = float(config['TwitchBot']['follow_price'])
first_message_price = float(config['TwitchBot']['first_message_price'])
subscribe_tier1_price = float(config['TwitchBot']['subscribe_tier1_price'])
subscribe_tier2_price = float(config['TwitchBot']['subscribe_tier2_price'])
subscribe_tier3_price = float(config['TwitchBot']['subscribe_tier3_price'])

all_logs = glob.glob('logging/*.log')
for file in all_logs:
    file_date = os.path.basename(file).split('.')[0]
    old_date = datetime.strptime(file_date, '%m-%d-%y')
    new_date = old_date.strftime('%a %b %d %Y')
    chat_count = 0
    setup_dictionary[file_date] = {'date': new_date}
    with open(file, 'r', encoding="utf8", errors='ignore') as ofile:
        for line in ofile:
            split_line = line.split()
            sub_type = split_line[-1]
            sub_tier = split_line[-2].lower()
            if sub_tier == 'tier1':
                price = subscribe_tier1_price
            elif sub_tier == 'prime':
                price = subscribe_tier1_price
            elif sub_tier == 'tier2':
                price = subscribe_tier2_price
            elif sub_tier == 'tier3':
                price = subscribe_tier3_price
            if sub_type in sub_msg_ids and sub_tier in sub_dictionary:
                list_type = f'{sub_type}_{sub_tier}'
                if list_type in setup_dictionary[file_date]:
                    current_list_type_value = setup_dictionary[file_date][list_type]
                    setup_dictionary[file_date][list_type] = current_list_type_value + 1
                else:
                    setup_dictionary[file_date][list_type] = 1
                    setup_dictionary[file_date]['total_subs']
            else:
                charity = charity + message_price
                chat_count += 1
    setup_dictionary[file_date]['messages'] = chat_count
    setup_dictionary[file_date]['charity_value'] = round(charity, 2)
for day in setup_dictionary:
    print(setup_dictionary[day])
    database.upsert(setup_dictionary[day], daily_db.date == setup_dictionary[day]['date'])