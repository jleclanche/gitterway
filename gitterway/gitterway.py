#!/usr/bin/env python

import argparse
import importlib
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

	def run(self, args):
		args = self.parser.parse_args(args)
		self.init_config(args.config)
		self.connect_all_accounts()

	def init_config(self, config):
		self.config.read(config)

		if not self.config.has_section("protocols"):
			raise ConfigurationError("No protocols defined in config file.")

		protocol_classes = {}
		for protocol in self.config.options("protocols"):
			path, _, name = self.config.get("protocols", protocol).rpartition(".")
			module = importlib.import_module(path)
			protocol_classes[protocol] = getattr(module, name)

		for protocol, cls in protocol_classes.items():
			self.accounts[protocol] = {}

			for section in self.config.sections():
				if section.count(":") != 1:
					# Not a protocol key
					continue

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


def main():
	import sys

	app = GitterWay()
	exit(app.run(sys.argv[1:]))


if __name__ == "__main__":
	main()
