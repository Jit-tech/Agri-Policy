
import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("IREL_AG2050_Policy_Simulation_Smoothed.csv")

df = load_data()

# Sidebar Policy Toggles
st.sidebar.title("Policy Scenario Builder")
selected_county = st.sidebar.selectbox("Select County", df["County"].unique())
selected_year = st.sidebar.slider("Year", min_value=int(df["Year"].min()), max_value=int(df["Year"].max()), value=2025)

# Policy switches
agro_toggle = st.sidebar.checkbox("Boost Agroforestry Support", value=False)
solar_toggle = st.sidebar.checkbox("Increase Solar Incentive", value=False)
bio_toggle = st.sidebar.checkbox("Enhance Bioenergy Program", value=False)

# Filter data
data_filtered = df[(df["County"] == selected_county) & (df["Year"] == selected_year)].copy()

# Apply toggles
yield_boost = data_filtered["CRISPR_YieldBoost"].values[0]
solar_pct = data_filtered["SolarAdoption"].values[0]
biomass = data_filtered["BiomassOutput"].values[0]
carbon_offset = data_filtered["CarbonCreditsEarned"].values[0]

if agro_toggle:
    yield_boost *= 1.1
if solar_toggle:
    solar_pct *= 1.15
if bio_toggle:
    biomass *= 1.2
    carbon_offset *= 1.05

# Display adjusted KPIs
st.title("Ireland 2026: Agri-Policy Simulator")
st.subheader(f"{selected_county} — Year: {selected_year}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("CRISPR Yield Boost (kg/ha)", f"{yield_boost:.1f}")
col2.metric("Solar Adoption (%)", f"{solar_pct:.1f}")
col3.metric("Biomass Output (GWh)", f"{biomass:.2f}")
col4.metric("Carbon Credits (mtCO₂)", f"{carbon_offset:.2f}")

# Dynamic AI Persona Logic
def generate_persona_response(persona, county, year, df):
    row = df[(df["County"] == county) & (df["Year"] == year)]
    if row.empty:
        return "No data available for this county and year."

    yield_val = row["CRISPR_YieldBoost"].values[0]
    solar_val = row["SolarAdoption"].values[0]
    bio_val = row["BiomassOutput"].values[0]
    carbon_val = row["CarbonCreditsEarned"].values[0]

    if persona == "ÉIREA":
        return (
            f"ÉIREA: In {year}, {county} achieved a CRISPR-driven yield boost of {yield_val:.1f} kg/ha. "
            f"This provides a solid base for transitioning to more resilient agroforestry systems. "
            f"Agroforestry support programs should prioritize regions with >{yield_val:.1f} kg/ha to capitalize on biological synergies."
        )
    elif persona == "SOLARA":
        return (
            f"SOLARA: As of {year}, solar adoption in {county} reached {solar_val:.1f}%. "
            f"If current CAP solar incentives continue, we expect adoption to exceed {solar_val*1.15:.1f}% by {year + 1}. "
            f"Consider aligning grid feed-in tariffs accordingly."
        )
    elif persona == "GRAINA":
        return (
            f"GRAINA: With {yield_val:.0f} kg/ha in yields and {carbon_val:.2f} mtCO₂ in credits, "
            f"{county} is positioned to enhance traceability premiums by 8–12% over baseline. "
            f"Local cooperatives should focus on export certification training in Q{year%4 + 1}."
        )
    elif persona == "AI-SCEAL":
        risk_score = 100 - min(100, yield_val/6 + solar_val + bio_val*2)
        return (
            f"AI-SCEAL: Citizen confidence correlates with visible green returns. "
            f"In {year}, the combined bio-solar-carbon mix in {county} suggests a policy risk score of {risk_score:.1f}. "
            f"Targeted awareness campaigns should begin immediately."
        )
    else:
        return "No persona selected."

# AI Persona Interface
st.markdown("---")
st.header("Ask the Agentic AI")
persona = st.selectbox("Choose AI Persona", ["ÉIREA", "SOLARA", "GRAINA", "AI-SCEAL"])
question = st.text_input("Ask your policy agent:")

if question:
    response = generate_persona_response(persona, selected_county, selected_year, df)
    st.success(response)

# Economic Impact Simulator
st.markdown("---")
st.header("Economic Impact Simulation")

# Prices/Values
grain_price_per_kg = 0.22  # €/kg
price_per_tonne = 85       # €/mtCO2 (EU ETS)
solar_savings = solar_pct * 120
bio_revenue = biomass * 45
carbon_revenue = carbon_offset * price_per_tonne
yield_revenue = yield_boost * grain_price_per_kg

total_impact = yield_revenue + solar_savings + bio_revenue + carbon_revenue

# Revenue breakdown
st.metric("Estimated Economic Impact (€)", f"{total_impact:,.0f}")
st.caption("Includes revenue from CRISPR yield, solar savings, bioenergy, and carbon credits.")

st.markdown("**Breakdown:**")
st.write({
    "CRISPR Yield Revenue (€)": round(yield_revenue, 2),
    "Solar Savings (€)": round(solar_savings, 2),
    "Biomass Revenue (€)": round(bio_revenue, 2),
    "Carbon Credits (€)": round(carbon_revenue, 2),
})

# Historical Yield Trend
st.markdown("---")
st.header("Yield Trend Over Time")
hist = df[df["County"] == selected_county]
fig = px.line(hist, x="Year", y="CRISPR_YieldBoost", title="Yield Trend Over Time")
st.plotly_chart(fig, use_container_width=True)


# Visual Insights
st.markdown("---")
st.header("Visual Insights & Multi-Metric Trends")

# Multivariate 3D Scatter Plot
st.subheader("Policy-Energy-Yield Interaction")
fig_3d = px.scatter_3d(
    df[df.County == selected_county],
    x="Year", y="SolarAdoption", z="CRISPR_YieldBoost",
    size="CarbonCreditsEarned", color="BiomassOutput",
    title=f"3D Simulation Map: {selected_county}"
)
st.plotly_chart(fig_3d, use_container_width=True)

# Line charts for all key metrics
st.subheader("Year-over-Year Performance")
metrics = ["CRISPR_YieldBoost", "SolarAdoption", "BiomassOutput", "CarbonCreditsEarned"]
for metric in metrics:
    fig_line = px.line(
        df[df.County == selected_county],
        x="Year", y=metric,
        title=f"{metric.replace('_', ' ')} over Time"
    )
    st.plotly_chart(fig_line, use_container_width=True)

# Economic Revenue Pie Chart
st.subheader("Revenue Breakdown by Stream")
import plotly.graph_objects as go
fig_pie = go.Figure(data=[go.Pie(
    labels=["CRISPR Yield", "Solar", "Biomass", "Carbon"],
    values=[yield_revenue, solar_savings, bio_revenue, carbon_revenue],
    hole=0.4
)])
fig_pie.update_layout(title="Economic Impact Composition (€)")
st.plotly_chart(fig_pie)


# Footer: Data Sources and Attribution
st.markdown("---")
st.markdown("Data Sources")
st.markdown("""
- CRISPR Yield Data: Derived from Phenotypic Dataset, Wheat Gene Expression Project  
- Solar Adoption: Calibrated using SEAI Solar PV Statistics  
- Biomass Output: Synthesized from IrBEA Solid Biomass Capacity Report (2023)  
- Carbon Credits: Proxy from EU-ETS and Irish CAP 2023–2027 simulations  
- Agroforestry Policy Context: Based on Teagasc Silvopasture Pilot (Wexford, 2005)  
""")

st.markdown("Designed by Jit")
st.caption("Powered by Econometrics and AI")
