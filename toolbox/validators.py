import re
import validators
from decimal import Decimal
from datetime import datetime
from pycpfcnpj import cpfcnpj

from toolbox import strings, data_time


def validate_text(text, max_length=0, required=False, verbose=None):
    value = strings.erase_inject_text(text)
    
    if not value:
        if required:
            raise Exception(f'{verbose} obrigatório(a)')
        return value

    if value:
        s = re.search(r"<[^<]+?>", value)
        if not s:
            if max_length and len(value) > max_length:
                raise Exception(f'{verbose} acima de {max_length} caracteres')
            return value
        raise Exception(f'{verbose} apresenta caracteres inválidos')
    
    raise Exception(f'{verbose} inválido(a)')


def validate_choices(selected, choice=[], queryset=None, required=False, verbose=None):
    if not selected:
        if required:
            raise Exception(f'{verbose} obrigatório(a)')
        return selected

    if choice:
        for key, lbl in choice:
            if str(selected) == str(key):
                return selected
        raise Exception(f'{verbose} não é um valor disponível')

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
        raise Exception(f'{verbose} não é um valor disponível')

    return selected


def _re_integer(max_length):
    return r'^[0-9]{{0,{max}}}$'.format(max=max_length)


def validate_integer(value, max_length=10, required=False, verbose=None,
                     minimum=None, maximum=None, above=None, below=None):
    if not value:
        if required:
            raise Exception(f'{verbose} obrigatório(a)')
        return value
    
    if not max_length:
        max_length = 10

    if not bool(re.match(_re_integer(max_length), value or '')):
        raise Exception(f'acima de {max_length} dígitos')

    if len(value) > max_length:
        raise Exception(f'acima de {max_length} dígitos')
    
    if minimum and int(value)<minimum:
        raise Exception(f'deve ser pelo menos {minimum}')
        
    if above and int(value)<=above:
        raise Exception(f'deve ser maior que {above}')
    
    if maximum and int(value)<maximum:
        raise Exception(f'deve ser até {maximum}')
        
    if below and int(value)<=below:
        raise Exception(f'deve ser abaixo de {below}')
    
    return value


def validate_decimal(value, max_digits=10, decimal_places=2, required=False, verbose=None,
                     minimum=None, maximum=None, above=None, below=None):
    if not value:
        if required:
            raise Exception(f'{verbose} obrigatório(a)')
        return value

    value = value.replace(',','.')
    if not '.' in value:
        value = value + '.00'
        
    if not max_length:
        max_length = 10
        
    if not decimal_places:
        decimal_places = 2
        
    try:
        Decimal(value)
    except:
        raise Exception(_(f'{verbose} inválido(a)')
    
    if len(value.split('.')[0]) > max_digits:
        raise Exception(f'acima de {max_digits} dígitos para inteiro')
    
    if len(value.split('.')[1]) > decimal_places:
        raise Exception(f'acima de {decimal_places} dígitos para decimal')
    
    if minimum and Decimal(value)<minimum:
        raise Exception(f'deve ser pelo menos {minimum}')
        
    if above and Decimal(value)<=above:
        raise Exception(f'deve ser maior que {above}')
    
    if maximum and Decimal(value)<maximum:
        raise Exception(f'deve ser até {maximum}')
        
    if below and Decimal(value)<=below:
        raise Exception(f'deve ser abaixo de {below}')

    return value.replace(',', '.')


def validate_email(email, max_length=0, required=False, verbose=None):
    if not email:
        if required:
            raise Exception(f'{verbose} obrigatório(a)')
        return None

    if email.count('@')>1 or ' ' in email:
        raise Exception(f'{verbose} inválido(a)')

    if len(email) > max_length:
        raise Exception(f'acima de {max_length} caracteres')

    EMAIL = '[a-z0-9!#$%&''*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&''*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?'
    if not bool(re.match(EMAIL, email or '')):
        raise Exception(f'{verbose} inválido(a)')
        
    return email


def validate_ddd(value, max_length=0, required=False, verbose=None):
    if not value:
        if required:
            raise Exception(f'{verbose} obrigatório(a)')
        return value

    if len(value) > max_length:
        raise Exception(f'acima de {max_length} dígitos')
    
    if not bool(re.match('^[0-9]{2,3}$', value or '')):
        raise Exception(f'{verbose} inválido(a)')
        
    return value


def validate_phone(value, max_length=0, required=False, verbose=None):
    if not value:
        if required:
            raise Exception(f'{verbose} obrigatório(a)')
        return value

    if len(value) > max_length:
        raise Exception(f'acima de {max_length} dígitos')
    
    if not bool(re.match(r'^[0-9]{8,9}$', value or '')):
        raise Exception(f'{verbose} inválido(a)')
        
    return value


def validate_data(data, required=False, verbose=None):
    if not data:
        if required:
            raise Exception(f'{verbose} obrigatório(a)')
        return None
    
    if not bool(
        re.match(
            r'\d{4}[/|-](0[1-9]|1[012])[/|-](0[1-9]|[12][0-9]|3[01])', 
            data or ''
        )
    ):
        raise Exception(f'{verbose} inválido(a)')
        
    return data


def validate_databr(data, required=False, verbose=None):
    if not data:
        if required:
            raise Exception(f'{verbose} obrigatório(a)')
        return None
    
    if not bool(
        re.match(
            r'^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$', 
            data or ''
        )
    ):
        raise Exception(f'{verbose} inválido(a)')
    return data_time.date_to_db(data)


def validate_cpfcnpj(value, required=False, verbose=None):
    value = ''.join([c for c in str(value) if c.isdigit()])
    if not value:
        if required:
            raise Exception(f'{verbose} obrigatório(a)')
        return value
    
    if not cpfcnpj.validate(value):
        raise Exception(f'{verbose} inválido(a)')
        
    return value


def validate_url(text, max_length=0, required=False, verbose=None):
    status, text = validate_text(text, 
        max_length=max_length, 
        required=required
    )
    if not (status and validators.url(text)):
        raise Exception(f'{verbose} inválido(a)')
    return text

 