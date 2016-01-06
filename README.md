# gitter-gateway

A [Gitter](https://gitter.im) IRC gateway in Python, with support for
multiple channel inputs and outputs.

Inspired by [gitter-irc-bot](https://github.com/finnp/gitter-irc-bot).


## Configuration

Configuration file in `/etc/gitter-gateway/gateway.conf`.

Example configuration file:

```ini
[gitter:account1]
apikey = 5b93335b8a83fb71914be1df6da0225e6257d2b0
rooms = org/example1

[gitter:account2]
apikey = ca18b0de85214421a7cc52c83f9b4f080eea6d89
rooms = org, org/example2

[irc:account1]
server = irc.example.com
nick = gitterbot-example
password = hunter2
sasl = true
rooms = #example1, #example2

# Example of a two-way mirror
[gateway:example1]
in = gitter:account1, irc:account1
out = gitter:account1, irc:account1

# Example of a one-way mirror (irc to gitter)
[gateway:example2]
in = irc:account1
out = gitter:account2

# Example of a one-way mirror (gitter to gitter)
[gateway:example3]
in = gitter:account1
out = gitter:account2
```
