from abc import abstractmethod
import pandas as pd


class BaseDataSource(object):

    def __init__(self, begin_date=None, end_date=None, deal_method='close', benchmark=None):

        self._begin_date = begin_date
        self._end_date = end_date
        self._benchmark = benchmark
        self._deal_method = deal_method

    @property
    def begin_date(self):
        """begin date

        Returns
        -------
            begin date
        """
        return self._begin_date

    @property
    def end_date(self):
        """end date

        Returns
        -------
            end date
        """
        return self._end_date

    @property
    def benchmark(self):
        """benchmark

        Returns
        -------
            benchmark
        """
        return self._benchmark

    @property
    def deal_method(self):
        """deal method

        Returns
        -------
            deal method
        """
        return self._deal_method

    @abstractmethod
    def set_benchmark(self, benchmark: str):
        """set benchmark

        Parameters
        ----------
        benchmark : str
            benchmark
        """
        pass

    @abstractmethod
    def set_universe(self, universe):
        """set universe

        Parameters
        ----------
        universe : 
            universe
        """
        pass

    @abstractmethod
    def set_deal_method(self, deal_method):
        """set deal method

        Parameters
        ----------
        deal_method :
            deal method
        """
        pass

    @abstractmethod
    def set_date_range(self, begin_date, end_date):
        """set date range (begin_date, end_date)

        Parameters
        ----------
        begin_date :
            begin date
        end_date :
            end date
        """
        pass

    @property
    @abstractmethod
    def QUOTE(self) -> pd.DataFrame:
        """stock prices

        Returns
        -------
        pd.DataFrame
            stock prices
        """
        pass

    @property
    @abstractmethod
    def OPEN(self) -> pd.DataFrame:
        """open price

        Returns
        -------
        pd.DataFrame
            open price
        """
        pass

    @property
    @abstractmethod
    def HIGH(self) -> pd.DataFrame:
        """highest price

        Returns
        -------
        pd.DataFrame
            highest price
        """
        pass

    @property
    @abstractmethod
    def LOW(self) -> pd.DataFrame:
        """lowest price

        Returns
        -------
        pd.DataFrame
            lowest price
        """
        pass

    @property
    @abstractmethod
    def CLOSE(self) -> pd.DataFrame:
        """close price

        Returns
        -------
        pd.DataFrame
            close price
        """
        pass

    @property
    @abstractmethod
    def PRECLOSE(self) -> pd.DataFrame:
        """pre close price

        Returns
        -------
        pd.DataFrame
            pre close price
        """
        pass

    @property
    @abstractmethod
    def VWAP(self) -> pd.DataFrame:
        """volume weighted average price

        Returns
        -------
        pd.DataFrame
            volume weighted average price
        """
        pass

    @property
    @abstractmethod
    def VOLUME(self) -> pd.DataFrame:
        """trade volume

        Returns
        -------
        pd.DataFrame
            trade volume
        """
        pass

    @property
    @abstractmethod
    def AMOUNT(self) -> pd.DataFrame:
        """trade money amount

        Returns
        -------
        pd.DataFrame
            trade money amount
        """
        pass

    @property
    @abstractmethod
    def MCAP(self) -> pd.DataFrame:
        """circulation market value

        Returns
        -------
        pd.DataFrame
            circulation market value
        """
        pass

    @property
    @abstractmethod
    def ADJCLOSE(self) -> pd.DataFrame:
        """split-adjusted share close prices

        Returns
        -------
        pd.DataFrame
            split-adjusted share close prices
        """
        pass

    @property
    @abstractmethod
    def ADJOPEN(self) -> pd.DataFrame:
        """split-adjusted share open prices

        Returns
        -------
        pd.DataFrame
            split-adjusted share open prices
        """
        pass

    @property
    @abstractmethod
    def ADJLOW(self) -> pd.DataFrame:
        """split-adjusted share open prices

        Returns
        -------
        pd.DataFrame
            split-adjusted share open prices
        """
        pass

    @property
    @abstractmethod
    def ADJVWAP(self) -> pd.DataFrame:
        """split-adjusted share volume weighted average price

        Returns
        -------
        pd.DataFrame
            split-adjusted share volume weighted average price
        """
        pass

    @property
    @abstractmethod
    def ADJHIGH(self) -> pd.DataFrame:
        """split-adjusted share hightest prices

        Returns
        -------
        pd.DataFrame
            split-adjusted share hightest prices
        """
        pass

    @property
    @abstractmethod
    def ADJPRECLOSE(self) -> pd.DataFrame:
        """split-adjusted share pre-close prices

        Returns
        -------
        pd.DataFrame
            split-adjusted share pre-close prices
        """
        pass

    @property
    @abstractmethod
    def AFCLOSE(self) -> pd.DataFrame:
        """post recovery close price

        Returns
        -------
        pd.DataFrame
            post recovery close price
        """
        pass

    @property
    @abstractmethod
    def AFOPEN(self) -> pd.DataFrame:
        """post recovery open price

        Returns
        -------
        pd.DataFrame
            post recovery open price
        """
        pass

    @property
    @abstractmethod
    def AFHIGH(self) -> pd.DataFrame:
        """post recovery highest price

        Returns
        -------
        pd.DataFrame
            post recovery highest price
        """
        pass

    @property
    @abstractmethod
    def AFLOW(self) -> pd.DataFrame:
        """post recovery lowest price

        Returns
        -------
        pd.DataFrame
            post recovery lowest price
        """
        pass

    @property
    @abstractmethod
    def AFPRECLOSE(self) -> pd.DataFrame:
        """post revovery pre close

        Returns
        -------
        pd.DataFrame
            post revovery pre close
        """
        pass

    @property
    @abstractmethod
    def DEALAMOUNT(self) -> pd.DataFrame:
        """[summary]

        Returns
        -------
        pd.DataFrame
            [description]
        """
        pass

    @property
    @abstractmethod
    def DEALVALUE(self) -> pd.DataFrame:
        """[summary]

        Returns
        -------
        pd.DataFrame
            [description]
        """
        pass

    @property
    @abstractmethod
    def TURNOVER(self) -> pd.DataFrame:
        """turnover ratio

        Returns
        -------
        pd.DataFrame
            turnover ratio
        """
        pass

    @property
    @abstractmethod
    def BENCHMARKINDEXOPEN(self) -> pd.DataFrame:
        """benchmark index open price 

        Returns
        -------
        pd.DataFrame
            benchmark index open price 
        """
        pass

    @property
    @abstractmethod
    def BENCHMARKINDEXCLOSE(self) -> pd.DataFrame:
        """benchmark index close price with multi-index

        Returns
        -------
        pd.DataFrame
            benchmark index close price with multi-index
        """
        pass

    @property
    @abstractmethod
    def BENCHMARKINDEXHIGH(self) -> pd.DataFrame:
        """benchmark index highest price with multi-index

        Returns
        -------
        pd.DataFrame
           benchmark index highest price with multi-index
        """
        pass

    @property
    @abstractmethod
    def BENCHMARKINDEXLOW(self) -> pd.DataFrame:
        """benchmark index lowest price with multi-index

        Returns
        -------
        pd.DataFrame
            benchmark index lowest price with multi-index
        """
        pass

    @property
    @abstractmethod
    def RET(self) -> pd.DataFrame:
        """day return

        Returns
        -------
        pd.DataFrame
            day return
        """

        pass

    @property
    @abstractmethod
    def CAP(self) -> pd.DataFrame:
        """Total market capitalizition

        Returns
        -------
        pd.DataFrame
            Total market capitalizition
        """
        pass

    @property
    @abstractmethod
    def HIGHLIMIT(self) -> pd.DataFrame:
        """hight limit price

        Returns
        -------
        pd.DataFrame
            hight limit price
        """
        pass

    @property
    @abstractmethod
    def LOWLIMIT(self) -> pd.DataFrame:
        """low limit price

        Returns
        -------
        pd.DataFrame
            low limit price
        """
        pass


class Data:
    """data container
    """

    def __init__(self):

        self.quote = None

        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.pre_close = None
        self.vwap = None
        self.volume = None
        self.amount = None
        self.mcap = None
        self.adj_close = None
        self.adj_open = None
        self.adj_high = None
        self.adj_low = None
        self.adj_vwap = None
        self.adj_pre_close = None
        self.af_close = None
        self.af_open = None
        self.af_high = None
        self.af_low = None
        self.af_pre_close = None

        self.deal_amount = None
        self.deal_value = None

        self.turnover = None
        self.benchmark_index_open = None
        self.benchmark_index_close = None
        self.benchmark_index_high = None
        self.benchmark_index_low = None

        self.ret = None
        self.cap = None

        self.high_limit = None
        self.low_limit = None
