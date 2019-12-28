from json_config_expander.cartesian_product_config_expander import expand_configs as cartesian_product_expand_configs
from json_config_expander.find_and_replace_config_expander import expand_configs as find_and_replace_expand_config


class ImplementationTypes:
	CARTESIAN_PRODUCT_BASED = cartesian_product_expand_configs
	FIND_AND_REPLACE_BASED = find_and_replace_expand_config


def expand_configs(base_config, function=None, expand_char='*',
		expand_configs_implementation=ImplementationTypes.FIND_AND_REPLACE_BASED):
	return expand_configs_implementation(base_config, function, expand_char)
