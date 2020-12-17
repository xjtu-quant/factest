import re


def format_jq_security_code(code) -> str:
    """format stock code to jqdata style

    Parameters
    ----------
    code : 
        code 

    Returns
    -------
    str
        formatted code
    """

    code = str(code)

    # eg: 600511 300807
    pure_num_pattern = re.compile(r'(\d+)')

    # eg: 600511.sh 300807.sz
    two_bit_suffix_pattern = re.compile(r'(\d{6}).(sh|sz)')
    # eg sh600511 sz300807
    two_bit_prefix_pattern = re.compile(r'(sh|sz)(\d{6})')

    num_mat = pure_num_pattern.match(code)
    tbs_mat = two_bit_suffix_pattern.match(code)
    tbp_mat = two_bit_prefix_pattern.match(code)

    num_code = None
    if num_mat:
        num_code = num_mat.group(0)
    elif tbs_mat:
        num_code = tbs_mat.group(0)
    elif tbp_mat:
        num_code = tbs_mat.group(1)
    else:
        return code

    num_code = num_code.zfill(6)

    if num_code[0] == '6' or num_code[0] == '5':
        return num_code + '.XSHG'
    else:
        return num_code + '.XSHE'
