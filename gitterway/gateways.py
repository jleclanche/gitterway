import irc.client


class ConfigurationError(Exception):
	pass


class Account:
	def __init__(self, name, args):
		self.name = name

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.name)

	def connect(self):
		print("%r: connecting..." % (self))


class IRCAccount(Account):
	defaults = {
		"nick": "GitterWay",
		"port": 6667,
	}

	def __init__(self, name, args):
		super().__init__(name, args)

		if "server" not in args:
			raise ConfigurationError("No IRC server specified for %r" % (self))

		self.server = args["server"]

		for k, v in self.defaults.items():
			setattr(self, k, args.get(k, v))

		try:
			self.port = int(self.port)
		except ValueError:
			raise ConfigurationError("Bad port: %r" % (self.port))

	def connect(self):
		print("Connecting to %r" % (self.server))



class GitterAccount(Account):
	pass
