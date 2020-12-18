from .data_service.base_data import BaseDataSource
from .meta_data.data_key_words import DATA_KEY_WORDS


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

def load_data_key_words() -> list:
    """load data keywords

    Returns
    -------
    list
        data keywords
    """
    return DATA_KEY_WORDS


def get_all_stocks(data_source: BaseDataSource):

    return list(data_source.QUOTE.columns)
