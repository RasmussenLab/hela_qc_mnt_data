import hela_data.pandas


def test_create_dict_of_dicts():
    data = {('a', 'a1', 'a2'): 1,
            ('a', 'a1', 'a3'): 2,
            ('b', 'b1', 'b2'): 3,
            ('b', 'b1', 'b3'): 4}
    expected = {
        "a": {'a1': {'a2': 1, 'a3': 2}},
        "b": {'b1': {'b2': 3, 'b3': 4}}
    }
    actual = hela_data.pandas.create_dict_of_dicts(data)
    assert expected == actual

    data = {('a', 'a1', 'a2'): (1, 1),
            ('a', 'a1', 'a3'): (2, 2),
            ('b', 'b1', 'b2'): (3, 3),
            ('b', 'b1', 'b3'): (4, 4)}
    expected = {
        "a": {'a1': {'a2': [1, 1], 'a3': [2, 2]}},
        "b": {'b1': {'b2': [3, 3], 'b3': [4, 4]}}
    }
    actual = hela_data.pandas.create_dict_of_dicts(data, transform_values=list)
    assert expected == actual


def test_flatten_dict_of_dicts():
    expected = {('a', 'a1', 'a2'): 1,
                ('a', 'a1', 'a3'): 2,
                ('b', 'b1', 'b2'): 3,
                ('b', 'b1', 'b3'): 4}
    data = {
        "a": {'a1': {'a2': 1, 'a3': 2}},
        "b": {'b1': {'b2': 3, 'b3': 4}}
    }
    actual = hela_data.pandas.flatten_dict_of_dicts(data)

    assert expected == actual
