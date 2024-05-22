# Thorlar Charity Tracker

A basic charity tracking app that connects to twitch via an oauth key, and captures all chats, subs, resubs, and gifted subs. The app allows you to set values for each of those events and will automatically increment the charity value, and store it to file that OBS can read and display/update on stream.

## How to run the app
- Download python3 installer to your windows machine and install it (https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe)
- Open a powershell window and cd to the folder with the thorlar_charity_tracker.py file
- Copy the config.ini.example file to config.ini and change the channel and twitch_token settings to your appropriate settings (unless you want to when you run the app).
- Run the app with ```python3 .\thorlar_charity_tracker.py```. On each start the config screen pops up to allow you to change the config file within the app before running.
- Thats it!

## TODO:
- Convert the script to an executable that just "works" with a doubleclick
- Add the ability to update the config while the app is running instead of restarting, by adding a taskbar icon that can be clicked
- Research and determine if I can display the test in a way that the string rotates the numbers up when there is an update
- Figure out how best to add followers to the charity as the twitch documentation says you need a webserver with ssl and a true domain name, that it can call back to when there is a follower, instead of providing an event like they do everything else <sadface>.
- Add tinydb for tracking everything in a "database" for later correlation