import re
from decimal import Decimal
from datetime import datetime

import validators as validatorslib
from pycpfcnpj import cpfcnpj

from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError

from src.utils import strings, data_time


def validate_text(text, max_length=0, required=False, verbose=None,
                  only_digits=False):
    if not text:
        if required:
            raise ValidationError(_(f'{verbose} obrigatório(a)'))
        return text

    value = strings.erase_inject_text(str(text))
    if not value:
        if required:
            raise ValidationError(_(f'{verbose} apresenta caracteres inválidos'))
        return value

    s = re.search(r"<[^<]+?>", value)
    if not s:
        if max_length and len(value) > max_length:
            raise ValidationError(_(f'{verbose} acima de {max_length} caracteres'))

        if only_digits:
            if not value.isdigit():
                raise ValidationError(_(f'{verbose} deve conter apenas digitos.'))

        return value

    raise ValidationError(_(f'{verbose} apresenta caracteres inválidos'))


def validate_html(text, required=False, verbose=None):
    if not text:
        if required:
            raise ValidationError(_(f'{verbose} obrigatório(a)'))
    return text


def validate_choices(selected, choice=[], queryset=None, required=False, verbose=None):
    if not selected:
        if required:
            raise ValidationError(_(f'{verbose} obrigatório(a)'))
        return selected

    if choice:
        for key, lbl in choice:
            if str(selected) == str(key):
                return selected
        raise ValidationError(_(f'{verbose} não é um valor disponível'))

    if queryset:
        if isinstance(selected, list):
            qselected = queryset.filter(pk__in=selected)
            if qselected:
                return qselected
        else:
            try:
                qselected = queryset.filter(pk=selected)
                if qselected:
                    return qselected.get()
            except ValueError:
                pass
        raise ValidationError(_(f'{verbose} não é um valor disponível'))

    return selected


def _re_integer(max_length):
    return r'^[0-9]{{0,{max}}}$'.format(max=max_length)


def validate_integer(value, max_length=10, required=False, verbose=None,
                     minimum=None, maximum=None, above=None, below=None):
    if not value:
        if required:
            raise ValidationError(_(f'{verbose} obrigatório(a)'))
        return value

    if not max_length:
        max_length = 10

    if not bool(re.match(_re_integer(max_length), str(value) or '')):
        raise ValidationError(_(f'{verbose} acima de {max_length} dígitos'))

    if len(str(value)) > max_length:
        raise ValidationError(_(f'{verbose} acima de {max_length} dígitos'))

    if minimum and int(value)<minimum:
        raise ValidationError(_(f'{verbose} deve ser pelo menos {minimum}'))

    if above and int(value)<=above:
        raise ValidationError(_(f'{verbose} deve ser maior que {above}'))

    if maximum and int(value)<maximum:
        raise ValidationError(_(f'{verbose} deve ser até {maximum}'))

    if below and int(value)<=below:
        raise ValidationError(_(f'{verbose} deve ser abaixo de {below}'))

    return value


def validate_decimal(value, max_digits=10, decimal_places=2, required=False, verbose=None,
                     minimum=None, maximum=None, above=None, below=None):
    if not value:
        if required:
            raise ValidationError(_(f'{verbose} obrigatório(a)'))
        return None

    value = str(value)
    value = value.replace(',','.')
    if not '.' in value:
        value = value + '.00'

    if not max_digits:
        max_digits = 10

    if not decimal_places:
        decimal_places = 2

    try:
        Decimal(value)
    except:
        raise ValidationError(_(f'{verbose} inválido(a)'))

    if len(value.split('.')[0]) > max_digits:
        raise ValidationError(_(f'{verbose} acima de {max_digits} dígitos para inteiro'))

    if len(value.split('.')[1]) > decimal_places:
        raise ValidationError(_(f'{verbose} acima de {decimal_places} dígitos para decimal'))

    if minimum and Decimal(value)<minimum:
        raise ValidationError(_(f'{verbose} deve ser pelo menos {minimum}'))

    if above and Decimal(value)<=above:
        raise ValidationError(_(f'{verbose} deve ser maior que {above}'))

    if maximum and Decimal(value)<maximum:
        raise ValidationError(_(f'{verbose} deve ser até {maximum}'))

    if below and Decimal(value)<=below:
        raise ValidationError(_(f'{verbose} deve ser abaixo de {below}'))

    return value.replace(',', '.')


def validate_email(email, max_length=0, required=False, verbose=None):
    if not email:
        if required:
            raise ValidationError(_(f'{verbose} obrigatório(a)'))
        return None

    if email.count('@')>1 or ' ' in email:
        raise ValidationError(_(f'{verbose} inválido(a)'))

    if len(email) > max_length:
        raise ValidationError(_(f'{verbose} acima de {max_length} caracteres'))

    EMAIL = '[a-z0-9!#$%&''*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&''*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?'
    if not bool(re.match(EMAIL, email or '')):
        raise ValidationError(_(f'{verbose} inválido(a)'))

    return email


def validate_ddd(value, max_length=0, required=False, verbose=None):
    if not value:
        if required:
            raise ValidationError(_(f'{verbose} obrigatório(a)'))
        return value

    if len(value) > max_length:
        raise ValidationError(_(f'{verbose} acima de {max_length} dígitos'))

    if not bool(re.match('^[0-9]{2,3}$', value or '')):
        raise ValidationError(_(f'{verbose} inválido(a)'))

    return value


def validate_phone(value, max_length=0, required=False, verbose=None):
    if not value:
        if required:
            raise ValidationError(_(f'{verbose} obrigatório(a)'))
        return value

    if len(value) > max_length:
        raise ValidationError(_(f'{verbose} acima de {max_length} dígitos'))

    if not bool(re.match(r'^[0-9]{8,9}$', value or '')):
        raise ValidationError(_(f'{verbose} inválido(a)'))

    return value


def validate_data(data, required=False, verbose=None):
    if not data:
        if required:
            raise ValidationError(_(f'{verbose} obrigatório(a)'))
        return None

    if not bool(
        re.match(
            r'\d{4}[/|-](0[1-9]|1[012])[/|-](0[1-9]|[12][0-9]|3[01])',
            data or ''
        )
    ):
        raise ValidationError(_(f'{verbose} inválido(a)'))

    return data


def validate_databr(data, required=False, verbose=None):
    if not data:
        if required:
            raise ValidationError(_(f'{verbose} obrigatório(a)'))
        return None

    if not bool(
        re.match(
            r'^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$',
            data or ''
        )
    ):
        raise ValidationError(_(f'{verbose} inválido(a)'))
    return data_time.date_to_db(data)


def validate_cpfcnpj(value, required=False, verbose=None):
    value = ''.join([c for c in str(value) if c.isdigit()])
    if not value:
        if required:
            raise ValidationError(_(f'{verbose} obrigatório(a)'))
        return value

    if not cpfcnpj.validate(value):
        raise ValidationError(_(f'{verbose} inválido(a)'))

    return value


def validate_url(text, max_length=0, required=False, verbose=None,
                 contains=''):
    if not text:
        if required:
            raise ValidationError(_(f'{verbose} obrigatório(a)'))
        return None

    text = validate_text(text,
        max_length=max_length,
        required=required
    )
    if not validatorslib.url(text):
        raise ValidationError(_(f'{verbose} inválido(a)'))

    if contains:
        if not contains.lower() in text.lower():
            raise ValidationError(_(f'{verbose} inválido(a)'))

    return text


def validate_boolean(value, verbose=None, silence=False):

    if str(value).lower() in ('true', 'on'):
        return True

    if str(value).lower() in ('false', 'off', '') or\
        value is None:
        return False

    if not silence:
        raise ValidationError(_(f'{verbose} inválido(a)'))
