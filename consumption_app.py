import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# --- Streamlit Setup ---
st.set_page_config(layout="wide")
st.title("🇸🇬 Singapore Domestic Consumption by Commodity Division")

st.markdown("""
### 📦 What’s This?

This dashboard estimates **internal consumption** in Singapore using:

> **Consumption = Imports − Re-Exports**

🧮 Data Source:
- `MerchandiseImportsByCommodityDivisionMonthly.csv`
- `ReExportsByCommodityDivisionMonthly.csv`

📁 Official data from [data.gov.sg](https://data.gov.sg)
---
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
