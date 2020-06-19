# The Labyrinth

The Labyrinth is a multiplayer cooperative game. The objective is to complete each level by navigating between platforms and finding the hidden coin.

## Prerequisites

Before installing The Labyrinth, be sure you meet the following requirements:

* Python 3.7 installed
* Internet access

## Installation

Install game at [The Labyrinth github repo](https://github.com/jordynmarlow/CloudComputingFinal.git)

## Usage

The game has two roles: Controller and Viewer. Before playing, each player must decide their role. The Controller must navigate the platforms to find the hidden coin, according to the Viewer's instructions. The Viewer, who can see the coin, must tell the Controller how to get to the coin.

The Controller will play the game with:

```bash
python control.py
```

The Viewer will play the game with:

```bash
python view.py
```

By running these scripts, the players will connect to the server and see The Labyrinth splash screen.

### Controls

#### Viewer

The Viewer can see the entire map, but they cannot control the player. However, they can communicate with the Controller via the chat window.

* DEL: activate chat window
* ENTER: send chat/deactivate caht window (only when chat is activated)

#### Controller

The Controller can see everything on the map, except the coin. THey have full control of the player. The Controller can utilize the chat window.

* DEL: activate chat window
* ENTER: send chat/deactivate caht window (only when chat is activated)
* LEFT ARROW: move left
* RIGHT ARROW: move right
* SPACE: jump

## Authors

##### Alexander Gale

* Created initial design and conducted research
* Designed and developed chat window
* Modified chat window for peer-to-peer integration
* Integrated and debugged The Labyrinth game with peer-to-peer

##### Gabriel Weir

* Created initial design and conducted research
* Designed peer-to-peer prototype
* Designed levels for The Labyrinth game
* Documented design, inspiration, bugs, and bug fixes throughout duration of project

##### Jordyn Marlow

* Created initial design and conducted research
* Designed and developed player physics and game mechanics in The Labyrinth
* Modified The Labyrinth game for peer-to-peer integration
* Integrated and debugged The Labyrinth game with peer-to-peer
