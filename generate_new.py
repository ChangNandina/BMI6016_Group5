import pandas as pd
import numpy as np

# 读取数据
hesitancy = pd.read_csv('Vaccine_Hesitancy_for_COVID-19__County_and_local_estimates.csv')
deaths = pd.read_csv('time_series_covid19_deaths_US.csv')

# ========== 1. 处理死亡数据 ==========

# 日期列从第12列开始 (index 12)
date_columns = deaths.columns[12:]

# 保留需要的列
deaths_clean = deaths[['FIPS', 'Admin2', 'Province_State', 'Population'] + list(date_columns)].copy()

# 重命名列
deaths_clean = deaths_clean.rename(columns={
    'Admin2': 'County',
    'Province_State': 'State'
})

# ========== 2. 计算每周累积死亡率 ==========

# 日期列
date_cols = deaths_clean.columns[4:]

# 把日期转换成 datetime
dates = pd.to_datetime(date_cols, format='%m/%d/%y')

# 确保数值类型
for col in date_cols:
    deaths_clean[col] = pd.to_numeric(deaths_clean[col], errors='coerce')

# 按周分组 - 取每周最后一天的累积值
week_labels = dates.to_period('W')

# 创建每周累积死亡数
weekly_cumulative = pd.DataFrame()
for week in week_labels.unique():
    # 找到该周的所有日期列
    week_cols = [col for col, w in zip(date_cols, week_labels) if w == week]
    # 取该周最后一天的累积值
    weekly_cumulative[str(week)] = deaths_clean[week_cols[-1]]

# 计算每周累积死亡率 (每10万人)
population = deaths_clean['Population'].replace(0, np.nan)
weekly_cumulative_rate = weekly_cumulative.div(population, axis=0) * 100000

# 合并基础信息和每周累积死亡率
result = pd.concat([
    deaths_clean[['FIPS', 'County', 'State', 'Population']],
    weekly_cumulative_rate
], axis=1)

# ========== 3. 与疫苗犹豫数据合并 ==========

# 准备疫苗犹豫数据
hesitancy_clean = hesitancy[['FIPS Code', 'County Name', 'State', 'Estimated hesitant']].copy()
hesitancy_clean = hesitancy_clean.rename(columns={
    'FIPS Code': 'FIPS',
    'County Name': 'County',
    'Estimated hesitant': 'Hesitancy_Rate'
})

# 按 FIPS 合并
final_dataset = result.merge(
    hesitancy_clean[['FIPS', 'Hesitancy_Rate']],
    on='FIPS',
    how='inner'
)

# 调整列顺序
cols = ['FIPS', 'County', 'State', 'Population', 'Hesitancy_Rate'] + [col for col in final_dataset.columns if col not in ['FIPS', 'County', 'State', 'Population', 'Hesitancy_Rate']]
final_dataset = final_dataset[cols]

# ========== 4. 查看结果并保存 ==========

print("=== 累积死亡率数据集 ===")
print(f"形状: {final_dataset.shape}")
print(f"\n列名: {final_dataset.columns.tolist()[:10]}...")
print(f"\n前几行:")
print(final_dataset.head())

# 查看最后一周的统计
last_week = final_dataset.columns[-1]
print(f"\n最后一周 ({last_week}) 累积死亡率统计:")
print(final_dataset[last_week].describe())

# 保存
final_dataset.to_csv('combined_hesitancy_cumulative_death_rate.csv', index=False)
print("\n已保存为 combined_hesitancy_cumulative_death_rate.csv")