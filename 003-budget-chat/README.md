## Budget Chat

Budget Chat is a simple TCP-based chat room protocol.

Each message is a single line of ASCII text terminated by a newline character ('\n', or ASCII 10). Clients can send multiple messages per connection. Servers may optionally strip trailing whitespace, such as carriage return characters ('\r', or ASCII 13). All messages are raw ASCII text, not wrapped up in JSON or any other format.


See https://protohackers.com/problem/3.
