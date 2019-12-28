# json-config-expander

Expand **multi optional** configuration to **multiple configurations**.

### Example 1
```
base_config = {'param_1*': [12, 13]}
expand_configs(base_config)
```
Returns:
```
[{'param_1': 12}, {'param_1': 13})
```

### Example 2
```
base_config = {'param_1': {'param_2*': [12, 13]}}
expand_configs(base_config)
```
Returns:
```
[
    {'param_1': {'param_2': 12}}, 
    {'param_1': {'param_2': 13}}
]
```

### Example 3
```
base_config = {'param_1*': [12, 13], 'param_2*': ['a', 'b']}
expand_configs(base_config)
```
Returns:
```
[
    {'param_1': 12, 'param_2': 'a'}, 
    {'param_1': 12, 'param_2': 'b'}, 
    {'param_1': 13, 'param_2': 'a'}, 
    {'param_1': 13, 'param_2': 'b'}
]
```

### Example 4
```
base_config = {
    'param_1*': [
        {'param_2*': [20, 30, 50]},
        {'param_3*': ['Big', 'Small']}
    ]
}
expand_configs(base_config)
```
Returns:
```
[
    {'param_1': {'param_2': 20}}, 
    {'param_1': {'param_2': 30}},
    {'param_1': {'param_2': 50}},  
    {'param_1': {'param_3': 'Big'}},
    {'param_1': {'param_3': 'Small'}}
]
```

### Motivation Scenario
##### You would like to  run a classification task on multiple parameters of multiple classifier types, and see which one performs better:
```
base_config = {
    'classifier*': [
        {'name': 'logistic_regression', 'max_iter*': [100, 200, 300]},
        {'name': 'xgboost', 'n_estimators*': [50, 100, 200], 'max_depth*': [3,4,5]}
    ]
}
```



To returns all the possible configurations of your setting:
```
expand_configs(base_config)
```
Returns:
```
[
    {'classifier': {'name': 'logistic_regression', 'max_iter': 100}}, 
    {'classifier': {'name': 'logistic_regression', 'max_iter': 200}}, 
    {'classifier': {'name': 'logistic_regression', 'max_iter': 300}}, 
    {'classifier': {'name': 'xgboost', 'n_estimators': 50, 'max_depth': 3}}, 
    {'classifier': {'name': 'xgboost', 'n_estimators': 50, 'max_depth': 4}}, 
    {'classifier': {'name': 'xgboost', 'n_estimators': 50, 'max_depth': 5}}, 
    {'classifier': {'name': 'xgboost', 'n_estimators': 100, 'max_depth': 3}}, 
    {'classifier': {'name': 'xgboost', 'n_estimators': 100, 'max_depth': 4}}, 
    {'classifier': {'name': 'xgboost', 'n_estimators': 100, 'max_depth': 5}}, 
    {'classifier': {'name': 'xgboost', 'n_estimators': 200, 'max_depth': 3}}, 
    {'classifier': {'name': 'xgboost', 'n_estimators': 200, 'max_depth': 4}}, 
    {'classifier': {'name': 'xgboost', 'n_estimators': 200, 'max_depth': 5}}
]
```

If you want to run evaluation on each configuration, you need to pass evaluation_function:
```
def evaluation_function(config):
    ...
```

```
results = expand_configs(base_config, evaluation_function)
```

The results list would have all the evaluation results on each config, then you can select the best result for your needs.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


