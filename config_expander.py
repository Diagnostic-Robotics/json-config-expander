import copy


class ConfigExpander:

	def __init__(self, expand_char='*'):
		self.expand_char = expand_char

	def _add_expand_char_to_all_keys_in_path(self, base_config):
		if type(base_config) not in [dict, list]:
			return False

		if type(base_config) == list:
			for base_config_item in base_config:
				if self._add_expand_char_to_all_keys_in_path(base_config_item):
					return True
			return False

		multi_val_keys = [key for key in base_config.keys() if self.expand_char in key]
		if multi_val_keys:
			return True

		for key in base_config.keys():
			if self._add_expand_char_to_all_keys_in_path(base_config[key]):
				base_config[f'{key}{self.expand_char}'] = base_config[key]
				base_config.pop(key)
				return True
		return False

	def expand_configs(self, base_config):
		self._add_expand_char_to_all_keys_in_path(base_config)
		return self._expand_configs_aux(base_config)

	def _expand_configs_aux(self, base_config):
		if type(base_config) != dict:
			return [base_config]

		multi_val_keys = [key for key in base_config.keys() if self.expand_char in key]
		if not multi_val_keys:
			return [base_config]

		expanded_configs = []
		multi_val_key = multi_val_keys[0]

		values = base_config[multi_val_key]
		if type(values) != list:
			values = [values]

		single_val_key = multi_val_key.replace(self.expand_char, '')
		for val in values:
			new_config = copy.deepcopy(base_config)
			sub_expanded_configs = self._expand_configs_aux(val)
			if len(sub_expanded_configs) == 1:
				new_config[single_val_key] = sub_expanded_configs[0]
				new_config.pop(multi_val_key)
			else:
				new_config[multi_val_key] = sub_expanded_configs

			expanded_configs.extend(self._expand_configs_aux(new_config))

		return expanded_configs

	def run_on_each_config(self, base_config, function):
		expanded_configs = self.expand_configs(base_config)
		results = [function(config) for config in expanded_configs]

		return results
