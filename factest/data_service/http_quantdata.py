import requests
import pandas as pd

url = 'http://192.168.31.39:5000/dataapi'


def text_to_df(text_data: str) -> pd.DataFrame:
    """transform response text to pandas DataFrame

    Parameters
    ----------
    text_data : str
        response text

    Returns
    -------
    pd.DataFrame
        transformed data
    """
    return pd.read_json(text_data)


def http_get_price(data: pd.DataFrame, universe, start_date, end_date, fields, freq='daily', fq=None) -> pd.DataFrame:

    if data is None:
        str_universe = ' '.join(universe)
        fields_str = ' '.join(fields)
        body = {
            "method": "get_price",
            "security": str_universe,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "frequency": freq,
            "fields": fields
        }
    pass
