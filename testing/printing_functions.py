def print_success(test_name):
    print("{} - OK".format(test_name))


def print_code_test(test_name, response_code, expected_code):
    if response_code == expected_code:
        return

    print("{} [Expected:{}, Got:{}] - ERROR".format(test_name,
                                                    expected_code,
                                                    response_code))

    exit(1)


def print_fields_exist_test(test_name, fields, expected_fields):
    for field in expected_fields:
        if field not in fields:
            print("{} [Missing field:{}] - ERROR".format(test_name,
                                                         field))
            exit(1)


def print_fields_valid_data_test(test_name, fields, expected_fields_and_values):
    for field in expected_fields_and_values:
        if fields[field] != expected_fields_and_values[field]:
            print("{} [Expected value:{}, Got:{}] - ERROR".format(test_name,
                                                                  expected_fields_and_values[field],
                                                                  fields[field]))
            exit(1)
