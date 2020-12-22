
from .data_service.base_data import BaseDataSource

from .factorcal.utils import calculate_factor
from .alphalens.utils import get_clean_factor_and_forward_returns, MaxLossExceededError

from .utils import load_data_key_words, get_benchmark_code
import pandas as pd

import matplotlib.pyplot as plt

import re
from .alphalens import plotting
from .alphalens import performance as perf
from .alphalens import utils
from .alphalens.tears import GridFigure


class FactorTest():

    def __init__(self, dataSource: BaseDataSource):

        self.__data: BaseDataSource = dataSource
        self.__period = None
        self.__formula = None
        self.__quantile = None
        self.__weight_method = None
        self.__long_short = None
        self.__group_neutral = None
        self.__by_group = None

        self.__data_key_words = None
        self.__factor_data = None

        self.__factor_returns = None
        self.__alpha_beta = None
        self.__mean_quant_rateret = None
        self.__mean_ret_spread_quant = None
        self.__mean_quant_rateret_bydate = None
        self.__std_spread_quant = None
        self.__mean_quant_ret_bydate = None

        self.__mean_return_quantile_group = None
        self.__mean_return_quantile_group_std_err = None
        self.__mean_quant_rateret_group = None
        self.__num_groups = None

        self.__ic = None
        self.__mean_monthly_ic = None
        self.__mean_group_ic = None

        self.__quantile_turnover = None
        self.__autocorrelation = None
        self.__turnover_periods = None

        self.__avg_cumulative_returns = None
        self.__avg_cumret_by_group = None

    def __load_data_key_words(self):
        """load data key words. eg: 'OPEN', 'CLOSE'
        """
        self.__data_key_words = load_data_key_words()

    def __clear_data(self):
        """clear data
        """
        self.__factor_data = None

    def factor_data(self) -> pd.DataFrame:
        """get merged data
        """
        if self.__factor_data is None:
            factors = self.factors()
            prices = self.prices()
            try_num = 1

            while try_num < 10:
                try:
                    self.__factor_data = get_clean_factor_and_forward_returns(
                        factors, prices, periods=self.__period, quantiles=self.__quantile)
                    break
                except MaxLossExceededError:
                    self.set_quantile(self.__quantile - 1)
                    print('try {try_num:}--decreasing quantile number to: {quantile:}'.format(
                        try_num=try_num, quantile=self.__quantile))
                try_num += 1

        return self.__factor_data

    def factors(self) -> pd.DataFrame:
        """get factor data
        """
        if self.__data_key_words is None:
            self.__load_data_key_words()
        return calculate_factor(self.__data, self.__formula, self.__data_key_words)

    def factor_returns(self):
        return self.__factor_returns

    def mean_quant_ret_bydate(self):
        return self.__mean_quant_rateret_bydate

    @property
    def by_group(self) -> bool:
        return self.__by_group

    @property
    def period(self) -> str:
        return self.__period

    @property
    def formula(self) -> str:
        return self.__formula

    @property
    def quantile(self) -> str:
        return self.__quantile

    @property
    def data_source(self) -> BaseDataSource:
        return self.__data

    @property
    def group_neutral(self) -> bool:
        """get group neutral

        Returns
        -------
        bool
            group neutral
        """
        return self.__group_neutral

    def prices(self) -> pd.DataFrame:
        """get price data
        """
        return self.__data.QUOTE

    def set_by_group(self, by_group: bool):
        self.__by_group = by_group
        self.__clear_data()

    def set_group_neutral(self, group_neutral: bool):
        """set group neutral

        Parameters
        ----------
        group_neutral : bool
            new group neutral
        """
        self.__group_neutral = group_neutral
        self.__clear_data()

    def set_data_source(self, data_source: BaseDataSource):
        """set data source
        """
        self.__data = data_source

    def set_benchmark(self, benchmark: str):
        """set bench mark

        Parameters
        ----------
        benchmark : str
            benchmark
        """
        self.__data.set_benchmark(get_benchmark_code(benchmark))
        self.__clear_data()

    def set_date_range(self, begin_date: str, end_date: str):
        """set date range

        Parameters
        ----------
        begin_date : str
            begin date
        end_date : str
            end date
        """
        self.__data.set_date_range(begin_date, end_date)
        self.__clear_data()

    def set_deal_method(self, deal_method: str):
        """set deal method

        Parameters
        ----------
        deal_method : str
            deal method
        """
        self.__data.set_deal_method(deal_method)
        self.__clear_data()

    def set_universe(self, universe):
        """set universe

        Parameters
        ----------
        universe :
            universe
        """
        if isinstance(universe, str):
            if universe != 'all':
                universe = get_benchmark_code(universe)
        self.__data.set_universe(universe)
        self.__clear_data()

    def set_period(self, period: tuple):
        """set period

        Parameters
        ----------
        period : tuple
            backtesting period
        """
        self.__period = period
        self.__clear_data()

    def set_formula(self, formula: str):
        """set factor formula

        Parameters
        ----------
        formula : str
            factor formula
        """
        self.__formula = formula
        self.__clear_data()

    def set_quantile(self, quantile: int):
        """set quantile

        Parameters
        ----------
        quantile : int
            quantile number
        """
        self.__quantile = quantile
        self.__clear_data()

    def set_weight_method(self, weight_method: str):
        """set weight method

        Parameters
        ----------
        weight_method : str
            weight method
        """
        self.__weight_method = weight_method
        self.__clear_data()

    def set_long_short(self, long_short: bool):
        """set long short

        Parameters
        ----------
        long_short : bool
            if do both long position and short position or not
        """
        self.__long_short = long_short
        self.__clear_data()

    def return_analysis(self):
        """calculate return performance
        """
        factor_data = self.factor_data()
        long_short = self.__long_short
        group_neutral = self.__group_neutral
        equal_weight = False
        if self.__weight_method == 'equal':
            equal_weight = True

        self.__factor_returns = perf.factor_returns(
            factor_data, long_short, group_neutral, equal_weight
        )
        mean_quant_ret, std_quantile = perf.mean_return_by_quantile(
            factor_data,
            by_group=False,
            demeaned=long_short,
            group_adjust=group_neutral,
        )

        self.__mean_quant_rateret = mean_quant_ret.apply(
            utils.rate_of_return, axis=0, base_period=mean_quant_ret.columns[0]
        )

        self.__mean_quant_ret_bydate, std_quant_daily = perf.mean_return_by_quantile(
            factor_data,
            by_date=True,
            by_group=False,
            demeaned=long_short,
            group_adjust=group_neutral,
        )

        self.__mean_quant_rateret_bydate = self.__mean_quant_ret_bydate.apply(
            utils.rate_of_return,
            axis=0,
            base_period=self.__mean_quant_ret_bydate.columns[0],
        )

        compstd_quant_daily = std_quant_daily.apply(
            utils.std_conversion, axis=0, base_period=std_quant_daily.columns[0]
        )

        self.__alpha_beta = perf.factor_alpha_beta(
            factor_data, self.__factor_returns, long_short, group_neutral
        )

        self.__mean_ret_spread_quant, self.__std_spread_quant = perf.compute_mean_returns_spread(
            self.__mean_quant_rateret_bydate,
            factor_data["factor_quantile"].max(),
            factor_data["factor_quantile"].min(),
            std_err=compstd_quant_daily,
        )

        if self.__by_group:
            (
                self.__mean_return_quantile_group,
                self.__mean_return_quantile_group_std_err,
            ) = perf.mean_return_by_quantile(
                factor_data,
                by_date=False,
                by_group=True,
                demeaned=long_short,
                group_adjust=group_neutral,
            )

            self.__mean_quant_rateret_group = self.__mean_return_quantile_group.apply(
                utils.rate_of_return,
                axis=0,
                base_period=self.__mean_return_quantile_group.columns[0],
            )

            self.__num_groups = len(
                self.__mean_quant_rateret_group.index.get_level_values(
                    "group").unique()
            )

    def information_analysis(self):
        """calculate information performance
        """
        self.__ic = perf.factor_information_coefficient(
            self.factor_data(), self.__group_neutral)

        if not self.__by_group:

            self.__mean_monthly_ic = perf.mean_information_coefficient(
                self.factor_data(),
                group_adjust=self.__group_neutral,
                by_group=False,
                by_time="M",
            )

        if self.__by_group:
            self.__mean_group_ic = perf.mean_information_coefficient(
                self.factor_data(), group_adjust=self.__group_neutral, by_group=True
            )

    def turnover_analysis(self):
        """calculate turnover performance
        """
        if self.__turnover_periods is None:
            input_periods = utils.get_forward_returns_columns(
                self.factor_data().columns, require_exact_day_multiple=True,).to_numpy()
            self.__turnover_periods = utils.timedelta_strings_to_integers(
                input_periods)
        else:
            self.__turnover_periods = utils.timedelta_strings_to_integers(
                self.__turnover_periods,)

        quantile_factor = self.factor_data()["factor_quantile"]

        self.__quantile_turnover = {
            p: pd.concat(
                [
                    perf.quantile_turnover(quantile_factor, q, p)
                    for q in quantile_factor.sort_values().unique().tolist()
                ],
                axis=1,
            )
            for p in self.__turnover_periods
        }

        self.__autocorrelation = pd.concat(
            [
                perf.factor_rank_autocorrelation(self.factor_data(), period)
                for period in self.__turnover_periods
            ],
            axis=1,
        )

    def event_analysis(self, avgretplot=(5, 15)):
        before, after = avgretplot

        self.__avg_cumulative_returns = perf.average_cumulative_return_by_quantile(
            self.factor_data(),
            self.prices(),
            periods_before=before,
            periods_after=after,
            demeaned=self.__long_short,
            group_adjust=self.__group_neutral,
        )

        if self.__by_group:

            self.__avg_cumret_by_group = perf.average_cumulative_return_by_quantile(
                self.factor_data(),
                self.__factor_returns,
                periods_before=before,
                periods_after=after,
                demeaned=self.__long_short,
                group_adjust=self.__group_neutral,
                by_group=True,
            )

    def plot_returns_table(self):
        plotting.plot_returns_table(
            self.__alpha_beta, self.__mean_quant_rateret, self.__mean_ret_spread_quant
        )

    def plot_turnover_table(self):
        plotting.plot_turnover_table(
            self.__autocorrelation, self.__quantile_turnover)

    def plot_information_table(self):
        plotting.plot_information_table(self.__ic)

    def plot_ic_ts(self):
        """
        Plots Spearman Rank Information Coefficient and IC moving
        average for a given factor.
        """
        columns_wide = 2
        fr_cols = len(self.__ic.columns)
        rows_when_wide = ((fr_cols - 1) // columns_wide) + 1
        vertical_sections = fr_cols + 3 * rows_when_wide + 2 * fr_cols
        gf = GridFigure(rows=vertical_sections, cols=columns_wide)

        ax_ic_ts = [gf.next_row() for _ in range(fr_cols)]
        plotting.plot_ic_ts(self.__ic, ax=ax_ic_ts)
        # gf.close()

    def plot_ic_hist(self):
        """
        Plots Spearman Rank Information Coefficient histogram for a given factor.
        """
        columns_wide = 1
        fr_cols = len(self.__ic.columns)
        rows_when_wide = ((fr_cols - 1) // columns_wide) + 1
        vertical_sections = fr_cols + 3 * rows_when_wide + 2 * fr_cols
        gf = GridFigure(rows=vertical_sections, cols=columns_wide)

        ax_ic_hqq = [gf.next_cell() for _ in range(fr_cols * 1)]
        plotting.plot_ic_hist(self.__ic, ax=ax_ic_hqq[::1])

        # # gf.close()

    def plot_ic_qq(self):
        """
        Plots Spearman Rank Information Coefficient "Q-Q" plot relative to
        a theoretical distribution.
        """
        columns_wide = 1
        fr_cols = len(self.__ic.columns)
        rows_when_wide = ((fr_cols - 1) // columns_wide) + 1
        vertical_sections = fr_cols + 3 * rows_when_wide + 2 * fr_cols
        gf = GridFigure(rows=vertical_sections, cols=columns_wide)

        ax_ic_hqq = [gf.next_cell() for _ in range(fr_cols * 1)]
        plotting.plot_ic_qq(self.__ic, ax=ax_ic_hqq[::1])

    def plot_quantile_statistics_table(self):

        plotting.plot_quantile_statistics_table(self.factor_data())

    def plot_quantile_returns_bar(self):
        """
        Plots mean period wise returns for factor quantiles.
        """
        fr_cols = len(self.__factor_returns.columns)
        vertical_sections = 2 + fr_cols * 3
        gf = GridFigure(rows=vertical_sections, cols=1)
        plotting.plot_quantile_returns_bar(
            self.__mean_quant_rateret,
            by_group=False,
            ylim_percentiles=None,
            ax=gf.next_row(),
        )
        if self.__by_group:

            vertical_sections = 1 + (((self.__num_groups - 1) // 2) + 1)
            gf = GridFigure(rows=vertical_sections, cols=2)

            ax_quantile_returns_bar_by_group = [
                gf.next_cell() for _ in range(self.__num_groups)
            ]
            plotting.plot_quantile_returns_bar(
                self.__mean_quant_rateret_group,
                by_group=True,
                ylim_percentiles=(5, 95),
                ax=ax_quantile_returns_bar_by_group,
            )
            plt.show()
        # gf.close()

    def plot_quantile_returns_violin(self):
        """
        Plots a violin box plot of period wise returns for factor quantiles.
        """
        fr_cols = len(self.__factor_returns.columns)
        vertical_sections = 2 + fr_cols * 3
        gf = GridFigure(rows=vertical_sections, cols=1)
        plotting.plot_quantile_returns_violin(
            self.__mean_quant_rateret_bydate, ylim_percentiles=(1, 99), ax=gf.next_row()
        )
        # gf.close()

    def plot_cumulative_returns(self):
        """Plots the cumulative returns of the returns series passed in.

        """
        fr_cols = len(self.__factor_returns.columns)
        vertical_sections = 2 + fr_cols * 3
        gf = GridFigure(rows=vertical_sections, cols=1)

        for period in self.__factor_returns:
            title = (
                "Factor Weighted "
                + ("Group Neutral " if self.__group_neutral else "")
                + ("Long/Short " if self.__long_short else "")
                + "Portfolio Cumulative Return ({} Period)".format(period)
            )
            pattern = re.compile(r'(\d+)(.*)D')
            match_per_num = pattern.match(period)
            per_num = 1
            if match_per_num:
                per_num = int(match_per_num.groups()[0])
            else:
                raise "Wrong Peroid Type! Requires like: 1D 5D 10D"
            plotting.plot_cumulative_returns(
                self.__factor_returns[period], period=period, title=title, ax=gf.next_row(
                ), freq=str(per_num) + 'B'
            )
        # gf.close()

    def plot_mean_quantile_returns_spread_time_series(self):
        """
        Plots mean period wise returns for factor quantiles.

        """
        fr_cols = len(self.__factor_returns.columns)
        vertical_sections = 2 + fr_cols * 3
        gf = GridFigure(rows=vertical_sections, cols=1)
        ax_mean_quantile_returns_spread_ts = [
            gf.next_row() for x in range(fr_cols)
        ]
        plotting.plot_mean_quantile_returns_spread_time_series(
            self.__mean_ret_spread_quant,
            std_err=self.__std_spread_quant,
            bandwidth=0.5,
            ax=ax_mean_quantile_returns_spread_ts,
        )
        # gf.close()

    def plot_ic_by_group(self):
        """
        Plots Spearman Rank Information Coefficient for a given factor over
        provided forward returns. Separates by group.
        """
        columns_wide = 2
        fr_cols = len(self.__ic.columns)
        rows_when_wide = ((fr_cols - 1) // columns_wide) + 1
        vertical_sections = fr_cols + 3 * rows_when_wide + 2 * fr_cols
        gf = GridFigure(rows=vertical_sections, cols=columns_wide)
        plotting.plot_ic_by_group(self.__mean_group_ic, ax=gf.next_row())
        # gf.close()

    def plot_factor_rank_auto_correlation(self):
        """
        Plots factor rank autocorrelation over time.
        See factor_rank_autocorrelation for more details.
        """
        fr_cols = len(self.__turnover_periods)
        columns_wide = 1
        rows_when_wide = ((fr_cols - 1) // 1) + 1
        vertical_sections = fr_cols + 3 * rows_when_wide + 2 * fr_cols
        gf = GridFigure(rows=vertical_sections, cols=columns_wide)
        for period in self.__autocorrelation:
            if self.__autocorrelation[period].isnull().all():
                continue
            plotting.plot_factor_rank_auto_correlation(
                self.__autocorrelation[period], period=period, ax=gf.next_row()
            )
        # gf.close()

    def plot_top_bottom_quantile_turnover(self):
        """
        Plots period wise top and bottom quantile factor turnover.
        """
        fr_cols = len(self.__turnover_periods)
        columns_wide = 1
        rows_when_wide = ((fr_cols - 1) // 1) + 1
        vertical_sections = fr_cols + 3 * rows_when_wide + 2 * fr_cols
        gf = GridFigure(rows=vertical_sections, cols=columns_wide)
        for period in self.__turnover_periods:
            if self.__quantile_turnover[period].isnull().all().all():
                continue
            plotting.plot_top_bottom_quantile_turnover(
                self.__quantile_turnover[period], period=period, ax=gf.next_row(
                )
            )
        # gf.close()

    def plot_monthly_ic_heatmap(self):
        """
        Plots a heatmap of the information coefficient or returns by month.
        """
        columns_wide = 2
        fr_cols = len(self.__ic.columns)
        rows_when_wide = ((fr_cols - 1) // columns_wide) + 1
        vertical_sections = fr_cols + 3 * rows_when_wide + 2 * fr_cols
        gf = GridFigure(rows=vertical_sections, cols=columns_wide)
        ax_monthly_ic_heatmap = [gf.next_cell() for x in range(fr_cols)]
        plotting.plot_monthly_ic_heatmap(
            self.__mean_monthly_ic, ax=ax_monthly_ic_heatmap)
        # gf.close()

    def plot_cumulative_returns_by_quantile(self):
        """
        Plots the cumulative returns of various factor quantiles.
        """
        fr_cols = len(self.__factor_returns.columns)
        vertical_sections = 2 + fr_cols * 3
        gf = GridFigure(rows=vertical_sections, cols=1)
        for period in self.__factor_returns:
            title = (
                "Factor Weighted "
                + ("Group Neutral " if self.__group_neutral else "")
                + ("Long/Short " if self.__long_short else "")
                + "Portfolio Cumulative Return ({} Period)".format(period)
            )
            pattern = re.compile(r'(\d+)(.*)D')
            match_per_num = pattern.match(period)
            per_num = 1
            if match_per_num:
                per_num = int(match_per_num.groups()[0])
            else:
                raise "Wrong Peroid Type! Requires like: 1D 5D 10D"
            plotting.plot_cumulative_returns_by_quantile(
                self.__mean_quant_ret_bydate[period], period=period, ax=gf.next_row(), freq=str(per_num) + 'B')
        # gf.close()

    def plot_quantile_average_cumulative_return(self, std_bar=True):
        """
        Plots sector-wise mean daily returns for factor quantiles
        across provided forward price movement columns.
        """
        num_quantiles = int(self.factor_data()["factor_quantile"].max())
        vertical_sections = 1
        if std_bar:
            vertical_sections += ((num_quantiles - 1) // 2) + 1
        cols = 2 if num_quantiles != 1 else 1
        gf = GridFigure(rows=vertical_sections, cols=cols)
        plotting.plot_quantile_average_cumulative_return(
            self.__avg_cumulative_returns,
            by_quantile=False,
            std_bar=False,
            ax=gf.next_row(),
        )
        if std_bar:
            ax_avg_cumulative_returns_by_q = [
                gf.next_cell() for _ in range(num_quantiles)
            ]
            plotting.plot_quantile_average_cumulative_return(
                self.__avg_cumulative_returns,
                by_quantile=True,
                std_bar=True,
                ax=ax_avg_cumulative_returns_by_q,
            )

        if self.__by_group:
            groups = self.factor_data()["group"].unique()
            num_groups = len(groups)
            vertical_sections = ((num_groups - 1) // 2) + 1
            gf = GridFigure(rows=vertical_sections, cols=2)
            for group, avg_cumret in self.__avg_cumret_by_group.groupby(level="group"):
                avg_cumret.index = avg_cumret.index.droplevel("group")
                plotting.plot_quantile_average_cumulative_return(
                    avg_cumret,
                    by_quantile=False,
                    std_bar=False,
                    title=group,
                    ax=gf.next_cell(),
                )
        # gf.close()

    def plot_events_distribution(self, num_bars=50, ax=None):
        """
        Plots the distribution of events in time.
        """
        gf = GridFigure(rows=1, cols=1)
        plotting.plot_events_distribution(
            events=self.factor_data()["factor"], num_bars=num_bars, ax=gf.next_row())
        plt.show()
        # gf.close()
