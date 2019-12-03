class ConfigExpander:
	def expand_configs(self, config):
		if type(config) != dict:
			return [config]

		config_keys = list(config.keys())
		multi_val_keys = list(filter(lambda key: '*' in key, config_keys))
		if len(multi_val_keys) == 0:
			return [config]

		expanded_configs = []
		multi_val_key = multi_val_keys[0]

		values = config[multi_val_key]
		if type(values) != list:
			values = [values]

		single_val_key = multi_val_key.replace('*', '')
		for val in values:
			new_config = config.copy()
			sub_expanded_configs = self.expand_configs(val)
			if len(sub_expanded_configs) == 1:
				new_config[single_val_key] = sub_expanded_configs[0]
				new_config.pop(multi_val_key)
			else:
				new_config[multi_val_key] = sub_expanded_configs

			expanded_configs.extend(self.expand_configs(new_config))

		return expanded_configs
