import pytest

from config_expander import ConfigExpander


def test_base_config_is_not_expanded():
	base_config = {'a': 12}
	results = ConfigExpander().run_on_each_config(base_config, lambda config: config)
	assert results == [base_config]


def test_base_config_is_expanded_in_one_level():
	base_config = {'a*': [12, 13]}
	results = ConfigExpander().run_on_each_config(base_config, lambda config: config)
	assert results == [{'a': 12}, {'a': 13}]


def test_base_config_is_expanded_in_two_levels():
	base_config = {'a': {'b*': [12, 13]}}
	results = ConfigExpander().run_on_each_config(base_config, lambda config: config)
	assert results == [{'a': {'b': 12}}, {'a': {'b': 13}}]


def test_base_config_is_expanded_twice_in_first_level():
	base_config = {'a*': [12, 13], 'b*': [14, 15]}
	results = ConfigExpander().run_on_each_config(base_config, lambda config: config)
	assert results == [{'a': 12, 'b': 14}, {'a': 12, 'b': 15}, {'a': 13, 'b': 14}, {'a': 13, 'b': 15}]


def test_base_config_is_expanded_in_first_level_and_in_sub_level():
	base_config = {'a*': [{'b': 12, 'c*': [10, 20]}, {'d': 40}]}
	results = ConfigExpander().run_on_each_config(base_config, lambda config: config)
	assert results == [{'a': {'b': 12, 'c': 10}}, {'a': {'b': 12, 'c': 20}}, {'a': {'d': 40}}]


def test_base_config_is_combination_of_expanded_and_not_expanded():
	base_config = {'a*': [12, 13], 'b': [14, 15]}
	results = ConfigExpander().run_on_each_config(base_config, lambda config: config)
	assert results == [{'a': 12, 'b': [14, 15]}, {'a': 13, 'b': [14, 15]}]


def test_running_function_on_each_config():
	base_config = {'a*': [12, 13]}
	results = ConfigExpander().run_on_each_config(base_config, lambda config: config['a'])
	assert results == [12, 13]


def test_expand_char_usage():
	base_config = {'a#': [12, 13]}
	results = ConfigExpander('#').run_on_each_config(base_config, lambda config: config)
	assert results == [{'a': 12}, {'a': 13}]


def test_using_the_expand_char_only_in_lower_level_with_many_levels():
	base_config = {'a': {'b': [{'c': {'d': {'e*': [10, 11]}}}, {'f': 50}]}}
	results = ConfigExpander().run_on_each_config(base_config, lambda config: config)
	assert results == [{'a': {'b': [{'c': {'d': {'e': 10}}}, {'f': 50}]}},
		{'a': {'b': [{'c': {'d': {'e': 11}}}, {'f': 50}]}}]


def test_different_configs_dont_have_same_reference_in_not_expanded_keys():
	base_config = {'a': {'b': 12}, 'c*': [1, 2]}

	def change_values(config):
		if config['c'] == 1:
			config['a']['b'] = 2
		return config

	results = ConfigExpander().run_on_each_config(base_config, change_values)
	assert results == [{'a': {'b': 2}, 'c': 1}, {'a': {'b': 12}, 'c': 2}]


def test_different_configs_dont_have_same_reference_in_expanded_keys():
	base_config = {'a': {'b*': [12, 13]}}

	def change_values(config):
		if config['a']['b'] == 12:
			config['a']['b'] = 2
		return config

	results = ConfigExpander().run_on_each_config(base_config, change_values)
	assert results == [{'a': {'b': 2}}, {'a': {'b': 13}}]


def test_the_base_config_is_immutable():
	base_config = {'a*': [{'b': 12}, {'b': 13}]}

	def change_values(config):
		if config['a']['b'] == 12:
			config['a']['b'] = 2
		return config

	results = ConfigExpander().run_on_each_config(base_config, change_values)
	assert base_config == {'a*': [{'b': 12}, {'b': 13}]}


def test_the_base_config_is_immutable_deeply():
	base_config = {'a*': [{'b': {'c': 12}}, {'b': {'c': 13}}]}

	def change_values(config):
		if config['a']['b']['c'] == 12:
			config['a']['b']['c'] = 2
		return config

	results = ConfigExpander().run_on_each_config(base_config, change_values)
	assert base_config == {'a*': [{'b': {'c': 12}}, {'b': {'c': 13}}]}


def test_illegal_expanded_key_should_throw_exception():
	base_config = {'a*': 12}

	with pytest.raises(Exception):
		assert ConfigExpander().run_on_each_config(base_config, lambda config: config)
