# %%

# 导入相关库
try:
    import sys
    import traceback
    sys.path.append('../../')
    from factest.data_service.jq_data import JQData
    from factest.data_service.local_data import LocalData
    from factest.utils import login_jqdata
    from factest.factor_test import FactorTest
except ImportError as e:
    print('导入库失败!')
    traceback.print_exc()

# %%

# 选择数据源

# 聚宽数据源 需要在test/config 文件夹中配置JQData的username和password
login_jqdata('./config/jqdata.json')
data_source = JQData()
# 本地数据源
 

# %%

# 创立Factest对象
factest = FactorTest(data_source)

# 设置因子测试的参数
factest.set_benchmark('沪深300')  # 设置基准
factest.set_by_group(False)  # 是否分组(如行业分组)
factest.set_deal_method('close')  # 交易的价格
factest.set_date_range('2016-01-01', '2019-01-01')  # 回测的区间
factest.set_group_neutral(False)  # 是否行业中性化
factest.set_long_short(False)  # 是否多空
factest.set_period((1, 5, 10))  # 调仓周期
factest.set_quantile(5)  # 分位数
factest.set_weight_method('equal')  # 因子加权方式 目前只支持等权
factest.set_universe('沪深300')  # 股票池
formula = "ABS(ADJCLOSE/ADJLOW + ADJHIGH/ADJOPEN - 2.03)"
factest.set_formula(formula)  # 因子计算公式


# %%
# 计算因子值
factors = factest.factors()
factors.to_csv('jq_f.csv')

# %%
# 交易价格
quote = data_source.QUOTE
quote.to_csv('local_quote.csv')
quote
# %%

# 因子分析 一定要在画图之前运行
factest.return_analysis()  # 收益分析
factest.information_analysis()  # ic分析
factest.turnover_analysis()  # 换手分析
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
# %%
 
