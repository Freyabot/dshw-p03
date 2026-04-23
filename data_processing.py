import pandas as pd
import os


def create_processed_dir():
    """创建处理后数据的目录"""
    processed_dir = 'data/processed'
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    print(f"Created directory: {processed_dir}")


def process_ownership():
    """处理ownership.csv，根据民营/外资和国营进行赋值"""
    file_path = 'data/raw/ownership.csv'
    df = pd.read_csv(file_path)

    # 处理股权性质赋值：
    # 1: 国企
    # 0: 民营或外资
    df['soe_flag'] = df['EquityNature'].apply(lambda x: 1 if x == '国企' else 0)

    # 确保只保留年末数据 (12月31日)
    df['EndDate'] = pd.to_datetime(df['EndDate'])
    df = df[df['EndDate'].dt.month == 12]
    df = df[df['EndDate'].dt.day == 31]

    # 保存处理后的文件
    output_path = 'data/processed/ownership_processed.csv'
    df.to_csv(output_path, index=False)
    print(f"Processed ownership data saved to: {output_path}")
    return df


def create_st_flag():
    """创建st_flag.csv，根据股票名称是否有ST前缀赋值"""
    # 从所有包含股票名称的文件中收集股票信息
    file_paths = [
        'data/raw/ownership.csv',
        'data/raw/balance_sheet.csv',
        'data/raw/income_stmt.csv',
        'data/raw/cashflow.csv',
        'data/raw/industry.csv'
    ]

    all_stock_info = []

    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path)

            # 统一列名
            if 'Symbol' in df.columns:
                symbol_col = 'Symbol'
            elif 'Stkcd' in df.columns:
                symbol_col = 'Stkcd'
            else:
                symbol_col = None

            if 'ShortName' in df.columns:
                name_col = 'ShortName'
            else:
                name_col = None

            if 'EndDate' in df.columns:
                date_col = 'EndDate'
            elif 'Accper' in df.columns:
                date_col = 'Accper'
            else:
                date_col = None

            if symbol_col and name_col and date_col:
                # 只保留所需列
                temp_df = df[[symbol_col, name_col, date_col]].copy()
                temp_df.rename(columns={
                    symbol_col: 'Symbol',
                    name_col: 'ShortName',
                    date_col: 'EndDate'
                }, inplace=True)
                all_stock_info.append(temp_df)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

    # 合并所有数据
    if all_stock_info:
        merged_df = pd.concat(all_stock_info, ignore_index=True)

        # 去重
        merged_df.drop_duplicates(inplace=True)

        # 统一日期格式
        merged_df['EndDate'] = pd.to_datetime(merged_df['EndDate'], errors='coerce')

        # 只保留年末数据 (12月31日)
        merged_df = merged_df.dropna(subset=['EndDate'])
        merged_df = merged_df[merged_df['EndDate'].dt.month == 12]
        merged_df = merged_df[merged_df['EndDate'].dt.day == 31]

        # 创建ST标志：1表示有ST前缀，0表示无
        merged_df['st_flag'] = merged_df['ShortName'].astype(str).apply(
            lambda x: 1 if ('ST' in x) or ('*ST' in x) or ('SST' in x) or ('S*ST' in x) else 0
        )

        # 只保留需要的列
        result_df = merged_df[['Symbol', 'ShortName', 'EndDate', 'st_flag']]

        # 保存文件
        output_path = 'data/processed/st_flag.csv'
        result_df.to_csv(output_path, index=False)
        print(f"ST flag data saved to: {output_path}")
        return result_df
    else:
        print("No stock data found in the CSV files")
        return None


def process_annual_data():
    """确保所有数据文件以年度频率为准，使用年末值"""
    files_to_process = [
        ('balance_sheet.csv', 'Accper'),
        ('income_stmt.csv', 'Accper'),
        ('cashflow.csv', 'Accper'),
        ('industry.csv', 'EndDate')
    ]

    for filename, date_col in files_to_process:
        file_path = f'data/raw/{filename}'
        try:
            df = pd.read_csv(file_path)

            # 统一日期格式
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

            # 只保留年末数据 (12月31日)
            df = df.dropna(subset=[date_col])
            df = df[df[date_col].dt.month == 12]
            df = df[df[date_col].dt.day == 31]

            # 保存处理后的文件
            output_path = f'data/processed/{filename.replace(".csv", "_processed.csv")}'
            df.to_csv(output_path, index=False)
            print(f"Processed annual data saved to: {output_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue


def process_m2():
    """处理m2.csv，使用Q4（12月）数据计算年增长率"""
    file_path = 'data/raw/m2.csv'
    try:
        # 读取CSV文件，不预先指定列名，先查看原始数据
        df = pd.read_csv(file_path, header=None)

        # 跳过第一行（表头），并设置列名
        df = df.iloc[1:].copy()
        df.columns = ['date', 'm2_growth']

        # 清理数据 - 确保是字符串类型后再移除引号
        df['date'] = df['date'].astype(str).str.replace('"', '').str.strip()
        df['m2_growth'] = df['m2_growth'].astype(str).str.replace('"', '').str.strip()

        # 转换为数值类型
        df['m2_growth'] = pd.to_numeric(df['m2_growth'], errors='coerce')

        # 转换日期格式
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m', errors='coerce')

        # 只保留Q4（12月）数据
        df = df.dropna(subset=['date', 'm2_growth'])
        df_q4 = df[df['date'].dt.month == 12].copy()

        # 添加年份列
        df_q4['year'] = df_q4['date'].dt.year

        # 排序
        df_q4 = df_q4.sort_values('year')

        # 重新组织列
        df_q4 = df_q4[['year', 'date', 'm2_growth']]

        # 保存处理后的文件
        output_path = 'data/processed/m2_processed.csv'
        df_q4.to_csv(output_path, index=False)
        print(f"Processed M2 data saved to: {output_path}")

        # 显示统计信息
        print(f"M2 data summary:")
        print(f"Total Q4 records: {len(df_q4)}")
        if len(df_q4) > 0:
            print(f"Year range: {df_q4['year'].min()} - {df_q4['year'].max()}")

        return df_q4
    except Exception as e:
        print(f"Error processing m2.csv: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    print("Starting data processing...")

    # 创建处理后数据目录
    create_processed_dir()

    # 处理所有权数据
    ownership_df = process_ownership()

    # 创建ST标志数据
    st_flag_df = create_st_flag()

    # 处理年度数据
    process_annual_data()

    # 处理M2数据
    m2_df = process_m2()

    # 显示处理结果摘要
    if ownership_df is not None:
        print(f"\nOwnership data summary:")
        print(f"Total records: {len(ownership_df)}")
        print(f"SOE count: {ownership_df['soe_flag'].sum()}")
        print(f"Non-SOE count: {len(ownership_df) - ownership_df['soe_flag'].sum()}")

    if st_flag_df is not None:
        print(f"\nST flag summary:")
        print(f"Total records: {len(st_flag_df)}")
        print(f"ST count: {st_flag_df['st_flag'].sum()}")
        print(f"Non-ST count: {len(st_flag_df) - st_flag_df['st_flag'].sum()}")

    print("\nData processing completed!")


if __name__ == "__main__":
    main()