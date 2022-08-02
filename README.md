# Apex
This application simulates an environment containing entities that depend on each other as sources of energy. A food chain arises from the configuration of various entities and their specified diets.

![screenshot](pics/screenshot.PNG)

There are four types of living entities: Chicken, Pig, Cow and Wolf. Each of these attempt to gain energy and reproduce. At the bottom of the food chain is Grass, which chickens, pigs and cows are able to eat. If there is no grass, everything collapses. Living entities spawn excrement when their energy needs are met and this turns into grass over time.

## Controls
At this time, the user can increase/decrease the tick speed, toggle the tick speed limit, manually spawn living entities, restart the simulation, enter debug mode and quit the application.

Key | Action
------------ | -------------
c | spawn a chicken
p | spawn a pig
m | spawn a cow
w | spawn a wolf
up | increase tick speed
down | decrease tick speed
l | toggle tick speed limit
r | restart
d | debug mode
q | quit

## Support
You can find the support discord server [here](https://discord.gg/49J4RHQxhy).

## Authors and acknowledgement
### Developers
Name | Main Contributions
------------ | -------------
Daniel Stephenson | Creator

## Project Info
This project was started in July 2022.

### Inspiration
This project is based on [Kreatures](https://github.com/Stephenson-Software/Kreatures) and [Interakt](https://github.com/Stephenson-Software/Interakt).

### Libraries
This project makes use of [graphik](https://github.com/Preponderous-Software/graphik) and [py_env_lib](https://github.com/Preponderous-Software/py_env_lib).
