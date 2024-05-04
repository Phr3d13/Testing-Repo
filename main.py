#!/usr/bin/env python
import config
import utility
import socket
import time
import re

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

try:
	s = socket.socket()
	s.connect((config.HOST, config.PORT))
	s.send(f"PASS {config.PASS}\r\n".encode("utf-8"))
	s.send(f"NICK {config.NICK}\r\n".encode("utf-8"))
	s.send(f"JOIN {config.CHAN}\r\n".encode("utf-8"))
	connected = True #Socket succefully connected
except Exception as e:
	print(e)
	connected = False #Socket failed to connect

def bot_loop():
	while connected:
		response = s.recv(1024).decode("utf-8")
		if response == "PING :tmi.twitch.tv\r\n":
			s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
			print("Pong")
		else:
			username = re.search(r"\w+", response)[0]
			message = CHAT_MSG.sub("", response)
			print(f"{username}: {response}")
			for pattern in config.BAN_PAT:
				if re.match(pattern, message):
					utility.ban(s, username)
					break
		time.sleep(1 / config.RATE)
if __name__ == "__main__":
	bot_loop()