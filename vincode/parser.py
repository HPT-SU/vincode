from pyparsing import *

from .const import symbols, numbers, correct_chars
from .raw import prepare_string

__all__ = ['parse', 'ParseException']

_lparent = Literal('(')
_rparent = Literal(')')
_delimiter = Literal('|')

# Подстановка подчеркиваниями или вопросами
_pattern = Combine(OneOrMore('?'))

# Составные части VIN-кода
vin_word = Word(correct_chars + '?', min=1, max=17)
vin_letter = Word(correct_chars, exact=1)
vin_chars = Word(symbols, min=1, max=13)
vin_numbers = Word(numbers, min=1, max=10)

# Несколько вариантов подстановки в скобках (X, Y), (XX, YY)...
# Матчит также непоследовательные записи вида (X, YY), (XX, YYY, Z)...,
# что не есть очень хорошо.. хотя, кто его знает...
sub_variants = Group(
    Suppress(_lparent) +
    vin_word +
    ZeroOrMore(
        Suppress(_delimiter) + vin_word
    ) +
    Suppress(_rparent)
)

# Вложенные списки вариантов подстановки
deep_variants = Group(
    Suppress(_lparent) +
    vin_word +
    sub_variants +
    ZeroOrMore(
        Suppress(_delimiter) + sub_variants
    ) +
    Suppress(_rparent)
)

# Полный VIN-код
vin_exact = Word(correct_chars, exact=17)

# Частичный VIN-код (с подстановками, подменами и многоточиями
vin_partial = (
        vin_word +
        ZeroOrMore(
            _pattern ^
            sub_variants ^
            deep_variants ^
            vin_word
        )
)

# VIN-код, начинающийся со знака вопроса
vin_prefixed = (
        Literal('?') +
        vin_partial
)

# Диапазон VIN-кодов
# Два полных VIN-кода ОТ и ДО (AAAAAAAAAAAAAA100->AAAAAAAAAAAAAA999)
# Или полный VIN-код начала диапазона и последние цифры конца диапазона: (AAAAAAAAAAAAAA100->999)
vin_range = (
        Group(vin_partial) +
        Literal('->') +
        Group(vin_partial ^ vin_numbers)
)

# Матчер одного кода разных форматов
vin = vin_exact | vin_range | vin_partial | vin_prefixed

# Матчер списка кодов, разделенных символом |
all_vins = Group(vin) + ZeroOrMore(Suppress(_delimiter) + (Group(vin) ^ SkipTo(_delimiter)))


def parse(s):
    return all_vins.parseString(prepare_string(s))
