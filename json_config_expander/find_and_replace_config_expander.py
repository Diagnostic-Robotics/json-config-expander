import copy


class expand_configs(object):
	def __new__(cls, base_config, function=None, expand_char='*'):
		self = object.__new__(cls)
		self.expand_char = expand_char
		self.type_handle_mapping = {dict: self._handle_dict, list: self._handle_list}
		return self(base_config, function)

	def __call__(self, base_config, function=None):
		if function is not None:
			expanded_configs = self(base_config)
			return [function(config) for config in expanded_configs]

		path = self._find_first_expand_char_path(base_config)
		if path is None:
			return [base_config]

		path_value = self._get_path_value(base_config, path)

		expanded_configs = []
		for value in path_value:
			new_value = copy.deepcopy(value)
			new_config = copy.deepcopy(base_config)
			self._update_value_in_path(new_config, new_value, path)
			expanded_configs.extend(self(new_config))

		return expanded_configs

	def _find_first_expand_char_path(self, base_config):
		base_config_type = type(base_config)
		if base_config_type in self.type_handle_mapping:
			return self.type_handle_mapping[base_config_type](base_config)
		return None

	def _handle_list(self, config_list):
		for index in range(len(config_list)):
			path = self._find_first_expand_char_path(config_list[index])
			if path is not None:
				return [index] + path
		return None

	def _handle_dict(self, config_dict):
		for key in config_dict:
			if self.expand_char in key:
				return [key]

			path = self._find_first_expand_char_path(config_dict[key])
			if path is not None:
				return [key] + path
		return None

	def _update_value_in_path(self, new_config, new_value, path):
		path_value = new_config
		for key_index in range(len(path) - 1):
			key = path[key_index]
			path_value = path_value[key]
		last_key = path[-1]  # The last key must be a string
		key_without_expand_char = last_key.replace(self.expand_char, '')
		path_value[key_without_expand_char] = new_value
		path_value.pop(last_key)

	def _get_path_value(self, base_config, path):
		path_value = base_config
		for key in path:
			path_value = path_value[key]
		if type(path_value) is not list:
			raise TypeError(f'the value of {path} should be a list! ({path_value} is not a list)')
		return path_value
