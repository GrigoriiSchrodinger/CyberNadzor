import re


def formatting(number):
    # TODO сдедать форматирование 27,5 >> 27,500
    if isinstance(number, float):
        return '{:,.2f}'.format(number)

    number = re.sub(r'[^0-9.]', '', str(number))
    parts = number.split('.')
    integer_part = format(int(parts[0]), ',')
    if len(parts) == 1:
        return integer_part
    else:
        return integer_part + '.' + parts[1]
