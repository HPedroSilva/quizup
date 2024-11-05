def comma_separated_str_to_list(comma_sep_str: str) -> list[str]:
    '''
    Creates and returns a list of values received in a comma separated string
    '''
    if not comma_sep_str or not isinstance(comma_sep_str, str):
        return []
    return [string.strip() for string in comma_sep_str.split(',') if string]
