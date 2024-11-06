import re


def field_attr(field, attr, attr_value):
    previous_value = field.widget.attrs.get(attr, '')
    field.widget.attrs[attr] = f'{previous_value} {attr_value}'.strip()

def validate_cpf(cpf):
    """
    Validate a CPF number using the formula for validation.
    """
    cpf = ''.join(re.findall(r'\d', str(cpf)))
    if (not cpf) or (len(cpf) < 11):
        return False
    new_cpf = cpf[:-2]
    reverse = 10
    total = 0
    for index in range(19):
        if index > 8:
            index -= 9
        total += int(new_cpf[index]) * reverse
        reverse -= 1
        if reverse < 2:
            reverse = 11
            d = 11 - (total % 11)
            if d > 9:
                d = 0
            total = 0
            new_cpf += str(d)
    sequence = new_cpf == str(new_cpf[0]) * len(cpf)
    if cpf == new_cpf and not sequence:
        return True
    return False
