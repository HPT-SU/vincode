from .const import correct_chars, chars_weights
from .raw import translate

__all__ = ['translate', 'valid', 'validate', 'IncorrectVinException', 'find_incorrect_symbols']


class IncorrectVinException(Exception):
    symbols = None

    def __init__(self, *args, **kwargs):
        self.symbols = kwargs.pop('symbols', list())
        super(IncorrectVinException, self).__init__(*args, **kwargs)


def find_incorrect_symbols(vin):
    result = []
    for symbol in vin:
        if symbol not in correct_chars:
            result.append(symbol)
    return result


def check_vin_numbers(vin):
    result = []
    for symbol in vin:
        try:
            int(symbol)
        except ValueError:
            result.append(symbol)

    return result


def valid(vin):
    if not vin or len(vin) != 17 or find_incorrect_symbols(vin):
        return False

    return True


def validate(vin, raise_error=False, additional_chars=None):
    if not vin or len(vin) != 17:
        return False

    trans_data = {
        'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5', 'F': '6', 'G': '7', 'H': '8',
        'J': '1', 'K': '2', 'L': '3', 'M': '4', 'N': '5', 'P': '7', 'R': '9',
        'S': '2', 'T': '3', 'U': '4', 'V': '5', 'W': '6', 'X': '7', 'Y': '8', 'Z': '9',
    }

    if additional_chars:
        if len(additional_chars) > 9:
            raise ValueError('Допустимо добавлять не более 9 символов')
        trans_data.update((str(v), str(k)) for k, v in enumerate(additional_chars, 1))

    trans_vin = translate(vin, trans_data)

    sum = 0
    try:
        for pos, weight in chars_weights.items():
            sum += weight * int(trans_vin[pos - 1])
    except ValueError as e:  # Случай присутствия запрещённого символа
        if raise_error:
            raise IncorrectVinException(e, symbols=check_vin_numbers(trans_vin))
        return False

    delta = sum // 11 * 11
    result = sum - delta
    if result == 10:
        result = 'X'

    return vin[8] == str(result)
