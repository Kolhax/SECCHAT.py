
# SECCHAT.py

A simply python socket based chat room to privately chat with peoples

## Setup

To setup,
- Edit the server/server.py first lines
- Replace host by your local ip or "0.0.0.0" if you want to hos it www
- - if u host it www make sure you do the port forward correctly on tcp protocol
- Replace PORT to the port you want to use
- Replace admin to the Admin username
- Save the modifications, should look like this:
```
...
HOST = "localhost"
PORT = 65432

admin = "kepar"
...
```
- to create a user, Open cmd in the "server" directory and do:
```
python3 credsmanager.py
```
- Now you are ready, open cmd in the "server" directory and do:
```
python3 server.py
```
- Users can now connect (make sure to create credentials for each users)
## how to connect to a server
- Open the client directory
- Open cmd in this directory and type:
```
python3 client.py
```
- Select the host ip
- select the host port
- If host and port are correct a page should open, It's time to login!
- Chat with your friends
- try doing "/help"
## Note for developpers:
- In the server.py you can code your own commands, just go to line 48 or 55 to see an example :D

### Credits
Kepar is always on TOP
