# 0 - Smoke Test

Accept TCP connections.

Whenever you receive data from a client, send it back unmodified.

Make sure you don't mangle binary data, and that you can handle at least 5 simultaneous clients.

Once the client has finished sending data to you it shuts down its sending side. Once you've reached end-of-file on your receiving side, and sent back all the data you've received, close the socket so that the client knows you've finished.

https://protohackers.com/problem/0.
