import re

from .const import correct_chars, length, trans_russian

replace_newlines = re.compile(r'[\r\n]+', re.U | re.M)
remove_strange_dots = re.compile(r', *\.', re.U)
replace_multidots = re.compile(r'[…]+', re.U)
replace_whitespaces = re.compile(r'[ \t]+', re.U)
replace_pattern_symbols = re.compile(r'[_.*/]', re.U)
replace_delimiters = re.compile(r'[,;]| *и *|или', re.U)
join_pattern_symbols = re.compile(r'(\?) ', re.U)

replace_range_delimiters = re.compile(r' *(по|пo) *', re.I | re.U)

split_similar_codes = re.compile(r'([%(cs)s?]{17})([%(cs)s?]+)' % dict(cs=correct_chars), re.U)
split_similar_codes2 = re.compile(r'(([%(cs)s]{3})[%(cs)s?]+) *(\2[%(cs)s?]+)' % dict(cs=correct_chars), re.U)

split_range_and_other = re.compile(r'([%(cs)s?]+->[%(cs)s?]{17}|[0-9]+) +(.*)' % dict(cs=correct_chars))

add_extra_spaces = re.compile(r'\)', re.U)
remove_extra_spaces = re.compile(r' *(\(|\)|\|) *', re.U)
remove_double_delimiters = re.compile(r'\|\|', re.U)
remove_extra_text = re.compile(r' *(с|С|c) +', re.U)

remove_russian_comments = re.compile(r'\([а-я]+[^)]*\)', re.I | re.U)

remove_trailing_patterns = re.compile(r'[ \|]+[?]+($|\|)', re.U)

remove_all_spaces = re.compile(r' ', re.U)


def translate(vin, trans_src=None):
    if isinstance(trans_src, (list, tuple)):
        trans = str.maketrans(*trans_src)
    elif isinstance(trans_src, dict):
        trans = str.maketrans(trans_src)
    else:
        trans = trans_russian
    return vin.translate(trans)


sparse_len = length * 2 - 1
match_sparse_vin = re.compile(r'[%(cs)s? ]{17,%(maxlen)d}' % dict(cs=correct_chars, maxlen=sparse_len), re.U)


def prepare_string(s):
    s1 = s

    s = s.strip()

    s = replace_newlines.sub(',', s)
    s = remove_russian_comments.sub('', s)
    s = remove_strange_dots.sub(',', s)
    s = replace_multidots.sub('...,', s)
    s = replace_pattern_symbols.sub('?', s)

    # Y V 2 ? ? ? ? A ? ? ? ? ? ? ? ? ?
    if len(s) <= length * 2 - 1:
        sparse_s = translate(s)
        if match_sparse_vin.fullmatch(sparse_s):
            joined_s = remove_all_spaces.sub('', sparse_s)
            if len(joined_s) == length:
                return joined_s

    s = replace_range_delimiters.sub('->', s)
    s = remove_extra_text.sub('', s)

    s = translate(s)

    s = split_similar_codes.sub('\\1,\\2', s)
    s = split_similar_codes2.sub('\\1,\\3', s)
    s = replace_delimiters.sub('|', s)
    s = replace_whitespaces.sub(' ', s)
    s = join_pattern_symbols.sub('\\1', s)
    s = remove_trailing_patterns.sub('\\1', s)

    s = split_range_and_other.sub('\\1|\\2', s)
    s = remove_extra_spaces.sub('\\1', s)
    s = remove_double_delimiters.sub('|', s)

    s = remove_all_spaces.sub('', s)
    s = s.strip('|')

    return s
