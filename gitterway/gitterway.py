#!/usr/bin/env python

import argparse
from configparser import ConfigParser


class ConfigurationError(Exception):
	pass


class GitterWay:
	def __init__(self):
		self.config = ConfigParser()
		self.parser = argparse.ArgumentParser("gitterway")
		self.parser.add_argument(
			"-c",
			"--config",
			type=str,
			dest="config",
			default="/etc/gitterway/gitterway.conf",
			help="Configuration file",
		)
		self.accounts = {}
		for protocol in PROTOCOLS:
			self.accounts[protocol] = {}

	def run(self, args):
		args = self.parser.parse_args(args)
		self.init_config(args.config)
		self.connect_all_accounts()

	def init_config(self, config):
		self.config.read(config)

		for protocol, cls in PROTOCOLS.items():
			for section in self.config.sections():
				if section.count(":") != 1:
					raise ConfigurationError("Bad config key: %r" % (section))

				p, name = section.split(":")
				if protocol == p:
					if name in self.accounts[protocol]:
						raise ConfigurationError("Duplicate account: %r" % (section))

					optkeys = self.config.options(section)
					options = {k: self.config.get(section, k) for k in optkeys}

					self.accounts[protocol][name] = cls(name, options)

	def connect_all_accounts(self):
		for protocol_accounts in self.accounts.values():
			for account in protocol_accounts.values():
				account.connect()


class Account:
	def __init__(self, name, args):
		self.name = name
		self.args = args

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.name)

	def connect(self):
		print("%r: connecting..." % (self))


class IRCAccount(Account):
	pass


class GitterAccount(Account):
	pass


PROTOCOLS = {
	"irc": IRCAccount,
	"gitter": GitterAccount,
}


def main():
	import sys

	app = GitterWay()
	exit(app.run(sys.argv[1:]))


if __name__ == "__main__":
	main()
