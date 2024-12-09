## General info
This project illustrates a simple pub/sub system, an architecture with a publisher, a
subscriber and a broker using sockets and threading in Python. Three (3) python files have been created, sub.py which runs the function of a subscriber,
pub.py which runs the function of a publisher and broker.py which runs the function of a broker.

## Language
Project running in Python 3.10.2 version

## Files
broker.py
sub.py
pub.py
publisher1.cmd (publisher's commands)
subscriber1.cmd (subscriber's commands)
subscriptions.txt (storage of sub's preferences, if not exists then created in the path)

## Execution
First, we run broker.py and then we run either sub.py or pub.py in the order we want.
All three are running in localhost.

Example of broker.py parameters is: broker -s 8012 -p 8013
Example of sub.py parameters is: subscriber -i s1 -r 8000 -h 127.0.0.1 -p 8012 -f subscriber1.cmd
Example of pub.py parameters is: -r 8200 -i p1 -f publisher1.cmd -h 127.0.0.1 -p 8013
