# 2nd person shooter project!
This project is a 2nd person shooter. There's third person shooters and first person shooters but no second person shooters. This is a multiplayer game where the goal is to shoot the other person through cameras that you place around the map

***Note:*** *There is a known bug where the player gets stuck some walls depending on direction*

**This is a bug with the engine and is currently out of scope for us to fix**

# How to Play
Goal of the game is to win 7 rounds.
It's a 1 v 1 KOTH (KING OF THE HILL) gamemode where the main objective is to contest the "hill" to gain points, the person with the most points at the end of the round wins.
The twist is instead of shooting people through your own perspective you shoot people through the perspective of cameras you place around the map.
Each round last 3 minutes and is followed by a buy / setup phase where you can buy player upgrades and place / reset cameras.
All hot keys for controls are inside the escape menu when you load into the game.

## How the project was made
This project was made in Python3 using the [Ursina](https://www.ursinaengine.org/) library.

## Running the project
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

### Windows
1. Download the [latest windows release](https://github.com/A-Random-Panda/Hack-Club/releases) zip
2. Unzip the file
3. Run main.exe (Note: you may have to unblock the .exe file)

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
- **Linux**
```
.\build-linux.sh
```

### AI DISCLOSURE:
**No AI was directly used for the project's code and assets.**

**Some AI was used to help explain some concepts and libraries and for debugging code snippits.**

### Credits:
**Brick wall image <a href="https://www.magnific.com/free-photo/weathered-brick-wall-texture_932618.htm">Image by kues on Magnific</a>**
