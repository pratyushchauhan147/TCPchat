# TCP Chat Application (Socket Programing with Python) 

## Overview
This is a TCP-based chat client with a graphical user interface (GUI) built using Tkinter. It allows users to connect to a server, send and receive messages in real-time, and receive notifications when new messages arrive while the application is minimized.

## Features
- Real-time chat with a server.
- GUI built with Tkinter.
- Scrollable text area for chat messages.
- Input field for sending messages.
- Notifications for new messages when the window is minimized.
- Simple **authentication** with nickname and password.
## Commands
**/list** - list all the connect socket information
**/close** -End the program
**/listname** - list all the users
**/hid** **<message>** - send a anonymous message
**/msg** **<username>** **<message>** - send a Private message to a user

## Dependencies
- `socket`
- `threading`
- `tkinter`
- `plyer`

You can install the required dependencies using:
```bash
pip install plyer
pip install tk
```
# NOTE:
- Server might refuse to connect under a firewall


