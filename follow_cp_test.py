import twitchio
import os
import sys
from twitchio.ext import pubsub, commands, routines

# Check if file doesn't exist
if not os.path.isfile('oauth.txt'):
    print("Your oauth.txt file is missing")
    sys.exit(1)
else:  # Does then open and read all lines
    with open('oauth.txt', 'r') as oauth:
        oauth_token = oauth.readlines()
        if len(oauth_token) < 1: # Do we not have at least one line?
            print("It appears your oauth.txt file is empty. Please add your oauth token to the file and restart this app.")
            sys.exit(1)
        else: # Pull the first item from the list and remove newlines
            oauth_token = oauth_token[0].rstrip()
            print(f"Found token: {oauth_token}")

thorlar_channel_id = 35740817

# Create a bot variable that instantiates a twitchio client connection using the token and looking for your channel
bot = twitchio.Client(
    token=oauth_token,
    initial_channels=["thorlar"]
)
# Setup a twitch websocket connection for receiving channel point notifications
bot.pubsub = pubsub.PubSubPool(bot)

# The capture event function by the websocket
@bot.event()
async def event_pubsub_channel_points(event):
    print(event)

# The main looping thread that subscribes to the websocket 
async def main():
    # List of channels to subscribe to
    topics = [
        pubsub.channel_points(oauth_token)[thorlar_channel_id],
    ]
    # Telling the websocket we're ready
    await bot.pubsub.subscribe_topics(topics)
    # Start the background thread that watches for event()
    await bot.start()

# Run this bot
bot.loop.run_until_complete(main())