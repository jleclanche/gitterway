import irc.bot


class ConfigurationError(Exception):
	pass


class Account:
	def __init__(self, name, args):
		self.name = name

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.name)

	def connect(self):
		print("%r: connecting..." % (self))

	def register_sink(self, inchan, outserv, outchan):
		print("%r: Messages to %r will be forwarded to %r @ %r" % (self, inchan, outserv, outchan))


class IRCAccount(Account):
	defaults = {
		"nick": "GitterWay",
		"realname": "GitterWay Bot",
		"port": 6667,
	}

	class Bot(irc.bot.SingleServerIRCBot):
		def on_welcome(self, c, e):
			print("Connected.")
			for channel in self._channels_to_join:
				print("Joining %r" % (channel))
				c.join(channel)

	def __init__(self, name, args):
		super().__init__(name, args)

		self._channels_to_join = set()

		if "server" not in args:
			raise ConfigurationError("No IRC server specified for %r" % (self))

		self.server = args["server"]

		for k, v in self.defaults.items():
			setattr(self, k, args.get(k, v))

		try:
			self.port = int(self.port)
		except ValueError:
			raise ConfigurationError("Bad port: %r" % (self.port))

		self.bot = self.Bot([(self.server, self.port)], self.nick, self.realname)

	def connect(self):
		print("Connecting to %r" % (self.server))
		print("Will join %r" % (self._channels_to_join))
		self.bot.start()

	def register_sink(self, inchan, outserv, outchan):
		super().register_sink(inchan, outserv, outchan)
		self._channels_to_join.add(inchan)
		if outserv is self:
			self._channels_to_join.add(outchan)


class GitterAccount(Account):
	pass
