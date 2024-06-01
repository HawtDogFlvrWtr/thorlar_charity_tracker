import configparser
import twitchio
from twitchio.ext import pubsub, commands, routines
import asyncio
import os
from tkinter import Tk, Label, Entry, Button, StringVar, Frame
import customtkinter
from datetime import date, datetime
from tinydb import TinyDB, Query
import time

# Blacklisted bot names not to count for chat charity
blacklisted_bots = ['streamelements', 'moobot', 'nightbot']
sub_msg_ids = ['sub', 'resub', 'subgift', 'giftpaidupgrade', 'anongiftpaidupgrade', 'submysterygift']
sub_dictionary = {'Prime': 'Prime', '1000': 'Tier1', '2000': 'Tier2', '3000': 'Tier3'}
database = TinyDB('thorlar_charity_tracker.json', indent=4)
database.default_table_name = 'daily_stats'
daily_db = Query()

# Create and initialize the configuration
config = configparser.ConfigParser()
config.read('config.ini')
# Create initial bot configuration GUI
class BotConfigGUI:
    def __init__(self, master, config):
        self.master = master
        self.master.title("Thorlar Charity Tracker")

        # Create labels and entry fields for each configuration option
        self.entries = {}
        row_number = 0
        for option, value in config['TwitchBot'].items():
            customtkinter.CTkLabel(self.master, text=option.replace('_', ' ').title()).grid(row=row_number, column=0, padx=10, pady=5)
            self.entries[option] = customtkinter.CTkEntry(self.master)
            self.entries[option].insert(0, value)
            self.entries[option].grid(row=row_number, column=1, padx=10, pady=5)
            row_number += 1

        # Create a button to update the configuration
        customtkinter.CTkButton(self.master, text="Update Configuration", command=self.update_config).grid(row=row_number, columnspan=2, pady=10)

    def update_config(self):
        # Get values from entry fields and update the configuration
        for option, entry in self.entries.items():
            config['TwitchBot'][option] = entry.get()
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        self.master.destroy()

# Initialize and display the bot configuration GUI
root = customtkinter.CTk()
frame = customtkinter.CTkFrame(master=root, width=200, height=200)
bot_config_gui = BotConfigGUI(root, config)
root.mainloop()

# Load configuration from the updated file
config.read('config.ini')
charity_amount_file = config['TwitchBot']['charity_amount_file']
obs_rounded_amount_file = config['TwitchBot']['obs_rounded_amount_file']

if not os.path.isfile(charity_amount_file):
    last_charity_amount = 0.0
else:
    with open(charity_amount_file, 'r') as ocharity_file:
        last_charity_amount = ocharity_file.readlines()
        if len(last_charity_amount) == 0: # No lines, start at 0
            last_charity_amount = 0.0
        else: # we have our last value
            last_charity_amount = float(last_charity_amount[0])

# Setup config items for the bot class
message_price = float(config['TwitchBot']['message_price'])
follow_price = float(config['TwitchBot']['follow_price'])
first_message_price = float(config['TwitchBot']['first_message_price'])
subscribe_tier1_price = float(config['TwitchBot']['subscribe_tier1_price'])
subscribe_tier2_price = float(config['TwitchBot']['subscribe_tier2_price'])
subscribe_tier3_price = float(config['TwitchBot']['subscribe_tier3_price'])
raid_in_price = float(config['TwitchBot']['raid_in_price'])
raid_out_price = float(config['TwitchBot']['raid_out_price'])
is_live = False

bot = twitchio.Client(
    token=config['TwitchBot']['twitch_token'],
    initial_channels=config['TwitchBot']['channels'].split(',')
)
bot.pubsub = pubsub.PubSubPool(bot)
routine = routines.routine(seconds=5.0, iterations=None)

def write_log(username, type, sub_type):
    if not os.path.exists('logging'): # Check for existing log dir and create if it doesn't exist, before writing logs
        os.makedirs('logging')
    short_date = date.today().strftime("%m-%d-%y")
    long_date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    with open(f'logging/{short_date}.log', 'a+', encoding="utf-8") as olog:
        # <date> - <login> <prime/tier#> <sub/giftsub/etc>
        log_string = f'{long_date} - {username} {type} {sub_type}\n'
        olog.write(log_string)

def write_charity(last_charity_amount, c_type, c_type_count = 1):
    global charity_amount_file
    global obs_rounded_amount_file
    # Update Charity
    print(f'{c_type.title()} Charity!: {last_charity_amount}')
    short_date = date.today().strftime("%a %b %d %Y")

    find_record = database.search(daily_db.date == short_date)
    if len(find_record) > 0:
        for record in find_record: # Iterate over records (should only be 1 but...always safer)
            if c_type in record:
                c_type_value = record[c_type] + c_type_count
            else:
                c_type_value = c_type_count
            # Increment record type and update charity amount
            database.upsert({c_type: c_type_value, 'charity_value': last_charity_amount}, daily_db.date == short_date)
    else: # A record for this date doesn't exist
        database.insert({c_type: 1, 'charity_value': last_charity_amount, 'date': short_date})

    # Update files for OBS
    with open(charity_amount_file, 'w') as ocharity_file:
        ocharity_file.write(str(last_charity_amount))

    # OBS Static text file
    with open(obs_rounded_amount_file, 'w') as oobd_charity_file:
        rounded_value = f"{round(last_charity_amount):,}".replace(',', ' ') # Put in Thorlar format of space betwen thousands
        oobd_charity_file.write(f"Raised: ${rounded_value}")
        
@bot.event()
async def ping(ctx):
    print('Caught Ping')
    await ctx.send(f'Pong!')

@bot.event()
async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
    print(f"Channel Point Redeem: REvent-UserId: {event.user.id}, REvent-UserName: {event.user.name}, REvent-Input: {event.input}, Reward-Name: {event.reward.title}, Reward-ID: {event.reward.id}, Reward-Cost: {event.reward.cost}, Reward-Prompt: {event.reward.prompt}")

@bot.event()
async def event_message(message):
    global last_charity_amount
    global charity_amount_file
    global is_live
    if is_live: # Only accept messages for charity if we're live
        if hasattr(message.author, 'name') and message.author.name.lower() not in blacklisted_bots:
            #print('New Message:', message.author.name, message.content)
            if 'first-msg' in message.tags and message.tags['first-msg'] == 1:
                last_charity_amount = last_charity_amount + first_message_price
                write_charity(last_charity_amount, "new-chatter-messages")
            else:
                last_charity_amount = last_charity_amount + message_price
                write_charity(last_charity_amount, "messages")
            write_log(message.author.name, ':', message.content)

@bot.event()
async def event_raw_usernotice(channel, tags):
    global last_charity_amount
    global charity_amount_file
    if 'msg-param-sub-plan' in tags and 'msg-id' in tags and tags['msg-id'] in sub_msg_ids: # Subs
        if tags['msg-param-sub-plan'] == 'Prime':
            plan_type = 'prime'
            last_charity_amount = last_charity_amount + subscribe_tier1_price
        elif tags['msg-param-sub-plan'] == '1000':
            plan_type = 'tier1'
            last_charity_amount = last_charity_amount + subscribe_tier1_price
        elif tags['msg-param-sub-plan'] == '2000':
            plan_type = 'tier2'
            last_charity_amount = last_charity_amount + subscribe_tier2_price
        elif tags['msg-param-sub-plan'] == '3000':
            plan_type = 'tier3'
            last_charity_amount = last_charity_amount + subscribe_tier3_price
        write_charity(last_charity_amount, f'{tags["msg-id"]}_{plan_type}')
        write_log(tags['login'], sub_dictionary[tags['msg-param-sub-plan']], tags['msg-id'])
    elif 'msg-id' in tags and 'msg-param-viewerCount' in tags and tags['msg-id'] == 'raid': # Handle incoming raid
        raid_in_charity_amount = raid_in_price * int(tags['msg-param-viewerCount'])
        last_charity_amount = last_charity_amount + raid_in_charity_amount
        write_charity(last_charity_amount, f'raid_in', int(tags['msg-param-viewerCount']))
        write_log(tags['login'], f'raid_in', tags['msg-param-viewerCount']) #<username> raid_in <viewer

# Check if live every 5 seconds
@routines.routine(seconds=5.0, iterations=None)
async def check_live():
    global is_live
    fetch_stream = await bot.fetch_streams(user_logins=config['TwitchBot']['channels'].split(','))
    if len(fetch_stream) > 0:
        is_live = True
    else:
        is_live = False

async def main():
    topics = [
        pubsub.channel_points(config['TwitchBot']['twitch_token'])[int(config['TwitchBot']['channel_id'])],
    ]
    check_live.start()
    await bot.pubsub.subscribe_topics(topics)
    await bot.start()

bot.loop.run_until_complete(main())