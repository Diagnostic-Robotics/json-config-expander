"""
ConfigExpander class makes all work
"""
from copy import deepcopy, copy
from itertools import product, chain


def seq_iter(obj):
	# iterate dict and list in same way
	return obj if isinstance(obj, dict) else range(len(obj))


class ConfigExpander:
	def __init__(self, expand_char='*'):
		self.expand_char = expand_char

	def run_on_each_config(self, base_config, function):
		expanded_configs = self.expand_configs(base_config)
		return [function(deepcopy(config)) for config in expanded_configs]

	def expand_configs(self, base_config):
		"""
		For each child we calculate its versions recursively and create new config with all possible combinations
		"""
		if not isinstance(base_config, dict) and not isinstance(base_config, list):
			return [base_config]
		expanded_config = self._expand_config_children(base_config)
		return self._create_cartesian_product_from_children(expanded_config)

	def _expand_config_children(self, config):
		expanded_config = copy(config)
		for key in seq_iter(expanded_config):
			item = expanded_config[key]
			if isinstance(key, str) and self.expand_char in key:
				if not isinstance(item, list): raise TypeError("You can apply expand only on list")
				# expand each child of item and flatten results to single list
				expanded_config[key] = chain.from_iterable(self.expand_configs(x) for x in item)
			else:
				expanded_config[key] = self.expand_configs(item)
		return expanded_config

	def _create_cartesian_product_from_children(self, expanded_config):
		if isinstance(expanded_config, list):
			# convert items to list, since product returns tuples
			return [list(x) for x in product(*expanded_config)]

		# create dicts from config keys and config product values
		keys = [k.replace(self.expand_char, '') for k in expanded_config.keys()]
		return list(dict(zip(keys, x)) for x in product(*expanded_config.values()))
