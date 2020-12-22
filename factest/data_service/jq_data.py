from .base_data import BaseDataSource, Data
from jqdatasdk.api import get_fundamentals, get_index_stocks, get_price, get_trade_days
from jqdatasdk.utils import query
from jqdatasdk.finance_service import valuation

import pandas as pd
from .utils import format_jq_security_code


def format_factor(data: pd.DataFrame) -> pd.DataFrame:
    """format data

    Parameters
    ----------
    data : pd.DataFrame
        raw data

    Returns
    -------
    pd.DataFrame
        formatted data
    """

    data.set_index(['time', 'code'], inplace=True)
    data.sort_index(inplace=True)
    data.index.names = ['date', 'asset']
    data.columns = ['factor']

    return data


def get_index_code(index_name: str) -> str:
    """get index code by index name

    Parameters
    ----------
    index_name : str
        index name. support 'hs300', 'zz500', 'zz800', 'zz1000', 'zzqz'

    Returns
    -------
    str
        index code in jqdata. 
    """
    if index_name == 'hs300':
        return '000300.XSHG'
    elif index_name == 'zz500':
        return '399905.XSHE'
    elif index_name == 'zz800':
        return '000906.XSHG'
    elif index_name == 'zz1000':
        return '000852.XSHG'
    elif index_name == 'zzqz':
        return '000985.XSHG'


def get_jq_price(data: pd.DataFrame, name: str, universe, begin_date, end_date, fq=None) -> pd.DataFrame:
    """if data is empty, get price data from jqdata.

    Parameters
    ----------
    data : pd.DataFrame
        original data
    name : str
        price type name
    universe :
        stocks
    begin_date :
        begin date
    end_date :
        end date
    fq : optional
        Restoration of rights information. Support 'post' 'pre', 'None'. by default None

    Returns
    -------
    pd.DataFrame
        price data
    """
    if data is None:
        data = get_price(universe, end_date=end_date, start_date=begin_date, fields=[
                         name], fq=fq, panel=False)
        # format data
        data = format_factor(data)

    return data


def get_jq_fundamentals(data: pd.DataFrame, name, universe, begin_date, end_date) -> pd.DataFrame:
    """ if data is empty, get fundamenta data from jqdata.

    Parameters
    ----------
    data : pd.DataFrame
        original data
    name :  
        fundamental data type. eg: valuation.circulating_market_cap
    universe :  
        stocks
    begin_date :  
        begin date
    end_date :  
        end date

    Returns
    -------
    pd.DataFrame
        fundamental data with multi-index
    """
    if data is None:
        data = pd.DataFrame()
        trade_days = get_trade_days(end_date=end_date, start_date=begin_date)
        for trade_day in trade_days:
            q = query(valuation.code, name).filter(
                valuation.code.in_(universe))
            one_day_data = get_fundamentals(q, trade_day)
            one_day_data['time'] = pd.Timestamp(trade_day)
            data = data.append(one_day_data)
        # format data
        data = format_factor(data)
    return data


def get_jq_index_price(data: pd.DataFrame, index_name: str, name: str, begin_date, end_date, fq='pre') -> pd.DataFrame:
    """if data is empty, get index price data from jqdata.

    Parameters
    ----------
    data : pd.DataFrame
        original data
    index_name : str
        index name
    name : str
        data column name. eg: 'open', 'close'
    begin_date :
        begin date
    end_date : [type]
        end date
    fq : str, optional
        Restoration of rights information., by default 'pre'

    Returns
    -------
    pd.DataFrame
        index price data
    """
    index_code = get_index_code(index_name)
    if data is None:
        data = get_price(index_code, end_date=end_date,
                         start_date=begin_date, fields=name, fq=fq, panel=False)
        data.index.name = 'date'
        data.rename(columns={'open': 'factor'}, inplace=True)

    return data


def get_jq_quote(data: pd.DataFrame, universe, price_type: str, begin_date, end_date) -> pd.DataFrame:
    """ get quote data from jqdata.

    Parameters
    ----------
    data : pd.DataFrame
        original data
    universe : [type]
        stocks
    price_type : str
        price type. eg: 'next_open'
    begin_date :
        begin date
    end_date :
        end date
    Returns
    -------
    pd.DataFrame
        [quote data with multi-index
    """
    if data is None:

        data = get_price(universe, end_date=end_date,
                         start_date=begin_date, fields=price_type, panel=False, fq='pre')
        data.set_index(['time', 'code'], inplace=True)
        data = pd.DataFrame(data.unstack())
        data = data[price_type]

    return data.shift(-1)


def get_universe(stocks, date):
    """get stock universe

    Parameters
    ----------
    stocks : str or sequence
        stock universe
    date :
        index date

    Returns
    -------
    stock universe
    """

    if isinstance(stocks, str):
        index_code = get_index_code(stocks)
        return get_index_stocks(index_code)
    else:
        stocks = list(map(format_jq_security_code, stocks))
    return stocks


class JQData(BaseDataSource):

    def __init__(self, begin_date='2015-01-01', end_date='2018-01-01', deal_method='close', universe='hs300', benchmark=None):

        BaseDataSource.__init__(
            self, begin_date, end_date, deal_method, benchmark)
        self._universe = get_universe(universe, begin_date)
        self.__data = Data()

    def __clear_all_data(self):
        """set all data to None
        """
        self.__data = Data()

    def set_universe(self, stocks):
        """set universe

        Parameters
        ----------
        stocks : str or sequence
            stock poll
        """
        self._universe = get_universe(stocks, self._end_date)
        self.__clear_all_data()

    def set_date_range(self, begin_date, end_date):

        self._begin_date = begin_date
        self._end_date = end_date
        self.__clear_all_data()

    def set_benchmark(self, benchmark: str):
        """set benchmark 

        Parameters
        ----------
        benchmark : str
            benchmark code
        """
        self._benchmark = benchmark
        self.__clear_all_data()

    def set_deal_method(self, deal_method):
        """set deal method

        Parameters
        ----------
        deal_method :
            deal method
        """
        self._deal_method = deal_method
        self.__clear_all_data()

    @property
    def universe(self):
        """get universe

        Returns
        -------
            universe
        """
        return self._universe

    @property
    def QUOTE(self) -> pd.DataFrame:

        name = self._deal_method
        self.__data.quote = get_jq_quote(self.__data.quote, self.universe,
                                         name, self.begin_date, self.end_date)
        return self.__data.quote

    @property
    def OPEN(self) -> pd.DataFrame:
        self.__data.open = get_jq_price(
            self.__data.open, 'open', self.universe, self.begin_date, self.end_date, fq=None)

        return self.__data.open

    @property
    def HIGH(self) -> pd.DataFrame:
        self.__data.high = get_jq_price(
            self.__data.high, 'high', self.universe, self.begin_date, self.end_date, fq=None)
        return self.__data.high

    @property
    def LOW(self) -> pd.DataFrame:
        self.__data.low = get_jq_price(
            self.__data.low, 'low', self.universe, self.begin_date, self.end_date, fq=None)
        return self.__data.low

    @property
    def CLOSE(self) -> pd.DataFrame:
        self.__data.close = get_jq_price(
            self.__data.close, 'close', self.universe, self.begin_date, self.end_date, fq=None)
        return self.__data.close

    @property
    def PRECLOSE(self) -> pd.DataFrame:
        self.__data.pre_close = get_jq_price(
            self.__data.pre_close, 'pre_close', self.universe, self.begin_date, self.end_date, fq=None)
        return self.__data.pre_close

    @property
    def VWAP(self) -> pd.DataFrame:
        self.__data.vwap = get_jq_price(
            self.__data.vwap, 'avg', self.universe, self.begin_date, self.end_date, fq=None)
        return self.__data.vwap

    @property
    def VOLUME(self) -> pd.DataFrame:
        self.__data.volume = get_jq_price(
            self.__data.volume, 'volume', self._universe, self.begin_date, self.end_date, fq=None)
        return self.__data.volume

    @property
    def AMOUNT(self) -> pd.DataFrame:
        self.__data.amount = get_jq_price(
            self.__data.amount, 'money', self.universe, self.begin_date, self.end_date, fq=None)
        return self.__data.amount

    @property
    def MCAP(self) -> pd.DataFrame:
        self.__data.mcap = get_jq_fundamentals(
            self.__data.mcap, valuation.circulating_market_cap, self.universe, self.begin_date, self.end_date)
        return self.__data.mcap

    @property
    def ADJCLOSE(self) -> pd.DataFrame:
        self.__data.adj_close = get_jq_price(
            self.__data.adj_close, 'close', self.universe, self.begin_date, self.end_date, fq='pre')
        return self.__data.adj_close

    @property
    def ADJOPEN(self) -> pd.DataFrame:
        self.__data.adj_open = get_jq_price(
            self.__data.adj_open, 'open', self.universe, self.begin_date, self.end_date, fq='pre')
        return self.__data.adj_open

    @property
    def ADJLOW(self) -> pd.DataFrame:
        self.__data.adj_low = get_jq_price(
            self.__data.adj_low, 'low', self.universe, self.begin_date, self.end_date, fq='pre')
        return self.__data.adj_low

    @property
    def ADJHIGH(self) -> pd.DataFrame:
        self.__data.adj_high = get_jq_price(
            self.__data.adj_high, 'high', self.universe, self.begin_date, self.end_date, fq='pre')
        return self.__data.adj_high

    @property
    def ADJVWAP(self) -> pd.DataFrame:
        self.__data.adj_vwap = get_jq_price(
            self.__data.adj_vwap, 'avg', self.universe, self.begin_date, self.end_date, fq='pre')
        return self.__data.adj_vwap

    @property
    def ADJPRECLOSE(self) -> pd.DataFrame:
        self.__data.adj_pre_close = get_jq_price(
            self.__data.adj_pre_close, 'pre_close', self.universe, self.begin_date, self.end_date, fq='pre')
        return self.__data.adj_pre_close

    @property
    def AFCLOSE(self) -> pd.DataFrame:
        self.__data.af_close = get_jq_price(
            self.__data.af_close, 'close', self.universe, self.begin_date, self.end_date, fq='post')
        return self.__data.af_close

    @property
    def AFOPEN(self) -> pd.DataFrame:
        self.__data.af_open = get_jq_price(
            self.__data.af_open, 'open', self.universe, self.begin_date, self.end_date, fq='post')
        return self.__data.af_open

    @property
    def AFHIGH(self) -> pd.DataFrame:
        self.__data.af_high = get_jq_price(
            self.__data.af_high, 'high', self.universe, self.begin_date, self.end_date, fq='post')
        return self.__data.af_high

    @property
    def AFLOW(self) -> pd.DataFrame:
        self.__data.af_low = get_jq_price(
            self.__data.af_low, 'low', self.universe, self.begin_date, self.end_date, fq='post')
        return self.__data.af_low

    @property
    def AFPRECLOSE(self) -> pd.DataFrame:
        self.__data.af_pre_close = get_jq_price(
            self.__data.af_pre_close, 'pre_close', self.universe, self.begin_date, self.end_date, fq='post')
        return self.__data.af_pre_close

    @property
    def TURNOVER(self) -> pd.DataFrame:
        self.__data.turnover = get_jq_fundamentals(
            self.__data.turnover, valuation.turnover_ratio, self.universe, self.begin_date, self.end_date)
        return self.__data.turnover

    @property
    def BENCHMARKINDEXOPEN(self) -> pd.DataFrame:
        self.__data.benchmark_index_open = get_jq_index_price(
            self.__data.benchmark_index_open, self.benchmark, 'open', self.begin_date, self.end_date, fq='pre')
        return self.__data.benchmark_index_open

    @property
    def BENCHMARKINDEXCLOSE(self) -> pd.DataFrame:
        self.__data.benchmark_index_close = get_jq_index_price(
            self.__data.benchmark_index_close, self.benchmark, 'close', self.begin_date, self.end_date, fq='pre')
        return self.__data.benchmark_index_close

    @property
    def BENCHMARKINDEXHIGH(self) -> pd.DataFrame:
        self.__data.benchmark_index_high = get_jq_index_price(
            self.__data.benchmark_index_high, self.benchmark, 'high', self.begin_date, self.end_date, fq='pre')
        return self.__data.benchmark_index_high

    @property
    def BENCHMARKINDEXLOW(self) -> pd.DataFrame:
        self.__data.benchmark_index_low = get_jq_index_price(
            self.__data.benchmark_index_low, self.benchmark, 'low', self.begin_date, self.end_date, fq='pre')
        return self.__data.benchmark_index_low

    @property
    def RET(self) -> pd.DataFrame:
        if self.__data.ret is None:
            self.__data.ret = self.ADJCLOSE / self.ADJPRECLOSE - 1
        return self.__data.ret

    @property
    def CAP(self) -> pd.DataFrame:
        self.__data.cap = get_jq_fundamentals(
            self.__data.cap, valuation.market_cap, self.universe, self.begin_date, self.end_date)
        return self.__data.cap

    @property
    def DEALAMOUNT(self) -> pd.DataFrame:
        pass

    @property
    def DEALVALUE(self) -> pd.DataFrame:
        pass

    @property
    def HIGHLIMIT(self) -> pd.DataFrame:
        pass

    @property
    def LOWLIMIT(self) -> pd.DataFrame:
        pass
