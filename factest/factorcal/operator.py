import numpy as np
import pandas as pd
import copy
import statsmodels.formula.api as smf
import statsmodels.api as sm
import talib


def pivot_table(A: pd.DataFrame) -> pd.DataFrame:
    """Transvert  A  to single index
    Args:
        A (pd.DataFrame): data with multi-index
    Returns:
        pd.DataFrame: data with single-index
    """
    return pd.pivot_table(A, values='factor', index='date', columns='asset',
                          fill_value=np.nan, dropna=False)


def stack_table(A: pd.DataFrame) -> pd.DataFrame:
    """Transvert  A  to multi-index
    Args:
        A (pd.DataFrame): data with single-index
    Returns:
        pd.DataFrame: data with multi-index
    """
    A = pd.DataFrame(A.stack(dropna=False))
    A.columns = ['factor']
    return A


def RANK(A: pd.DataFrame) -> pd.DataFrame:
    """sorting cross-section
    Args:
        A (pd.DataFrame): factor data with multi-index
    Returns:
        pd.DataFrame: factor data with multi-index
    """
    return A.groupby('date').rank()+1


def MAX(A: pd.DataFrame, B: pd.DataFrame) -> pd.DataFrame:
    """Max value
    Args:
        A : factor data with multi-indexable
        B : factor data with multi-index
    Returns:
        pd.DataFrame: factor data with multi-index
    """
    A_copy = A * 1
    B_copy = B * 1
    res = A_copy.where(A_copy > B_copy, other=B_copy)
    return res


def MIN(A: pd.DataFrame, B: pd.DataFrame) -> pd.DataFrame:
    """min value
    Args:
        A : factor data with multi-indexable
        B : factor data with multi-index
    Returns:
        pd.DataFrame: factor data with multi-index
    """
    A_copy = A * 1
    B_copy = B * 1
    res = A_copy.where(A_copy < B_copy, other=B_copy)
    return res


def STD(A: pd.DataFrame, n) -> pd.DataFrame:
    """Standard deviation (Time Series)
    Args:
        A (pd.DataFrame): factor data with multi-index
        n: days
    Returns:
        pd.DataFrame: std data with multi-index
    """
    At = pivot_table(A)
    res = At.rolling(n, min_periods=int(n/2)).std()
    res = stack_table(res)
    return res


def CORR(A: pd.DataFrame, B: pd.DataFrame, n) -> pd.DataFrame:
    """Correlation coefficient (Time Series)
    Args:
        A (pd.DataFrame): factor data with index
        B (pd.DataFrame): factor data with index
        n : days
    Returns:    
        pd.DataFrame: corr data with multi-index
    """
    A = A.unstack()
    B = B.unstack()
    res = A.rolling(n).corr(B)
    return res.stack()


def DELTA(A: pd.DataFrame, n) -> pd.DataFrame:
    """DELTA(At-At-n)
    Args:
        A (pd.DataFrame): factor data with multi-index
        n: days
    Returns:
        pd.DataFrame: DELTA data with multi-index
    """
    At = pivot_table(A)
    res = At - At.shift(n)
    res = stack_table(res)
    return res


def LOG(A: pd.DataFrame) -> pd.DataFrame:
    """logarithmic function    
    Args:
        A (pd.DataFrame): factor data with multi-index
    Returns:
        pd.DataFrame: DELTA data with multi-index
    """
    return np.log(A)


def SUM(A: pd.DataFrame, n) -> pd.DataFrame:
    """Sum (Time Series)
    Args:
        A (pd.DataFrame): factor data with multi-index
        n: days
    Returns:
        pd.DataFrame: sum data with multi-index
    """
    At = pivot_table(A)
    res = At.rolling(n, min_periods=int(n/2)).sum()
    res = stack_table(res)
    return res


def ABS(A: pd.DataFrame) -> pd.DataFrame:
    """absolute value
    Args:
        A (pd.DataFrame): factor data with multi-index
    Returns:
        pd.DataFrame: DELTA data with multi-index
    """
    return np.abs(A)


def MEAN(A: pd.DataFrame, n) -> pd.DataFrame:
    """n days Mean (Time Series)
    Args:
        A (pd.DataFrame): factor data with multi-index
        n: days
    Returns:
        pd.DataFrame: mean data with multi-index
    """
    At = pivot_table(A)
    res = At.rolling(n, min_periods=1).mean()
    res = stack_table(res)
    return res


def TSRANK(A: pd.DataFrame, n) -> pd.DataFrame:
    """TSRANK (Time Series)
    It refers to that on a time series X, the sorting value 
    of the last value of each fixed window is calculated circularly 
    in this window. The popular point is to look at the order of 
    the current value of the time series X in the past period of 
    time at each time.
    Args:
        A (pd.DataFrame): factor data with multi-index
        n: days
    Returns:
        pd.DataFrame: TSRANK data with multi-index
    """
    At = pivot_table(A)
    for i in range(len(At.columns)):
        At.iloc[:, i] = At.iloc[:, i].rolling(
            n).apply(lambda x: (np.argsort(x)[-1]+1)/n)
    res = stack_table(At)
    return res


def SIGN(A):
    """SIGN value (1 if A >0;0 if A=0; -1 if A <0 )
    Args:
        A : a number or DataFrame or array
    """
    return np.sign(A)


def COVIANCE(A: pd.DataFrame, B: pd.DataFrame, n) -> pd.DataFrame:
    """covariance (Time Series)
    Args:
        A (pd.DataFrame): factor data with index
        B (pd.DataFrame): factor data with index
        n : days
    Returns:
        pd.DataFrame: cov data with multi-index
    """
    At = pivot_table(A)
    Bt = pivot_table(B)

    for i in range(len(At.columns)):
        colres = []
        for j in range(len(At)):
            if j < n-1:
                colres.append(np.nan)
            else:
                colres.append(At.iloc[j-n+1:j+1, i].cov(Bt.iloc[j-n+1:j+1, i]))
        At.iloc[:, i] = colres
    res = stack_table(At)
    return res


def DELAY(A, n):
    """Data n days ago  (Time Series) At-n
    Args:
        A : data with index
        n : days
    Returns:
        Data n days ago
    """
    At = pivot_table(A)
    res = At.shift(n)
    res = stack_table(res)
    return res


def TSMIN(A: pd.DataFrame, n) -> pd.DataFrame:
    """Sum (Time Series)
    Time series function, minimum in n days
    Args:
        A (pd.DataFrame): factor data with multi-index
        n: days
    Returns:
        pd.DataFrame: std data with multi-index
    """
    At = pivot_table(A)
    res = At.rolling(n, min_periods=1).min()
    res = stack_table(res)
    return res


def TSMAX(A: pd.DataFrame, n) -> pd.DataFrame:
    """Sum (Time Series)
    Args:
        A (pd.DataFrame): factor data with multi-index
        n: days
    Returns:
        pd.DataFrame: std data with multi-index
    """
    At = pivot_table(A)
    res = At.rolling(n, min_periods=1).max()
    res = stack_table(res)
    return res


def PROD(A: pd.DataFrame, n):
    """Multiply (Time Series)
    Args:
        A : factor data List or Series or DataFrame
        n: days
    Returns:
        Multiply data(with the same format with A)
    """
    At = pivot_table(A)
    At_copy = copy.deepcopy(At)
    At_copy.iloc[:, :] = np.nan
    l = len(At.columns)
    for i in range(0, len(At)):
        At_copy.iloc[i, :] = At.iloc[i-n+1:i+1, :].prod()
    res = stack_table(At_copy)
    return res


def PRREGBETAOD(A: pd.DataFrame, B: pd.DataFrame, n) -> pd.DataFrame:
    """ 
    Regression coefficient (B = beta * A + a)
    The regression coefficient of sample A in the first n periods 
    was obtained by regression with B. the Nan value was excluded 
    and the intercept term was added.
    Args:
        A (pd.DataFrame):factor data with multi-index
        B (pd.DataFrame): factor data with multi-index
        n ([type]): days
    Returns:
        pd.DataFrame: Multiply data(with the same format with A)
    """
    def __OLS(X, Y):
        x = X.values
        y = Y.values
        X = sm.add_constant(x)
        est = sm.OLS(y, X).fit()
        return est.params[1]

    At = pivot_table(A)
    Bt = pivot_table(B)

    for i in range(len(At.columns)):
        colres = []
        for j in range(len(At)):
            if j < n-1:
                colres.append(np.nan)
            else:
                colres.append(
                    __OLS(At.iloc[j-n+1:j+1, i], Bt.iloc[j-n+1:j+1, i]))
        At.iloc[:, i] = colres

    res = stack_table(At)
    return res


def TREGRESI(A: pd.DataFrame, B: pd.DataFrame) -> pd.DataFrame:
    """ 
    Truncation regression residuals
    For example, TREGRESI (close, open) returns the residual after 
    the regression of close and open
    Args:
        A (pd.DataFrame):factor data with multi-index
        B (pd.DataFrame): factor data with multi-index
    Returns:
        pd.DataFrame: data with multi-index
    """
    def __OLS(X, Y):
        x = X.values
        y = Y.values
        # X=sm.add_constant(x)
        est = sm.OLS(y, x).fit()
        return est.resid
    At = pivot_table(A)
    Bt = pivot_table(B)

    for i in range(len(At)):
        At.iloc[i, :] = __OLS(At.iloc[i, :], Bt.iloc[i, :])
    res = stack_table(At)
    return res

    return


def SMA(A: pd.DataFrame, n) -> pd.DataFrame:
    """
    Simple moving average (SMA)
    It is the unweighted arithmetic mean of N values
    before a variable. For example, the 10 day simple
    moving average of closing price refers to the average 
    of the closing price of the previous 10 days.
    Args:
        A (pd.DataFrame): [description]
        n ([type]): days
    Returns:
        pd.DataFrame: data with multi-index
    """
    At = pivot_table(A)
    for i in range(len(At.columns)):
        At.iloc[:, i] = talib.SMA(At.iloc[:, i], n)
    res = stack_table(At)
    return res


def WMA(A: pd.DataFrame, n) -> pd.DataFrame:
    """
    Weighted moving average (WMA)
    In technical analysis, the most recent value of wma
    on N days is multiplied by N, the next nearest value
    is multiplied by n-1, and so on until 0.
    Args:
        A (pd.DataFrame): [description]
        n ([type]): days
    Returns:
        pd.DataFrame: data with multi-index
    """
    At = pivot_table(A)
    for i in range(len(At.columns)):
        At.iloc[:, i] = talib.WMA(At.iloc[:, i], n)
    res = stack_table(At)
    return res


def HIGHDAY(A: pd.DataFrame, n) -> pd.DataFrame:
    """
    Maximum distance
    Args:
        A (pd.DataFrame): [description]
        n ([type]): days

    Returns:
        pd.DataFrame: data with multi-index
    """
    return


def LOWDAY(A: pd.DataFrame, n) -> pd.DataFrame:
    """
    Minimum distance
    Args:
        A (pd.DataFrame): [description]
        n ([type]): days

    Returns:
        pd.DataFrame: data with multi-index
    """
    return


def SEQUENCE(n):
    """
    Arithmetic Sequence
    Isochromatic sequence of 1 ~ n
    Args:
        n ([type]): days
    Returns:
        Arithmetic Sequence: 1,2,~，n
    """
    return [i for i in range(1, n+1)]


def SUMAC(A: pd.DataFrame, n) -> pd.DataFrame:
    """
    Accumulation (return sequence)
    Return the n days cumulative result value, for example 
    A
               factor1
    1   stocks    1
    2   stocks    2
    3   stocks    3
    4   stocks    4
    SUMAC(A,2)
               factor1
    2   stocks    3
    3   stocks    5
    4   stocks    7

    Args:
        A (pd.DataFrame): data with multi-index
        n ([type]): days
    Returns:
        pd.DataFrame: data with multi-index
    """
    def __sum(x, n):
        return x.rolling(n).sum()
    At = pivot_table(A)
    for i in range(len(At.columns)):
        At.iloc[:, i] = __sum(At.iloc[:, i], n)
    res = stack_table(At)
    return res


def AND(A, B) -> bool:
    """&
    Args:
        A ([type]): [description]
        B ([type]): [description]
    Returns:
        bool: [description]
    """
    return A and B


def OR(A, B) -> bool:
    """|
    Args:
        A ([type]): [description]
        B ([type]): [description]
    Returns:
        bool: [description]
    """
    return A or B


def TRD(condition: pd.DataFrame, A, B) -> pd.DataFrame:
    """
    Trinomial operation
    Args
        condition (pd.DataFrame): dataframe index by date time(level 0) and asset(level 1), containing bool values  
        A (pd.DataFrame or int): values when condition is True 
        B (pd.DataFrame or int): values when condition is False

    Returns:
        pd.DataFrame: [description]
    """
    if not isinstance(A, pd.DataFrame):
        value = A
        A = condition.copy()
        A[A.columns] = value

    if not isinstance(B, pd.DataFrame):
        value = B
        B = condition.copy()
        B[B.columns] = value

    return A.where(cond=condition, other=B)


def COUNT(condition: pd.DataFrame, n: int):
    """the number of days fits the 'condition' in the past n days

    Args:
        condition (pd.DataFrame): dataframe index by date time(level 0) and asset(level 1), containing bool values 
        n (int): the number of past days
    """
    return condition.rolling(n, center=False, min_periods=n).sum()
