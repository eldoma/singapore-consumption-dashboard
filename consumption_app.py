import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# --- Streamlit Setup ---
st.set_page_config(layout="wide")
st.title("🇸🇬 Singapore Domestic Consumption by Commodity Division")


st.markdown("""App Copyright by : e-networksystems, May 2025
### 📦 What’s This?
A Data Science project: Making Guesstimates
            
This dashboard estimates **internal consumption** in Singapore using the formula:

> **Consumption = Imports − Re-Exports**

🧮 Data Source:
- `MerchandiseImportsByCommodityDivisionMonthly.csv`
- `ReExportsByCommodityDivisionMonthly.csv`

Merchandise Imports By Commodity Division, Monthly
Data from Jan 1976 to Mar 2025

Source: SINGSTAT (Singapore Department of Statistics)
            
Footnotes: Prior to 2003, merchandise trade data exclude Singapore's merchandise trade with Indonesia. Data prior to 1999 are based on Standard International Trade Classification (SITC) 3. Data from 1999 onwards are based on SITC 4.1 and consistent with the ASEAN Harmonised Tariff Nomenclature (AHTN) 2022 version.

https://data.gov.sg/datasets/d_b89e35ce38cb93a17f5c016e71f50690/view


Re-Exports By Commodity Division, Monthly
Data from Jan 1976 to Mar 2025

SINGSTAT (Singapore Department of Statistics)
Source: ENTERPRISE SINGAPORE

Footnotes: Prior to 2003, merchandise trade data exclude Singapore's merchandise trade with Indonesia. Data prior to 1999 are based on Standard International Trade Classification (SITC) 3. Data from 1999 onwards are based on SITC 4.1 and consistent with the ASEAN Harmonised Tariff Nomenclature (AHTN) 2022 version.            
https://data.gov.sg/datasets/d_d57aee293789d31a8cb4097ad50e78cb/view
            
📁 Official data from [data.gov.sg](https://data.gov.sg). Update Frequency: Monthly
---
### 📈 Sample Key takeaways and notable trends: Singaporeans 
## Consume more Edible Oil, Tea, Cocoa, Spices
            
Edible oils (Fixed Vegetable Fats & Oils) show volatile trends with large spikes and drops, but since 2010 the average monthly consumption appears to have stabilized at higher levels than pre-2000, indicating moderate to increased usage over time.

Coffee, Tea, Cocoa, Spices & Manufactures show a clear upward trend, especially after 2010, with a strong spike in recent years — strongly suggesting growing consumption habits among Singaporeans for these products.

## Singaporeans (both individuals and industries) are rapidly phasing out paper

Aligning with digital and environmental trends.          

## Will be consuming less on Beverages

The chart suggests potential stagnation or even decline in Singapore’s domestic beverage consumption, especially in recent years.
            
Key signs:
⚠️ Heavy fluctuations and sharp negative values (post-2010), possibly indicating:
Inventory re-exports exceeding imports (e.g., re-exporting stock)
Seasonal dumping, corrections, or trade anomalies
📉 Lack of clear growth trend post-2015—consumption appears more volatile and flat, if not declining
📊 Compared to pre-2010: earlier decades showed steadier or moderate growth
Possible factors:
Market saturation
Shift to healthier or alternative drinks
Export-driven beverage trade (less local use)
So yes, unless corrected, this data may imply lower domestic beverage demand, or at least more erratic patterns going forward.
            
## Stable Clothing consumption
            
The Singaporean net domestic consumption is modest and stable, but masked by high re-export flows and global supply chain roles.
            
## Consuming a bit more Fish & Seafood
            
The chart strongly suggests that Singaporeans have been consuming more fish and seafood over time.
            
Key observations:
            
📈 Long-term upward trend in domestic consumption from the 1980s through 2020s.
            
📊 Especially sharp growth after the early 2000s, possibly due to population growth, dietary shifts, or improved trade access.
            
⚠️ The spikes and volatility in recent years could reflect seasonal demand, stockpiling, or supply chain shifts (e.g., during COVID).
            
So yes, the data supports that internal demand for fish and seafood has increased significantly.
""")

# --- Upload Section ---
import_file = st.file_uploader("📁 Upload Imports CSV", type=["csv"], key="imp")
export_file = st.file_uploader("📁 Upload Re-Exports CSV", type=["csv"], key="exp")

if import_file and export_file:
    # Load datasets
    df_imp = pd.read_csv(import_file).dropna(subset=["DataSeries"])
    df_exp = pd.read_csv(export_file).dropna(subset=["DataSeries"])

    # Clean DataSeries
    df_imp["DataSeries"] = df_imp["DataSeries"].str.strip()
    df_exp["DataSeries"] = df_exp["DataSeries"].str.strip()

    # Get common divisions
    common_divisions = sorted(set(df_imp["DataSeries"]).intersection(set(df_exp["DataSeries"])))

    if common_divisions:
        selected = st.selectbox("📦 Select a Commodity Division", common_divisions)

        # Filter & reshape
        imp = df_imp[df_imp["DataSeries"] == selected].melt(id_vars="DataSeries", var_name="Month", value_name="Imports")
        exp = df_exp[df_exp["DataSeries"] == selected].melt(id_vars="DataSeries", var_name="Month", value_name="ReExports")

        # Parse months
        imp["Month"] = pd.to_datetime(imp["Month"] + "01", format="%Y%b%d", errors="coerce")
        exp["Month"] = pd.to_datetime(exp["Month"] + "01", format="%Y%b%d", errors="coerce")

        # Merge & calculate
        merged = pd.merge(imp[["Month", "Imports"]], exp[["Month", "ReExports"]], on="Month", how="inner")
        merged["Imports"] = pd.to_numeric(merged["Imports"], errors="coerce")
        merged["ReExports"] = pd.to_numeric(merged["ReExports"], errors="coerce")
        merged["Consumption"] = merged["Imports"] - merged["ReExports"]
        merged = merged.dropna().sort_values("Month")

        # --- Plot ---
        st.subheader(f"📈 Estimated Monthly Consumption: {selected}")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(merged["Month"], merged["Consumption"], marker="o", color="purple")
        ax.set_xlabel("Month")
        ax.set_ylabel("Consumption (thousands SGD)")
        ax.set_title(f"Singapore Domestic Consumption — {selected}")
        ax.grid(True)
        fig.tight_layout()
        st.pyplot(fig)

        # --- Table ---
        with st.expander("📋 View Raw Data Table"):
            st.dataframe(merged[["Month", "Imports", "ReExports", "Consumption"]])
    else:
        st.warning("⚠️ No common commodity divisions found between the two files.")
else:
    st.info("Please upload both CSV files to begin.")
