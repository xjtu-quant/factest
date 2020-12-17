import json
from jqdatasdk import auth

from .data_service.base_data import BaseDataSource


def get_benchmark_code(benchmark_name: str) -> str:
    """get benchmark code by benchmark name

    Args:
        benchmar_name (str): benchmark Name

    Returns:
        str: benchmark code
    """
    benchmark_name == benchmark_name.strip()
    if benchmark_name == '沪深300':
        return 'hs300'
    elif benchmark_name == '中证500':
        return 'zz500'
    elif benchmark_name == '中证800':
        return 'zz800'
    elif benchmark_name == '中证1000':
        return 'zz1000'
    elif benchmark_name == '中证全指':
        return 'zzqz'
    return benchmark_name


def get_universe_code(universe_name: str) -> str:
    """get univese code by universe name

    Args:
        universe_name (str): universe name
    Returns:
        str: universe code
    """
    universe_name = universe_name.strip()
    if universe_name == '沪深300':
        return 'hs300'
    elif universe_name == '中证500':
        return 'zz500'
    elif universe_name == '中证800':
        return 'zz800'
    elif universe_name == '中证1000':
        return 'zz1000'
    elif universe_name == '中证全指':
        return 'zzqz'


def get_peroid_tuple(period_str: str) -> tuple:
    """get periods list by period string like '1 5 10'

    Args:
        period_str (str): period string

    Returns:
        tuple: periods tuple
    """
    return tuple(map(int, period_str.split(' ')))


def login_jqdata(login_info_file):
    """login to jqdata

        Args:
            login_info_file (str): login infomation file

        """
    with open(login_info_file) as f:
        info = json.load(f)
        auth(info['username'], info['password'])


def load_test_config(test_info_file) -> dict:
    """load test config

    Args:
        test_info_file (str): testing config file path

    Returns:
        dict: test info
    """
    info = {}
    with open(test_info_file, encoding='utf8') as f:
        config_info = json.load(f)
        info['benchmark'] = get_benchmark_code(config_info['benchmark'])
        info['begin_date'] = config_info['begin_date']
        info['end_date'] = config_info['end_date']
        info['deal_method'] = config_info['deal_method']
        info['universe'] = get_universe_code(config_info['universe'])
        info['period'] = get_peroid_tuple(config_info['period'])
        info['formula'] = config_info['formula']
        info['quantile'] = int(config_info['quantile'])
        info['weight_method'] = config_info['weight_method']
        info['long_short'] = config_info['long_short']

    return info


def load_data_key_words(key_words_file: str) -> list:
    """load keywords file

    Args:
        key_words_file (str): keywords file

    Returns:
        list: keywords list
    """
    with open(key_words_file, 'r') as f:
        keywords = f.read()

    return keywords.strip().split('\n')


def get_all_stocks(data_source: BaseDataSource):

    return list(data_source.QUOTE.columns)
