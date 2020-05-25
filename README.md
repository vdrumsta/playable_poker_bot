# playable_poker_bot
A simple monte carlo implementation of a texas hold'em no limit poker bot that you can play against using PyPokerEngine library.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. These commands are tailored for Linux systems.

### Prerequisites

Python3 - https://docs.python-guide.org/starting/install3/linux/

### Installing

Clone the repo into your desired folder
```
git clone https://github.com/worm00111/playable_poker_bot.git .
```

Install dependencies:
```
pip install -r requirements.txt
```

Apply PyPokerEngine fix for Python3:
```
patch -p1 < other/pypokergui_fix.diff
```

Start the graphical interface (playable on http://localhost:8000/):
```
pypokergui serve src/poker_conf.yaml --port 8000 --speed moderate
```
