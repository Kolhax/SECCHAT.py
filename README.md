# SECCHAT.py

A simple Python socket-based chat room for private chats with people.

## Setup

To set up:

- Edit the first lines of server/server.py.
- Replace "host" with your local IP or "0.0.0.0" if you want to host it on the web.
- If you host it on the web, make sure you correctly do the port forwarding on the TCP protocol.
- Replace "PORT" with the port you want to use.
- Replace "admin" with the admin username.
- Save the modifications. It should look like this:

```
...
HOST = "localhost"
PORT = 65432

admin = "kepar"
...
```
- To create a user, open the command prompt in the "server" directory and run:

```
python3 credsmanager.py
```

- Now, you're ready to go. Open the command prompt in the "server" directory and run:

```
python3 server.py
```

- Users can now connect. (Make sure to create credentials for each user.)

## How to connect to a server

- Open the "client" directory.
- Open the command prompt in this directory and type:

```
python3 client.py
```

- Select the host IP.
- Select the host port.
- If the host and port are correct, a page should open. It's time to log in!
- Chat with your friends.
- Try typing "/help".

## Note for developers:

- In server.py, you can code your own commands. Just go to line 48 or 55 to see an example. :D

### Credits:

Kepar#6326 is always on top.
