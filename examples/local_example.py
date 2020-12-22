# %%
# 导入相关库
try:
    import traceback
    from factest.data_service.local_data import LocalData
    from factest.factor_test import FactorTest
except ImportError as e:
    print('导入库失败!')
    traceback.print_exc()

# %%

# 因子计算公式
FAC_FROM = '(-1*CORR(RANK(DELTA(LOG(VOLUME), 1)),RANK(((CLOSE - OPEN) / OPEN)), 6))'

# 本地数据的地址
DATA_BASE_DIR = 'data/daily_price.h5'
# 因子值输出地址
FAC_OUT_DIR = 'out/factors.csv'

# 因子测试的时间区间
BEGIN_DATE = '2017-01-01'
END_DATE = '2019-01-01'

# 股票池 可以设置为全部'all', 也可以自己指定股票池
STOCKS = 'all'
# STOCKS = ['000001', '603336', '603991', '603997', '000005']

# 调仓周期
PEROIDS = (1, 5, 10)

# 分层数
QUANTILE_NUM = 5

# 结算价格 收盘价'close' 开盘价'open' 均价'vwap'
DEAL_METHOD = 'close'


# %%

# 导入本地数据源
data_source = LocalData(data_dir=DATA_BASE_DIR)
# 创立Factest对象
factest = FactorTest(data_source)

factest.set_group_neutral(False)  # 是否行业中性化
factest.set_long_short(False)  # 是否多空
factest.set_by_group(False)  # 是否分组(如行业分组) 目前最好不要
factest.set_weight_method('equal')  # 因子加权方式 目前只支持等权

factest.set_date_range(BEGIN_DATE, END_DATE)  # 回测的区间
factest.set_universe(STOCKS)  # 自定义股票池
factest.set_deal_method(DEAL_METHOD)  # 交易的价格
factest.set_period(PEROIDS)  # 调仓周期
factest.set_quantile(QUANTILE_NUM)  # 分位数
factest.set_formula(FAC_FROM)  # 因子计算公式

# %%

# 计算因子值
factors = factest.factors()
factors.to_csv(FAC_OUT_DIR)
factors.head(5)

# %%

# 交易价格
quote = data_source.QUOTE
quote.head(5)

# %%

# 因子分析 一定要在画图之前运行
factest.return_analysis()  # 收益分析
factest.information_analysis()  # ic分析
factest.turnover_analysis()  # 换手分析

# %%

# 因子收益

factest.factor_returns().head(10)

# %%

# 收益分析表
factest.plot_returns_table()

# %%

# 因子加权(目前只支持等权)累积收益
factest.plot_cumulative_returns()

# %%

# 因子分层回测
factest.plot_cumulative_returns_by_quantile()

# %%

# 因子分层平均收益直方图
factest.plot_quantile_returns_bar()
# %%

# 因子分层收益小提琴图
factest.plot_quantile_returns_violin()

# %%

# 收益差(最高层 - 最低层)
factest.plot_mean_quantile_returns_spread_time_series()

# %%

# ic分析表
factest.plot_information_table()

# %%

# 时序IC
factest.plot_ic_ts()

# %%

# IC 直方图
factest.plot_ic_hist()

# %%

# IC Q-Q 图
factest.plot_ic_qq()
# %%

# 月度IC热力图
factest.plot_monthly_ic_heatmap()

# %%

# 因子换手率表
factest.plot_turnover_table()

# %%

# 最高层换手率-最低层换手率
factest.plot_top_bottom_quantile_turnover()

# %%

# 因子排序的自相关
factest.plot_factor_rank_auto_correlation()

 
