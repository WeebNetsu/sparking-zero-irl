# Sparking Zero IRL

This software that translates body movements to Sparking Zero gameplay. This was inspired by a video I saw of a guy play Sparking Zero with his XBox Kinnect. This software is open and free to use.

![Preview](./assets/preview.gif)

## Content

- [The Goal](#the-goal)
- [Note](#note)
- [Running and Installing](#running-and-installing)
  - [Install](#install)
  - [Run](#run)
- [Issues And Contributing](#issues-and-contributing)
- [Todo](#todo)

## The Goal

I want to create software that can easily be used as a template to mod other games in the same way. This template should allow many other games to work with a webcam via passing input from movement into the game with minimum modifications required.

## Note

This software is still in early development, check the [change logs](./changelogs.md) for more information. This project contains the Zlib license, it is short and sweet, so give it a read. I welcome any help you want to offer.

## Running and Installing

_Note: Only tested on Windows 11 using [DroidCam](https://droidcam.app/) as a Webcam._

### Install

#### PC Requirements

- [Python](https://www.python.org/) - To run the project
- [PDM](https://pdm-project.org/en/latest/) - Python package management done right
- [VSCode](https://code.visualstudio.com/) - Or any text editor to edit the code
- Decent Spec System, around the ballpark of:
    - RAM: 16GB (minimum)
    - GPU: GTX 1080 TI (recommended)
    - CPU: Ryzen 7 5700X (recommended)
    - Webcam, or [DroidCam](https://droidcam.app/) if you don't have a webcam


#### From Source

1. Clone or download the code onto your system
1. Open the code in your text editor of choice
1. Modify `configs/computer_info.json` to fit your system
    - If using a webcam, specify a number, if DroidCam, web interface seems to work good, just use the correct local IP
1. In the SAME directory, run `pdm install` in your terminal

### Run

1. Open Sparking Zero
1. Run the software `pdm run main.py`

## Issues And Contributing

This project does not have any official support forums or servers, so until then, feel free to use the issues tab.

## Todo

As this project is still in development, here is my ever growing todo list:

- [ ] Punching
- [ ] Ki Blasts
- [ ] Skill 1
- [ ] Skill 2
- [ ] Skill 3 (super)
- [ ] Recharge
- [ ] Ability 1 (L2 + 0)
- [ ] Ability 2 (L2 + up + 0)
- [ ] Guard
- [ ] Throw (regular)
- [ ] Throw (ground)
- [ ] Make software easy to use as a template for other games with minimal modification required
- [x] Make software easy for user to configure
- [ ] Fly Up/Down
- [ ] Dash forward
- [ ] Dash behind character
- [ ] All Counters
- [ ] A bunch of other stuffs

---

If you want to support the work I do, please consider donating to me on one of these platforms:

[<img alt="liberapay" src="https://img.shields.io/badge/-LiberaPay-EBC018?style=flat-square&logo=liberapay&logoColor=white" />](https://liberapay.com/stevesteacher/)
[<img alt="kofi" src="https://img.shields.io/badge/-Kofi-7648BB?style=flat-square&logo=ko-fi&logoColor=white" />](https://ko-fi.com/stevesteacher)
[<img alt="patreon" src="https://img.shields.io/badge/-Patreon-F43F4B?style=flat-square&logo=patreon&logoColor=white" />](https://www.patreon.com/Stevesteacher)
[<img alt="paypal" src="https://img.shields.io/badge/-PayPal-0c1a55?style=flat-square&logo=paypal&logoColor=white" />](https://www.paypal.com/donate/?hosted_button_id=P9V2M4Q6WYHR8)
[<img alt="youtube" src="https://img.shields.io/badge/-YouTube-fc0032?style=flat-square&logo=youtube&logoColor=white" />](https://www.youtube.com/@Stevesteacher/join)
