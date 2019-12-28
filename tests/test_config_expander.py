import pytest
from json_config_expander.config_expander import expand_configs, ImplementationTypes


def test_base_config_is_not_expanded():
	base_config = {'a': 12}
	results = expand_configs(base_config)
	assert results == [base_config]


def test_base_config_is_expanded_in_one_level():
	base_config = {'a*': [12, 13]}
	results = expand_configs(base_config)
	assert results == [{'a': 12}, {'a': 13}]


def test_base_config_is_expanded_in_two_levels():
	base_config = {'a': {'b*': [12, 13]}}
	results = expand_configs(base_config)
	assert results == [{'a': {'b': 12}}, {'a': {'b': 13}}]


def test_base_config_is_expanded_in_three_levels():
	base_config = {'a': {'b': {'c*': [12, 13]}}}
	results = expand_configs(base_config)
	assert results == [{'a': {'b': {'c': 12}}}, {'a': {'b': {'c': 13}}}]


def test_base_config_is_expanded_twice_in_first_level():
	base_config = {'a*': [12, 13], 'b*': [14, 15]}
	results = expand_configs(base_config)
	assert results == [{'a': 12, 'b': 14}, {'a': 12, 'b': 15}, {'a': 13, 'b': 14}, {'a': 13, 'b': 15}]


def test_base_config_is_expanded_in_first_level_and_in_sub_level():
	base_config = {'a*': [{'b': 12, 'c*': [10, 20]}, {'d': 40}]}
	results = expand_configs(base_config)
	assert results == [{'a': {'b': 12, 'c': 10}}, {'a': {'b': 12, 'c': 20}}, {'a': {'d': 40}}]


def test_base_config_is_combination_of_expanded_and_not_expanded():
	base_config = {'a*': [12, 13], 'b': [14, 15]}
	results = expand_configs(base_config)
	assert results == [{'a': 12, 'b': [14, 15]}, {'a': 13, 'b': [14, 15]}]


def test_running_function_on_each_config():
	base_config = {'a*': [12, 13]}
	results = expand_configs(base_config, lambda config: config['a'])
	assert results == [12, 13]


def test_expand_char_usage():
	base_config = {'a#': [12, 13]}
	results = expand_configs(base_config, expand_char='#')
	assert results == [{'a': 12}, {'a': 13}]


def test_using_the_expand_char_only_in_lower_level_with_many_levels():
	base_config = {'a': {'b': [{'c': {'d': {'e*': [10, 11]}}}, {'f': 50}]}}
	results = expand_configs(base_config)
	assert results == [{'a': {'b': [{'c': {'d': {'e': 10}}}, {'f': 50}]}},
		{'a': {'b': [{'c': {'d': {'e': 11}}}, {'f': 50}]}}]


def test_different_configs_dont_have_same_reference_in_not_expanded_keys():
	base_config = {'a': {'b': 12}, 'c*': [1, 2]}

	def change_values(config):
		if config['c'] == 1:
			config['a']['b'] = 2
		return config

	results = expand_configs(base_config, change_values)
	assert results == [{'a': {'b': 2}, 'c': 1}, {'a': {'b': 12}, 'c': 2}]


def test_different_configs_dont_have_same_reference_in_expanded_keys():
	base_config = {'a': {'b*': [12, 13]}}

	def change_values(config):
		if config['a']['b'] == 12:
			config['a']['b'] = 2
		return config

	results = expand_configs(base_config, change_values)
	assert results == [{'a': {'b': 2}}, {'a': {'b': 13}}]


def test_the_base_config_is_immutable():
	base_config = {'a*': [{'b': 12}, {'b': 13}]}

	def change_values(config):
		if config['a']['b'] == 12:
			config['a']['b'] = 2
		return config

	results = expand_configs(base_config, change_values)
	assert base_config == {'a*': [{'b': 12}, {'b': 13}]}


def test_the_base_config_is_immutable_deeply():
	base_config = {'a*': [{'b': {'c': 12}}, {'b': {'c': 13}}]}

	def change_values(config):
		if config['a']['b']['c'] == 12:
			config['a']['b']['c'] = 2
		return config

	results = expand_configs(base_config, change_values)
	assert base_config == {'a*': [{'b': {'c': 12}}, {'b': {'c': 13}}]}


def test_illegal_expanded_key_should_throw_exception():
	base_config = {'a*': 12}

	with pytest.raises(TypeError):
		assert expand_configs(base_config)


def test_expand_inside_a_not_expanded_list():
	base_config = {'a': [{'b*': [1, 2]}, 10]}

	results = expand_configs(base_config)
	assert results == [{'a': [{'b': 1}, 10]}, {'a': [{'b': 2}, 10]}]


def test_complex_example_on_two_different_implementations():
	base_config = {'a': [{'b*': [1, {'c': {'d': [1, 2, {'e*': [4, 5, 6], 'f': {'g*': [7, 8, 'x']}}]}}]}, 10]}

	results1 = expand_configs(base_config, expand_configs_implementation=ImplementationTypes.FIND_AND_REPLACE_BASED)
	results2 = expand_configs(base_config, expand_configs_implementation=ImplementationTypes.CARTESIAN_PRODUCT_BASED)

	assert results1 == results2
