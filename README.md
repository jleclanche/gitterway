# GitterWay

A [Gitter](https://gitter.im) IRC gateway in Python, with support for
multiple channel inputs and outputs.

Inspired by [gitter-irc-bot](https://github.com/finnp/gitter-irc-bot).


## Configuration

Configuration file is in `/etc/gitter-gateway/gateway.conf`.

GitterWay works by defining accounts in the services you want to use,
then defining "gateways" with inputs and outputs.

For example, to set up a two-way gateway between Gitter and IRC, you
would define a `gitter` account, an `irc` account and a gateway with
both gitter and irc as inputs *and* outputs.

See `gateway.conf.sample` for an example configuration file.
