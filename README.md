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
  * [Clean Page - Remove all ads](#clean-page)
  * [Robot - Preview](#robot-preview)
  * [Installation](#installation)
    * [Terminal commands](#commands)
  * [How to works](#how-to-works)
  * [Tests](#tests)
  * [Themes](#themes)
  * [Configs](#configs)
    * 🆕 [Auth with user and pass](#auth-with-user-and-pass)
  * [How config the bot](#how-config-bot)
    * [What are the problems](#what-are-problems)
    * [Threshold in config file](#threshold-config)
    * [Image replacement](#image-replacement)
    * [Some behaviors that may indicate a false positive or negative](#some-behaviors)

## 📋 <a id="about"></a>About

This bot contains code from other developers, this bot was just refactored, to facilitate new implementations and maintenance.

Developers (Base code):
* https://github.com/mpcabete/
* https://github.com/vin350/ (Telegram integration)

This bot is free and open source.

Features:  
* Refactored code
* Add 3 captchas
* Themes
* Multi account with many windows side-by-side or many windows maximized
* Run the Bot, without interrupting errors in the code
* Console colorful
* Bot speed, gain a few seconds on the move
* Update the configuration file required
* Auto-update files (requires Git installed)
* Bcoins report after finalizing the map
* New map estimation added
* Telegram new commands (workall, restall)
* Multi account with Multi auth
* Send heroes to **House** for rarity

## 🎁 <a id="donation"></a>Donation
BCOIN: 0x4847C29561B6682154E25c334E12d156e19F613a  
SEN: 0x4847C29561B6682154E25c334E12d156e19F613a  
PIX: 08912d17-47a6-411e-b7ec-ef793203f836  

## 🖌️ <a id="clean-page"></a>Clean Page - Remove all ads
### Stylebot https://stylebot.dev/
```css
html, body {
  background-color: #000000;
  width: 100%;
  height: 100%;
}

div {
  height: 100%;
  width: 100%;
}

#root > div > img,
#root > div > div > div:nth-child(1),
#root > div > div > div:nth-child(3),
#root > div > div > div:nth-child(2) > div:nth-child(1),
#root > div > div > div:nth-child(2) > div:nth-child(3) {
  display: none;
}

#root > div > div > div:nth-child(2) > div:nth-child(2) > div {
  background: none;
  display: flex;
  justify-content: center;
  align-items: center;
}

#root > div > div > div:nth-child(2) > div:nth-child(2) > div > iframe {
  width: 965px;
  height: 645px;
}
``` 
### Tampemonkey https://www.tampermonkey.net/
```js
// ==UserScript==
// @name         Bombcrypto Styles
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       Newerton
// @match        https://app.bombcrypto.io/
// @icon         https://www.google.com/s2/favicons?domain=bombcrypto.io
// @grant        none
// @require http://code.jquery.com/jquery-latest.js
// ==/UserScript==

const $ = window.jQuery;
$('html, body').css({'background-color': '#150F1B', 'height': '100%'});
const iframe = $('iframe[title^="Bomb"]').attr('scrolling', 'no').clone();
$('div[id="root"] > div').remove();
$('div[id="root"]')
    .css({'width': '100%', 'height': '100%', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'});
$('div[id="root"]').append(iframe);
```
## 🤖 <a id="robot-preview"></a>Robot - Preview
![Screenshot - Preview](https://raw.githubusercontent.com/newerton/bombcrypto-bot/main/images/readme/bot_working.png)

## 🪟 <a id="installation"></a>Installation

### **Python**

🖥️ Computer/Laptop High or Medium Profile  
🐍 Install the Python 3.9.9

🖥️ Computer/Laptop Low Profile or Low Profile with Windows 7 Pro  
🐍 Install the Python 3.8.10

🔗 [https://www.python.org/downloads/](https://www.python.org/downloads/)

⚠️ **It is important to check the option to add python to PATH**

### **Git (To use auto-update)**

Windows: [https://gitforwindows.org/](https://gitforwindows.org/)  
Linux (Ubuntu): sudo apt -y update && sudo apt -y install git

⚠️ **Open a new terminal and type the command to verify that it was installed correctly**
```
git version
```

### <a id="commands"></a>Commands
Install the dependencies by running the command below into the project folder:

```
pip install -r requirements.txt
```
Ready! Now just start the bot with the command, inside the project folder

```
python index.py
```

| commands | OS | description |
| :---: | :---: | :---: |
| ./cmd/update_files.sh | Linux	| Updates all project files except config.yaml and telegram.yaml and Python requirements.txt |
| ./cmd/update.sh | Linux	| Updates only the Python requirements.txt |
| .\cmd\update_files.bat | Windows | Updates all project files except config.yaml and telegram.yaml and Python requirements.txt |
| .\cmd\update.bat | Windows	| Updates only the Python requirements.txt |


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
| game | string | amazon_survival |
| verify_version | boolean - true/false | Check app version every 1h, recommended to keep up to date |
| emoji | boolean - true/false | Enable/Disable show emoji in console messages |
| terminal_colorful | boolean - true/false | Enable/Disable show colored messages on terminal |
| run_time_app | int | Bot loop execution time |
| monitor_to_use | int | Monitor that the bot uses as a reference |
| captcha | boolean - true/false | Enable/Disable in-game captcha recognition |
| speed | string - normal/fast | Two bot speed modes, fast mode is between 1~3 minutes faster |
| authenticate | boolean - true/false | Enable/Disable Login with Username and Password |
| **multi_account** | - | - |
| enable | boolean - true/false | Enable/Disable Multi Account functionality |
| window_title | string | Window title, for identification of the active game by the bot |
| window_fullscreen | boolean - true/false | Enable/Disable Fullscreen mode, recommended for small monitors |
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
| work_button | decimal | Confidence value of work button |
| home_enable_button | decimal | Confidence value of home enable button |
| heroes_green_bar | decimal | Hero's partial green energy bar confidence value |
| heroes_red_bar | decimal | Hero's partial red energy bar confidence value |
| heroes_full_bar | decimal | Hero's full energy bar confidence value |
| heroes_send_all | decimal | Trust value of the send all heroes to work |
| heroes_rest_all | decimal | Trust value of the send all heroes to rest |
| chest | decimal | Confidence value of the chests to calculate the total tokens of the map |
| jail | decimal | Confidence value of the chests to calculate the total jail of the map |
| auth_input | decimal | Confidence value of the input of login |
| heroes.common | decimal | Confidence value of the rarity tag - common |
| heroes.rare | decimal | Confidence value of the rarity tag - rare |
| heroes.super_rare | decimal | Confidence value of the rarity tag - super_rare |
| heroes.epic | decimal | Confidence value of the rarity tag - epic |
| heroes.legend | decimal | Confidence value of the rarity tag - legend |
| heroes.super_legend | decimal | Confidence value of the rarity tag - super_legend |
| **heroes** | - | - |
| mode | string - all, green, full | How to send heroes to work.<br />**all** - Sends all heroes without criteria.<br />**green** - Sends heroes with partially green energy<br />**full** - Sends heroes with full energy|
| **list** | - | - |
| scroll_attempts | int | Total scroll the bot will make in the hero list |
| **offsets** | - | - |
| work_button_green | array - [int, int] | Offset for mouse click on WORK button |
| work_button_full | array - [int, int] | Offset for mouse click on WORK button |
| **metamask** | - | - |
| enable | boolean - true/false | Enable/Disable Metamask Auto Login |
| password | string | Password to unlock Metamask to login to the game |
| **services** | - | - |
| telegram | boolean - true/false | Enable/Disable the message sending service for Telegram |
| **log** | |
| save_to_file | boolean - true/false | Enable/Disable save console log to logger.log file |
| console | boolean - true/false | Enable/Disable debugging of some bot information |
| show_print | boolean - true/false | Enable/Disable show a screenshot of the bot analysis |


## <a id="auth-with-user-and-pass"></a>👥 Auth with user and pass

### ⚠️ Don't forget to rename /config/EXAMPLE-accounts.yaml file, to /config/accounts.yaml.  


One account without House
```
1: {username: "your username", password: "your password", house: false, rarity: []}
```

One account with House
```
1: {username: "your username", password: "your password", house: true, rarity: ["super_rare", "legend"]}
```

Multi account without House

```
1: {username: "your username", password: "your password", house: false, rarity: []}
2: {username: "your username", password: "your password", house: false, rarity: []}
3: {username: "your username", password: "your password", house: false, rarity: []}
```

Multi account with/without House

```
1: {username: "your username", password: "your password", house: true, rarity: ["rare", "super_rare"]}
2: {username: "your username", password: "your password", house: false, rarity: []}
3: {username: "your username", password: "your password", house: true, rarity: ["super_legend", "legend", "epic"]}
```

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
### SEN: 0x4847C29561B6682154E25c334E12d156e19F613a  
### PIX: 08912d17-47a6-411e-b7ec-ef793203f836