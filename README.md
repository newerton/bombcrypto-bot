<h1 align="center">

![Bomb Crypto Banner](https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/images/readme/banner.jpg)

  <a>
    💣 Bomb Crypto Bot 💣 
  </a>
</h1>

## ⚠️ Warning

I am not responsible for any penalties incurred by those who use the bot, use it at your own risk.

## 📄 Documentation
| - | Language |
|:---: | :---: |
| ![Portuguese](https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/images/readme/flags/brazil.png) | [Portuguese](https://github.com/newerton/bombcrypto-bot/blob/main/docs/README_pt-br.md) |
  
## 📌 Glossary

  * [About](#about)
  * [Donation](#donation)
  * [Robot - Preview](#robot-preview)
  * [Installation](#installation)
    * [Terminal commands](#commands)
  * [How to works](#how-to-works)
  * [Tests](#tests)
  * [Themes](#themes)
  * [Configs](#configs)
  * [How config the bot](#how-config-bot)
    * [What are the problems](#what-are-problems)
    * [Threshold in config file](#threshold-config)
    * [Image replacement](#image-replacement)
    * [Some behaviors that may indicate a false positive or negative](#some-behaviors)

## 📋 <a id="about"></a>About

This bot contains code from other developers, this bot was just refactored, to facilitate new implementations and maintenance.

Developers:
* https://github.com/mpcabete/
* https://github.com/afkapp/

This bot is free and open source.

Features:  
* Refactored code
* Add 3 captchas
* Themes
* Multi account with many windows side-by-side or many windows maximized
* Run the bot, without interrupting errors in the code
* Console colorful
* Bot speed, gain a few seconds on the move
* Update the configuration file required
## 🎁 <a id="donation"></a>Donation
BCOIN: 0x4847C29561B6682154E25c334E12d156e19F613a  
PIX: 08912d17-47a6-411e-b7ec-ef793203f836  

## 🤖 <a id="robot-preview"></a>Robot - Preview
![Screenshot - Preview](https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/images/readme/bot_working.jpg)

## 🪟 <a id="installation"></a>Installation

🖥️ Computer/Laptop High or Medium Profile  
🐍 Install the Python 3.9.9

🖥️ Computer/Laptop Low Profile or Low Profile with Windows 7 Pro  
🐍 Install the Python 3.8.10

🔗 [https://www.python.org/downloads/](https://www.python.org/downloads/)


⚠️ **It is important to check the option to add python to PATH**

### <a id="commands"></a>Commands
Install the dependencies by running the command below into the project folder:

```
pip install -r requirements.txt
```
Ready! Now just start the bot with the command, inside the project folder

```
python index.py
```


### <a id="how-to-works"></a>**How to works?**

The bot doesn't change any of the game's source code, it just takes a screenshot of the game's screen to find the buttons and simulates mouse movements.

### ⚠️ Some settings can be changed in the /config/config.yaml file, don't forget to restart the bot if you change the settings, some changes in the /config/config.yaml file may cause the bot to stop, such as activating the telegram when the bot is running.
## 🧪 <a id="tests"></a>Tests
**Desktop Medium Profile**  
Intel i5-3570k @ 3.4Ghz, 24GB RAM  
Windows 11, Resolution@1920x1080  
Python 3.9.9  

**Laptop Low Profile**  
Laptop Samsumg RV411, Pentium P6200 @ 2.13Ghz, 2GB RAM  
Windows 7, Resolution@1366x768  
Python 3.8.10

## 🎨 <a id="themes"></a>Themes
|      theme     	| toolbar image preview 	|
|:-------------:	|:-----:	|
| default 	| ![Lunar New Year](https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/images/readme/themes/default.jpg)	|
| lunar_newyear 	| ![Lunar New Year](https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/images/readme/themes/lunar_newyear.jpg)	|
## ⚒️ <a id="configs"></a>Configs
| code | type | description |
|:-------------: |:-----: |:-----: |
| **app** | - | - |
| theme | string | Current game theme, to recognize bug titles and hero list. Values in the [Themes](#themes) table |
| verify_version | bollean - true/false | Check app version every 1h, recommended to keep up to date |
| emoji | bollean - true/false | Enable/Disable show emoji in console messages |
| terminal_colorful | bollean - true/false | Enable/Disable show colored messages on terminal |
| run_time_app | int | Bot loop execution time |
| monitor_to_use | int | Monitor that the bot uses as a reference |
| captcha | bollean - true/false | Enable/Disable in-game captcha recognition |
| speed | string - normal/fast | Two bot speed modes, fast mode is between 1~3 minutes faster |
| **multi_account** | - | - |
| enable | bollean - true/false | Enable/Disable Multi Account functionality |
| window_title | string | Window title, for identification of the active game by the bot |
| window_fullscreen | bollean - true/false | Enable/Disable Fullscreen mode, recommended for small monitors |
| **time_intervals** | - | - |
| send_heroes_for_work | array - [int, int] | Start and end time for bot to search for heroes to work |
| refresh_heroes_positions | array - [int, int] | Start and end interval for bot to update map |
| **chests** | - | - |
| **values** | - | - |
| chest_01 | decimal | Brown chest reward value |
| chest_02 | decimal | Purple chest reward value |
| chest_03 | decimal | Golden chest reward value |
| chest_04 | decimal | Blue chest reward value |
| [**threshold**](#threshold-config) | - | - |
| default | decimal | Confidence default value |
| error_message | decimal | Confidence Value of Error Window Title |
| back_button | decimal | Confidence value of map back button |
| heroes_green_bar | decimal | Hero's partial energy bar confidence value |
| heroes_full_bar | decimal | Hero's full energy bar confidence value |
| heroes_send_all | decimal | Trust value of the send all button to work |
| chest | decimal | Confidence value of the chests to calculate the total BCOINS of the map |
| **heroes** | - | - |
| mode | string - all, green, full | How to send heroes to work.<br />**all** - Sends all heroes without criteria.<br />**green** - Sends heroes with partially green energy<br />**full** - Sends heroes with full energy|
| **list** | - | - |
| scroll_attempts | int | Total scroll the bot will make in the hero list |
| click_and_drag_amount | int | Maximum amount bot will scroll hero list |
| **offsets** | - | - |
| work_button_green | array - [int, int] | Offset for mouse click on WORK button |
| work_button_full | array - [int, int] | Offset for mouse click on WORK button |
| **metamask** | - | - |
| enable_login_metamask | bollean - true/false | Enable/Disable Metamask Auto Login |
| password | string | Password to unlock Metamask to login to the game |
| **services** | - | - |
| telegram | bollean - true/false | Enable/Disable the message sending service for Telegram |
| **log** | |
| save_to_file | bollean - true/false | Enable/Disable save console log to logger.log file |
| debug | bollean - true/false | Enable/Disable debugging of some bot information |



## ⚠️ <a id="how-config-bot"></a>Adjusting the bot

**Why some adjustments might be necessary?**

The bot uses image recognition to make decisions and move the mouse and click in the right places.  
It accomplishes this by comparing an example image with a screenshot of the computer/laptop screen.  
This method is subject to inconsistencies due to differences in your screen resolution and how the game is rendered on your computer.  
It's likely that the bot doesn't work 100% on the first run, and you need to make some adjustments to the config file.

<a id="what-are-problems"></a>  

**What are the problems?**

* **False negative** - The bot was supposed to recognize an image, for example the push to work button, but it didn't recognize the image in the screenshot.

* **False Positive** - The bot thinks it has recognized the image it is looking for in a place where this image does not appear.

To solve these problems there are two possibilities, adjusting the "threshold" parameter in the config.yaml file or replacing the example image in the "targets" folder with one taken on your own computer:

  <a id="threshold-config"></a>
  ### **Threshold in config file**

The "threshold" parameter regulates how confident the bot needs to be to consider that it has found the image it is looking for.  
This value is from 0 to 1 (0% to 100%).  
Ex:  

A threshold of 0.1 is too low, it will assume that it has found the image it is looking for in places it is not showing (false positive). The most common behavior for this problem is the bot clicking random places around the screen.

A threshold of 0.99 or 1 is too high, it won't find the image it's looking for, even when it's showing up on the screen. The most common behavior is that it simply doesn't move the cursor anywhere, or crashes in the middle of a process such as login.

  <a id="image-replacement"></a>

  ### **Image Replacement**

  The example images are stored in the "images/themes/default" folder. These images were taken on my computer with a resolution of 1920x1080. To replace some image that is not being recognized properly, simply find the corresponding image in the folder "images/themes/default", take a screenshot of the same area and replace the previous image. It is important that the replacement has the same name, including the .png extension.

  <a id="some-behaviors"></a>

### **Some behaviors that may indicate a false positive or negative**

### False positive:

- Repeatedly sending a hero who is already working to work on a infinite loop.
   - False positive on "work_button.png" image, bot thinks it sees the dark button on a hero with the light button.

- Clicking random places (usually white) on the screen
   - False positive on image "metamask_sign_button.png"
 
 ### False negative:

- Not doing anything
  - Maybe the bot is having problems with its resolution and is not recognizing any of the images, try changing the browser setting to 100%.

- Not sending the heroes to work
  - It may be a false negative on the image "bar_green_stamina.png" if the option "heroes.mode" is set to "green".

## 👍 Did you like it? :)

### BCOIN: 0x4847C29561B6682154E25c334E12d156e19F613a  
### PIX: 08912d17-47a6-411e-b7ec-ef793203f836
