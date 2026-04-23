# Capital Structure Determinants of Chinese Listed Firms

> [Assignment brief](https://github.com/lianxhcn/dsfin/blob/main/homework/ex_P03_Panel-capital_strucuture.md)

## Personal Info
- Name: Freya
- Email: [1139588082@qq.com]

## Data Source
- CSMAR, download date: 2026-04-20
- Use output/sample_screening_table.csv and model outputs as the latest sample reference.

## Sample Screening Table
```
                    step obs_dropped  obs_left  firms_left
          Initial sample           -    266446        5684
Drop financial/insurance     10021.0    256425        5627
        Drop ST/PT firms     48713.0    207712        4911
            Drop Lev > 1        96.0    207616        4911
   Drop missing key vars     24630.0    182986        4705
            Final sample         0.0    182986        4705
```

## Tools
- Python 3.8+
- Jupyter Notebook
- Libraries: pandas, numpy, matplotlib, seaborn, pyfixest, scipy

## GitHub Repository
https://github.com/Freyabot/dshw-p03

## Quarto Book (optional)
https://Freyabot.github.io/dshw-p03/

## Main Findings
1. Main theoretical direction supported by M1-M3.
2. Ownership heterogeneity between SOE and Non-SOE.
3. Time-varying patterns from M4.
4. Size heterogeneity and threshold effect from M5-M6.

## File Structure
- 01_data_clean.ipynb: cleaning, variable construction, screening, winsorization
- 02_descriptive_statistics.ipynb: descriptive stats, correlation matrix, trend charts
- 03_model_estimation.ipynb: M1-M6 estimation and figures
- 04_results_summary.ipynb: summary tables, discussion, README generation
- output/
  - figures/
  - sample_screening_table.csv
  - descriptive_statistics.xlsx
  - correlation_matrix.xlsx
  - regression_summary.xlsx / regression_summary.csv
  - model_*.txt
