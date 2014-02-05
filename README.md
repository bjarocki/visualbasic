visualbasic
===========

## How to run simple test
 * apt-get install python-websocket python-redis redis-server python-tornado
 * feed the sample /tmp/test.log this way : http://pastebin.com/raw.php?i=Mry5xnkH
 * on one console run : python start_server.py
 * on the other one start a websocket client : wsdump ws://localhost:8888/
 * on the third one run this command couple of times to produce some logs input : http://pastebin.com/raw.php?i=Mry5xnkH

## TODO:
 * *comments*: missing comments in the code
 * *settings*: move hardcoded settings into configuration file
 * *requirements.txt*: missing requirements list
 * *setup.py*: missing pip setup
 * *unit tests*: basic unit testing covering
