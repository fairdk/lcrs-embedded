def clean_int(str_value):
    numbers = [int(s) for s in str_value.split() if s.isdigit()]
    if len(numbers) == 0:
        return None
    if len(numbers) == 1:
        return numbers[0]
    raise TypeError("Several numbers in result")


def clean_int_boolean(str_value):
    """
    1 = True
    Everything else = False
    """
    return str_value == "1"
