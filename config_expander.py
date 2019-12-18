class ConfigExpander:

	def __init__(self, expand_char='*'):
		self.expand_char = expand_char

	def expand_configs(self, base_config):
		if type(base_config) != dict:
			return [base_config]

		config_keys = list(base_config.keys())
		multi_val_keys = list(filter(lambda key: self.expand_char in key, config_keys))
		if len(multi_val_keys) == 0:
			return [base_config]

		expanded_configs = []
		multi_val_key = multi_val_keys[0]

		values = base_config[multi_val_key]
		if type(values) != list:
			values = [values]

		single_val_key = multi_val_key.replace(self.expand_char, '')
		for val in values:
			new_config = base_config.copy()
			sub_expanded_configs = self.expand_configs(val)
			if len(sub_expanded_configs) == 1:
				new_config[single_val_key] = sub_expanded_configs[0]
				new_config.pop(multi_val_key)
			else:
				new_config[multi_val_key] = sub_expanded_configs

			expanded_configs.extend(self.expand_configs(new_config))

		return expanded_configs

	def run_on_each_config(self, base_config, function):
		expanded_configs = self.expand_configs(base_config)
		results = []
		for config in expanded_configs:
			result = function(config)
			results.append(result)

		return results
