# Cataclysmic Tanks!
This project is a 2nd person shooter. There's third person shooters and first person shooters but no second person shooters.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/aa1f2e93-97db-46fe-a70f-1837d2edbf06" />

#### ***Note:*** *There is a known bug where the player gets stuck some walls depending on direction*

**This is a bug with the engine and is currently out of scope for us to fix**

Also, there is *ANOTHER* engine bug where it just breaks and gets really laggy if you screenshare your whole screen with something like discord

If you want to screenshare or record your screen, choose the game instead of screencapture.

# How to Play
The goal of the game is to win 7 rounds.


It's a **1v1 KOTH (KING OF THE HILL)** gamemode where the main objective is to contest the "hill" to gain points, the person with the most points at the end of the round wins.

The twist is instead of shooting people through your own perspective you shoot people *through the perspective of cameras you place around the map.*

Each round lasts 3 minutes and is followed by a buy/setup phase where you can buy player upgrades and place/reset cameras.

All hotkeys for controls are inside the escape menu when you load into the game.

## Local multiplayer
For connecting with computers on the same IP address, the other player must connect using the local address shown on the hosting computer's screen in the host game menu.
If your computer is hosting, then localhost will work as well.

## Online multiplayer
For online multiplayer, you must set up port forwarding.

Instead of connecting with your local ip address, your friends must connect via your public ip which can be found with websites like [whatismyipaddress.com](https://whatismyipaddress.com/)

An online guide for port forwarding can be [found here](https://www.noip.com/support/knowledgebase/general-port-forwarding-guide)

The game uses **TCP**, the default port for the game is **port 1983** but it can be set in game.

## Running the project

### Windows
1. Download the [latest windows release](https://github.com/A-Random-Panda/Hack-Club/releases) zip
2. Unzip the file
3. Run main.exe (Note: you may have to unblock the .exe file)

**Note:** The server.exe file may get flagged by some antivirus software ([virustotal of current build as of writing this](https://www.virustotal.com/gui/file/d26d25a339c8bbe1550e66b6ce5854a6807f1fcdc52abeb86e04781849fea882))

I can only pull a trust me bro and say that **it's not.**

You may have to override said antivirus, there are different steps depending on which antivirus

### Run from source
***Requirement: Python 3.12+***
1. Clone the source code
```sh
git clone https://github.com/A-Random-Panda/Hack-Club
```
2. Get the dependancies 
```sh
pip install -r requirements.txt
```
3. Run the main.py file
```sh
python main.py
```
## How the project was made
This project was made in Python3 using the [Ursina](https://www.ursinaengine.org/) library. 

This project also has other requirements, namely pygame ~~for only the clock because the fps is locked for some reason~~, but is mostly built on Ursina and built-in python libraries.

## Build instructions
***Requirement: Python 3.12+***

***Note: Python 3.14 only has expirimental support with Nuitka as of the time I'm writing this.***
1. Clone the source code
```sh
git clone https://github.com/A-Random-Panda/Hack-Club
```
2. Run the build script depending on os:
- **Windows**

*Note: You may need Visual Studio on the build machine*
```
.\build-windows.ps1
```
- **Linux/Mac**

**The build script is no longer supported**

Building on Linux/Mac should work using the same Nuitka commands as in the windows build script without the --windows-console-mode flag, but this is untested!

## Development issues
~~Because this is in the hack club readme guide for whatever reason~~

- Shu Ning
1. Collaboration as a whole was a huge issue in development. This project was a 2 person project between new developers so tech debt added up really fast. Keeping some sort of orgaization and NOT having a single 4000 line python file was a challenge as well.
2. Speaking of lines of code, this is the largest project that either of us has ever worked on, to the point of knowing what is already added, and knowing what is redundant code was a lot.
3. NOT wanting to rewrite whatever I perceive as sphaghetti code was also tough, because some of the code was bad (literally used boolean as a function argument and a function called open_main_menu that doesn't open main menu), but some of it is also just because I am unfamiliar with the other person's code.
4. Personally, being the person to write server code for the first time was an interesting experience, because of how different having to send infomation through packets is. Making it a server instead of peer to peer was a choice made to have to ability to have dedicated servers (me because hack club nest is in Oslo), and making my playtesters NOT have to make them set up port forwarding.

- Harry 
1. I learned a lot about how to use github, and Ursina
2. I got a lot more experience with using classes and splitting code into different files for readability
3. Learning to work with some else on a coding project and trying to make my work readable was a new experience
### AI DISCLOSURE:
**No AI was directly used for the project's code or assets.**

Some AI was used to help explain some concepts and libraries ([Ursina's documentation](https://www.ursinaengine.org/documentation.html) sucks!) and for debugging code snippits... ~~like a lot of them; the code broke a lot~~.

## Credits:
**Thank you for making this project possible!**

Playtesters - [Ivan](https://github.com/ivanding3) and Alec

Tank model - [ProbablyaDoor](https://github.com/ProbablyaDoor)

Brick wall image <a href="https://www.magnific.com/free-photo/weathered-brick-wall-texture_932618.htm">Image by kues on Magnific</a>
