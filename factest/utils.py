from .meta_data.data_key_words import DATA_KEY_WORDS


def get_benchmark_code(benchmark_name: str) -> str:
    """
    get benchmark code by benchmark name

    Parameters
    ----------
    benchmark_name : str
        benchmar_name (str): benchmark Name

    Returns
    -------
    str
        benchmark code
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

    Parameters
    ----------
    universe_name : str
        universe name

    Returns
    -------
    str
        universe code
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


def load_data_key_words() -> list:
    """load data keywords

    Returns
    -------
    list
        data keywords
    """
    return DATA_KEY_WORDS
