from .validation import validate, IncorrectVinException

__all__ = ['fix_vin', 'check_vin_mask', 'split']


def fix_vin(vin: str) -> str:
    trans_table = {
        'i': '1',
        'o': '0',
        'q': '0',
        'а': 'a',
        'в': 'b',
        'д': 'd',
        'е': 'e',
        'к': 'k',
        'м': 'm',
        'н': 'h',
        'о': '0',
        'р': 'p',
        'с': 'c',
        'т': 't',
        'у': 'y',
        'х': 'x',
        'ч': '4',
    }
    trans = vin.maketrans(trans_table)

    vin = vin.lower().translate(trans).upper()

    return vin


def check_vin_mask(vin: str) -> str | None:
    vin = vin.strip().strip('-').upper()

    if len(vin) != 17:
        return None

    vin = fix_vin(vin)

    try:
        validate(vin, raise_error=True, additional_chars='?')
    except IncorrectVinException:
        return None
    else:
        return vin


def split(vin):
    vin = vin.upper()
    return {
        'wmi': vin[0:3],
        'country': vin[0:2],
        'spc': vin[3:6],
        'wds': vin[3:9],
        'vis': vin[9:16],
        'checksum': vin[8],
        'year': vin[9],
    }
