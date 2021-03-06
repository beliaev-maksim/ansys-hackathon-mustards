# Task

You are the executive committee in an anarcho-syndicalist commune and as a way of keeping the 
masses under control you want to examine whether chemtrails would actually work. This project is 
about writing a simple tool that will calculate for you the approximate area covered by a 
chemtrail-distribution system based on flight paths supplied by the user and the additional energy required 
to carry that payload alongside regular passengers. Results should be in the form of square meters covered and
energy cost in Joules, as well as an optional visual representation on a map and the density of the gas at ground level. 
The threshold gas level for visualization on the ground, as well as the plane height, should be specifiable by the user.

# Game interface
You can find screenshots of game interface following [this link](docs/game_interface.md)

# Installation Instruction
You can start the game directly from compiled executable, just unpack the archive and 
run `game.exe` [->download<-](https://github.com/beliaev-maksim/ansys-hackathon-mustards/releases/download/0.0.1/game.exe)

> Note: due to antivirus check start of the game may take up to 80 seconds

Alternatively, you can run via your Python Interpreter of version 3.7+.  
* Download source code from [source.zip](https://github.com/beliaev-maksim/ansys-hackathon-mustards/archive/refs/tags/0.0.1.zip)  
* Unpack the archive
* Open windows command line in unpacked folder 
* Run following code to start the game:
  ```bash
  pip install .
  mustards_game
  ```

# User Guide
The user can control the UFO using the keyboard.
* To change altitude use Up and Down arrow:

    ![Upkey](mustards_game/sprites/UpDown.png)

* To rotate use left and right arrow:

    ![Upkey](mustards_game/sprites/LeftRight.png)
    
The goal is to cover the maximum area without crashing with an obstacle or the screen border.

# What did we learn

Our main idea when joining the Hackathon was to create something interesting and having fun.
Here some bullet Points of our main lessons we learned: 

* How to set project goals
* How to split tasks among all team members
* Utilize GitHub platform to effectively collaborate
* Practice working in an agile environment
* Create project configuration files, eg. leverage pyproject.toml file
* Build a local virtual python environment
* Create and review Pull Requests
* Analyse and optimize code runtime
* Document code in uniform style (numpy)
* Manage code quality using automated tools like `pre-commit` and `black`
