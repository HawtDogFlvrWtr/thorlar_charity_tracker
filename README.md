# Thorlar Charity Tracker

A basic charity tracking app that connects to twitch via an oauth key, and captures all chats, subs, resubs, and gifted subs. The app allows you to set values for each of those events and will automatically increment the charity value, and store it to file that OBS can read and display/update on stream.

## How to run the app
- Download python3 installer to your windows machine and install it (https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe)
- Open a powershell window and cd to the folder with the thorlar_charity_tracker.py file
- Run ```<python>/<install>/<path>/pip install twitchio configparser tkinter customtkinter``` to download imports that we need and aren't included with python3 out of the box
    - The install path is likely ```c:\users\<username>\appdata\local\programs\python\python312\scripts\``` if you used the install exe above.
- Copy the config.ini.example file to config.ini and change the channel and twitch_token settings to your appropriate settings (unless you want to when you run the app).
- Generate an oAuth token for your bot by visiting ```https://twitchapps.com/tmi/``` and selecting connect. After your connection is made, save the string it provides (ex. oauth:blahblahblahblah). You need to use ```blahblahblahblah``` in your config.ini as the twitch_token
- Run the app with ```python3 .\thorlar_charity_tracker.py```. On each start the config screen pops up to allow you to change the config file within the app before running.

## OBS Text Source (no number rotate)
- Configure OBS to read the ```obs_charity_rounded.txt``` within this runtime folder. It will generate exactly what you need to display on stream. (Ex. Raised: $158 117)
    - On the scene you want to add it, click + in ```Sources```. 
    - Select ```Text (GDI+)```
        - ![Plus Image](https://github.com/HawtDogFlvrWtr/thorlar_charity_tracker/blob/main/git_images/plus_menu.png)
    - Add a name for the source
        - ![Name Source](https://github.com/HawtDogFlvrWtr/thorlar_charity_tracker/blob/main/git_images/create_select_source.png)
    - Select the font and Size you want. I suggest setting it to 72 and shrinking to the size you want
    - Click the ```Read from file``` box and select the file ```obs_charity_rounded.txt``` in your tracker folder.
    - Select the colors and any transform you want and then click OK
        - ![Change Settings](https://github.com/HawtDogFlvrWtr/thorlar_charity_tracker/blob/main/git_images/properties_for.png)
    - Shrink the box on the scene above and put it where you want it to. The text will update as the tracker updates the file.
        - ![Change Settings](https://github.com/HawtDogFlvrWtr/thorlar_charity_tracker/blob/main/git_images/move_text.png)

## OBS Browser source (with number rotate)
- Configure OBS Browser Source to read ```obs_charity_rounded.html``` within the runtime folder. It contains javascript that will rotate the text real fancy like.
    - On the scene you want to add it, click + in ```sources```.
    - Select ```Browser```
        - ![Plus Image](https://github.com/HawtDogFlvrWtr/thorlar_charity_tracker/blob/main/git_images/plus_menu_browser.png)
    - Add a name for the source
        - ![Name Source](https://github.com/HawtDogFlvrWtr/thorlar_charity_tracker/blob/main/git_images/create_select_source.png)
    - Click the ```Local file``` box and select the file ```obs_charity_rounded.html``` in your tracker folder.
    - Select the box size you want but 550x80 is optimal, then click Ok.
        - ![Change Settings](https://github.com/HawtDogFlvrWtr/thorlar_charity_tracker/blob/main/git_images/properties_for_browser.png)
    - Resize the web display on screen to fit exactly where you need it to.
        - ![Change Settings](https://github.com/HawtDogFlvrWtr/thorlar_charity_tracker/blob/main/git_images/move_shrink_text.png)

## TODO:
- Convert the script to an executable that just "works" with a doubleclick
- Add the ability to update the config while the app is running instead of restarting, by adding a taskbar icon that can be clicked
- ~~Research and determine if I can display the test in a way that the string rotates the numbers up when there is an update~~
- Figure out how best to add followers to the charity as the twitch documentation says you need a webserver with ssl and a true domain name, that it can call back to when there is a follower, instead of providing an event like they do everything else <sadface>.
    - This will likely be a csv export at the end of an episode that I need to build an ingest script for
- Track watch time per episode
    - This will likely be a csv export at the end of an episode that I need to build an ingest script for
- ~~Add tinydb for tracking everything in a "database" for later correlation~~
- ~~Build a database rebuild function based on chat logs, in case of catastrophe~~