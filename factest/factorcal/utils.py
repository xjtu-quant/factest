import re
import pandas as pd

from ..data_service.base_data import BaseDataSource
from .operator import *


def calculate_factor(data: BaseDataSource, formula: str, data_key_words) -> pd.DataFrame:
    """calculate factor values

    Parameters
    ----------
    data : BaseDataSource
        data object
    formula : str
        formulte to calculte factor value
    data_key_words :
        data keywords sequence

    Returns
    -------
    pd.DataFrame
        actor value with multi-index
    """

    data_pattern = '[^A-Za-z\u4e00-\u9fa5]+'

    keywords = re.sub(data_pattern, ' ', formula).strip().split(' ')

    for word in keywords:
        if word in data_key_words:
            exec('{word:} = data.{word:}'.format(word=word))
    # to void AttributeError. The reason is unkown
    formula = '(' + formula.strip() + ')*1'
    return eval(formula)
