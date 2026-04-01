import pandas as pd
import numpy as np

# ========== 1. 读取现有数据和SDOH数据 ==========

# 读取已有的合并数据（可以用周死亡率或累积死亡率版本）
combined_df = pd.read_csv('combined_hesitancy_death_rate.csv')

# 读取SDOH数据
sdoh = pd.read_csv('SDOH_Measures_for_County_ACS_2017-2021.csv')

print("=== SDOH 数据概览 ===")
print(f"形状: {sdoh.shape}")
print(f"\n列名: {sdoh.columns.tolist()}")
print(f"\n唯一的 Short_Question_Text 类型:")
print(sdoh['Short_Question_Text'].unique())

# ========== 2. 处理SDOH数据 ==========

# 只保留需要的列
sdoh_clean = sdoh[['LocationID', 'LocationName', 'StateAbbr', 'Short_Question_Text', 'Data_Value']].copy()

# 重命名列
sdoh_clean = sdoh_clean.rename(columns={
    'LocationID': 'FIPS',
    'LocationName': 'County',
    'StateAbbr': 'State',
    'Short_Question_Text': 'SDOH_Measure',
    'Data_Value': 'Value'
})

# 将FIPS转为数值类型以便匹配
sdoh_clean['FIPS'] = pd.to_numeric(sdoh_clean['FIPS'], errors='coerce')

# ========== 3. 将SDOH数据从长格式转为宽格式 ==========

# 透视表：每个SDOH指标变成一列
sdoh_wide = sdoh_clean.pivot_table(
    index='FIPS',
    columns='SDOH_Measure',
    values='Value',
    aggfunc='first'
).reset_index()

# 给SDOH列添加前缀，便于识别
sdoh_wide.columns = ['FIPS'] + ['SDOH_' + col for col in sdoh_wide.columns[1:]]

print(f"\n=== SDOH 宽格式数据 ===")
print(f"形状: {sdoh_wide.shape}")
print(f"SDOH 指标数量: {len(sdoh_wide.columns) - 1}")
print(f"指标列表:")
for col in sdoh_wide.columns[1:]:
    print(f"  - {col}")

# ========== 4. 合并数据 ==========

# 确保FIPS类型一致
combined_df['FIPS'] = pd.to_numeric(combined_df['FIPS'], errors='coerce')

# 合并
final_dataset = combined_df.merge(
    sdoh_wide,
    on='FIPS',
    how='inner'
)

print(f"\n=== 最终合并数据集 ===")
print(f"原数据行数: {len(combined_df)}")
print(f"SDOH数据县数: {len(sdoh_wide)}")
print(f"合并后行数: {len(final_dataset)}")
print(f"总列数: {len(final_dataset.columns)}")

# ========== 5. 查看SDOH与Hesitancy的相关性 ==========

print(f"\n=== SDOH 与 Vaccine Hesitancy 相关性分析 ===")
sdoh_cols = [col for col in final_dataset.columns if col.startswith('SDOH_')]

correlations = {}
for col in sdoh_cols:
    corr = final_dataset['Hesitancy_Rate'].corr(final_dataset[col])
    correlations[col] = corr

# 按相关性排序
corr_sorted = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)

print("\nSDOH指标与疫苗犹豫率的相关性 (按绝对值排序):")
print("-" * 60)
for measure, corr in corr_sorted:
    if not np.isnan(corr):
        print(f"{measure.replace('SDOH_', ''):<40} {corr:>8.4f}")

# ========== 6. 保存文件 ==========

# 调整列顺序：基础信息 -> Hesitancy -> SDOH -> 周死亡率
info_cols = ['FIPS', 'County', 'State', 'Population', 'Hesitancy_Rate']
date_cols = [col for col in final_dataset.columns if '/' in col or col.startswith('20')]
date_cols = [col for col in date_cols if not col.startswith('SDOH')]

final_cols = info_cols + sdoh_cols + [col for col in final_dataset.columns if col not in info_cols + sdoh_cols]
final_dataset = final_dataset[final_cols]

print(f"\n前几行预览:")
print(final_dataset.head())

# 保存
final_dataset.to_csv('combined_hesitancy_sdoh_death_rate.csv', index=False)
print(f"\n已保存为 combined_hesitancy_sdoh_death_rate.csv")

# 同样处理累积死亡率版本
cumulative_df = pd.read_csv('combined_hesitancy_cumulative_death_rate.csv')
cumulative_df['FIPS'] = pd.to_numeric(cumulative_df['FIPS'], errors='coerce')

final_cumulative = cumulative_df.merge(
    sdoh_wide,
    on='FIPS',
    how='inner'
)

# 调整列顺序
final_cols_cum = info_cols + sdoh_cols + [col for col in final_cumulative.columns if col not in info_cols + sdoh_cols]
final_cumulative = final_cumulative[final_cols_cum]

final_cumulative.to_csv('combined_hesitancy_sdoh_cumulative_death_rate.csv', index=False)
print(f"已保存为 combined_hesitancy_sdoh_cumulative_death_rate.csv")