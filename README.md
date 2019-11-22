A little game written with pygame and numpy.

Until the game UI, and requirements.txt are created, here's an explanation on how to get this running: 

- runs on python 3.7
- there are dependencies: pygame, and numpy. I haven’t tested it, but I believe any version of these modules should work.I think that with python installed you should have access to pip in the command line. From there, you should be able to install modules with a command that looks like “pip install pygame” or “python3 -m pip install pygame”. If you dont use python often then I guess there’s no need to configure a separate interpreter, but people usually do. 
- I ran into an issue working on a mac before, as there’s some sort of command line tool that isn’t installed by default, but I figure you probably have them, seeing as you’re a developer. (Or maybe you’re on linux, so it probably doesnt matter) 
- The game should run pretty smoothly. If you experience game lag on mac, the solution is here: https://stackoverflow.com/questions/31685936/pygame-application-runs-slower-on-mac-than-on-pc


oh yeah and I haven't implemented the explanation… essentially you jump from zone to zone, building up a fleet. The goal is to destroy the enemy boss ship. It plays like a traditional RTS where you select ships with boxes, or by left clicking on them. Right clicking is a move order. Other commands are:
- q puts ships into an autonomous fighting mode. You can still issue move/fire commands in this mode. 
- s stops all ships
- w brings up the starmap menu. To warp ships, have them selected in this window and click on an adjacent square. 
- a will make all selected ships fire in the direction of the mouse’s x,y coordinates. Ship accuracy is linked to the number of kills that ship has. 

Still needs work… obviously… some dev tools are still there
- p spawns a planet
- i spawns a friendly ship
- o spawns an enemy ship
- c clears everything (except enemy ships because I forgot about them) 

When I have time someday I’ll finish the UI and explanations, then package it as a .app. That’s a little ways away though. 
