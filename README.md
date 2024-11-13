# OBS Scoreboard

A very simple scoreboard for OBS Studio. It's a simple HTML file that you can add as a browser source in OBS Studio.
You can then set the scores by using the GUI that is included.
You can edit the board style by editing the HTML file. 


## Compiling

You can build your own version for your OS using pyinstaller: `pyinstaller soft.spec`
Or just download the provided Win64 binary from the release page.


## Usage

At startup, you need to provide the IP address of the scoreboard server.
A default localhost:5000 is provided, you don't need to change this value if you are running the server and the client on the same machine.


If you want to run the client on a separate machine, you need to specify the local IP address of the server and the port (which is by default 5000).
You can't quit the app by clicking the X in the topbar, you have to quit using the tray icon.
This is made to avoid closing the client while being livestreaming for example.
