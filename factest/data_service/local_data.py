from .base_data import BaseDataSource, Data
from .utils import format_jq_security_code
import pandas as pd
from functools import wraps


def format_factor(data: pd.DataFrame) -> pd.DataFrame:
    """format factor data

    Parameters
    ----------
    data : pd.DataFrame
        factor data

    Returns
    -------
    pd.DataFrame
        factor
    """

    data.sort_index(inplace=True)
    data.index.names = ['date', 'asset']
    data.columns = ['factor']

    return data


def load_local_data(data_file_dir, start_date, end_date, universe):
    """load data from hdf file

    Parameters
    ----------
    data_file_dir :
        data file path
    start_date :
        start date
    end_date :
        end date
    universe:
        stock pool

    Returns
    -------
    pd.DataFrame
        stock data
    """
    local_data = None
    if isinstance(universe, str):
        if universe == 'all':
            local_data = pd.read_hdf(data_file_dir)
    else:
        local_data = pd.read_hdf(data_file_dir)
        local_data = local_data.iloc[local_data.index.get_level_values(
            'code').isin(list(universe))]

    local_data = local_data.reset_index()
    mask = (local_data.time >= start_date) & (local_data.time <= end_date)
    local_data = local_data[mask]
    local_data.set_index(['time', 'code'], inplace=True)

    data = Data()
    data.open = format_factor(local_data[['open']])
    data.high = format_factor(local_data[['high']])
    data.low = format_factor(local_data[['low']])
    data.close = format_factor(local_data[['close']])
    data.volume = format_factor(local_data[['volume']])
    data.amount = format_factor(local_data[['money']])
    data.high_limit = format_factor(local_data[['high_limit']])
    data.low_limit = format_factor(local_data[['low_limit']])
    data.pre_close = format_factor(local_data[['pre_close']])
    data.vwap = format_factor(local_data[['avg']])

    return data


class LocalData(BaseDataSource):

    def __init__(self, data_dir, begin_date='2015-01-01', end_date='2018-01-01', deal_method='close', universe='all', benchmark=None):

        BaseDataSource.__init__(
            self, begin_date, end_date, deal_method, benchmark)

        self._data_dir = data_dir
        self._universe = universe
        self._data = None

    def __reload_all_data(self):
        """reload all data
        """
        self._data = load_local_data(
            self._data_dir, self._begin_date, self._end_date, self._universe)

    def set_universe(self, universe):
        """set stock universe(stock pool)

        Parameters
        ----------
        universe :
            universe
        """
        if isinstance(universe, str):
            self._universe = universe
        else:
            self._universe = list(map(format_jq_security_code, universe))

        self.__reload_all_data()

    def set_benchmark(self, benchmark: str):
        """set benchmark

        Parameters
        ----------
        benchmark : str
            benchmark name
        """
        self._benchmark = benchmark

    def set_deal_method(self, deal_method):
        """set deal method

        Parameters
        ----------
        deal_method :
            deal method: support 'close', 'open', 'vwap'
        """
        self._deal_method = deal_method

    def set_date_range(self, begin_date, end_date):
        """set date range (begin_date, end_date)

        Parameters
        ----------
        begin_date :
            begin date
        end_date :
            end date
        """
        self._begin_date = begin_date
        self._end_date = end_date
        self.__reload_all_data()

    @property
    def QUOTE(self) -> pd.DataFrame:
        if self._data is None:
            self.__reload_all_data()

        if self._data.quote is None:
            data = None
            if self._deal_method == 'open':
                data = self._data.open
            elif self._deal_method == 'close':
                data = self._data.close
            elif self._deal_method == 'vwap':
                data = self._data.vwap
            data = data.unstack()
            data.columns = [t[1] for t in data.columns]
            # next day
            self._data.quote = data.shift(-1)
        return self._data.quote

    @property
    def OPEN(self) -> pd.DataFrame:
        if self._data is None:
            self.__reload_all_data()
        return self._data.open

    @property
    def HIGH(self) -> pd.DataFrame:
        if self._data is None:
            self.__reload_all_data()
        return self._data.high

    @property
    def LOW(self) -> pd.DataFrame:
        if self._data is None:
            self.__reload_all_data()
        return self._data.low

    @property
    def CLOSE(self) -> pd.DataFrame:
        if self._data is None:
            self.__reload_all_data()
        return self._data.close

    @property
    def PRECLOSE(self) -> pd.DataFrame:
        if self._data is None:
            self.__reload_all_data()
        return self._data.pre_close

    @property
    def VWAP(self) -> pd.DataFrame:
        if self._data is None:
            self.__reload_all_data()
        return self._data.vwap

    @property
    def VOLUME(self) -> pd.DataFrame:
        if self._data is None:
            self.__reload_all_data()
        return self._data.volume

    @property
    def AMOUNT(self) -> pd.DataFrame:
        if self._data is None:
            self.__reload_all_data()
        return self._data.amount

    @property
    def MCAP(self) -> pd.DataFrame:
        pass

    @property
    def ADJCLOSE(self) -> pd.DataFrame:
        pass

    @property
    def ADJOPEN(self) -> pd.DataFrame:
        pass

    @property
    def ADJLOW(self) -> pd.DataFrame:
        pass

    @property
    def ADJVWAP(self) -> pd.DataFrame:
        pass

    @property
    def ADJHIGH(self) -> pd.DataFrame:
        pass

    @property
    def ADJPRECLOSE(self) -> pd.DataFrame:
        pass

    @property
    def AFCLOSE(self) -> pd.DataFrame:
        pass

    @property
    def AFOPEN(self) -> pd.DataFrame:
        pass

    @property
    def AFHIGH(self) -> pd.DataFrame:
        pass

    @property
    def AFLOW(self) -> pd.DataFrame:
        pass

    @property
    def AFPRECLOSE(self) -> pd.DataFrame:
        pass

    @property
    def DEALAMOUNT(self) -> pd.DataFrame:
        pass

    @property
    def DEALVALUE(self) -> pd.DataFrame:
        pass

    @property
    def TURNOVER(self) -> pd.DataFrame:
        pass

    @property
    def BENCHMARKINDEXOPEN(self) -> pd.DataFrame:
        pass

    @property
    def BENCHMARKINDEXCLOSE(self) -> pd.DataFrame:
        pass

    @property
    def BENCHMARKINDEXHIGH(self) -> pd.DataFrame:
        pass

    @property
    def BENCHMARKINDEXLOW(self) -> pd.DataFrame:
        pass

    @property
    def RET(self) -> pd.DataFrame:
        pass

    @property
    def CAP(self) -> pd.DataFrame:
        pass

    @property
    def HIGHLIMIT(self) -> pd.DataFrame:
        pass

    @property
    def LOWLIMIT(self) -> pd.DataFrame:
        pass
