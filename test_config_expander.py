from config_expander import ConfigExpander


def test_base_config_is_not_expandable():
	base_config = {'a': 12}
	results = ConfigExpander().run_on_each_config(base_config, lambda config: config)
	assert results == [base_config]


def test_base_config_is_expanded_in_one_level():
	base_config = {'a*': [12, 13]}
	results = ConfigExpander().run_on_each_config(base_config, lambda config: config)
	assert results == [{'a': 12}, {'a': 13}]


def test_base_config_is_expanded_in_two_levels():
	base_config = {'a*': {'b*': [12, 13]}}
	results = ConfigExpander().run_on_each_config(base_config, lambda config: config)
	assert results == [{'a': {'b': 12}}, {'a': {'b': 13}}]


def test_base_config_is_expanded_twice_in_first_level():
	base_config = {'a*': [12, 13], 'b*': [14, 15]}
	results = ConfigExpander().run_on_each_config(base_config, lambda config: config)
	assert results == [{'a': 12, 'b': 14}, {'a': 12, 'b': 15}, {'a': 13, 'b': 14}, {'a': 13, 'b': 15}]


def test_base_config_is_combination_of_expanded_and_not_expanded():
	base_config = {'a*': [12, 13], 'b': [14, 15]}
	results = ConfigExpander().run_on_each_config(base_config, lambda config: config)
	assert results == [{'a': 12, 'b': [14, 15]}, {'a': 13, 'b': [14, 15]}]


def test_running_function_on_each_config():
	base_config = {'a*': [12, 13]}
	results = ConfigExpander().run_on_each_config(base_config, lambda config: config['a'])
	assert results == [12, 13]
