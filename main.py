import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import math
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

# Import required modules
from md_shaving_solution import show as show_md_shaving_solution

st.set_page_config(page_title="MD Shaving Analysis", layout="wide")

# Load custom CSS if available
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Sidebar Configuration
st.sidebar.title("🔧 Configuration")
st.sidebar.markdown("---")

# AFA Rate Configuration (Global setting)
st.sidebar.markdown("### AFA Rate Setting")
st.sidebar.caption("Alternative Fuel Agent rate for RP4 calculations")

if 'global_afa_rate' not in st.session_state:
    st.session_state.global_afa_rate = 0.0

global_afa_rate_cent = st.sidebar.number_input(
    "AFA Rate (cent/kWh)", 
    min_value=-10.0, 
    max_value=10.0, 
    value=st.session_state.global_afa_rate, 
    step=0.1,
    help="Current AFA rate in cents per kWh. Used for RP4 tariff calculations."
)

# Update session state
st.session_state.global_afa_rate = global_afa_rate_cent
global_afa_rate = global_afa_rate_cent / 100

st.sidebar.markdown("---")
st.sidebar.info(f"**Current AFA Rate:** {global_afa_rate_cent:+.1f} cent/kWh")
if global_afa_rate_cent >= 0:
    st.sidebar.success("✅ AFA adds to electricity cost")
else:
    st.sidebar.warning("⚠️ AFA reduces electricity cost")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 About")
st.sidebar.markdown("""
**MD Shaving Analysis Tool**

This tool provides:
- Maximum Demand (MD) shaving analysis
- Advanced battery sizing with real degradation data
- Financial analysis and ROI calculations
- Export capabilities

**Features:**
- Real WEIHENG TIANWU degradation curves
- RP4 tariff integration
- 20-year lifecycle modeling
""")

# Helper function to read different file formats
def read_uploaded_file(file):
    """Read uploaded file based on its extension"""
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format")

# Main app tabs
st.title("⚡ Maximum Demand Shaving Analysis")
st.markdown("**Comprehensive MD shaving analysis with battery energy storage solutions**")

tabs = st.tabs(["🔧 MD Shaving Solution", "🔋 Advanced MD Shaving"])

with tabs[0]:
    show_md_shaving_solution()

with tabs[1]:
    # 🔋 Advanced MD Shaving Tab (Copy the entire content from your original file)
    # [Insert the complete Tab 6 content from lines 795+ of your original streamlit_app.py]
    # This is the same content as in your original file for Tab 6
    
    st.title("🔋 Advanced MD Shaving")
    st.markdown("""
    **Advanced Maximum Demand (MD) shaving analysis with real battery degradation modeling.**
    
    This tool integrates actual WEIHENG TIANWU series degradation data to provide:
    - **Real degradation curves** (not linear approximations)
    - **20-year battery lifecycle analysis** with non-linear patterns
    - **MD target vs capacity modeling** over extended timeframes
    - **Investment planning** with accurate performance projections
    """)
    
    # Add information box about real degradation data
    with st.expander("🔬 About WEIHENG TIANWU Real Degradation Data", expanded=False):
        st.markdown("""
        **This analysis uses actual WEIHENG TIANWU series test data:**
        
        ✅ **Real Performance Data:**
        - 21 data points over 20-year period (Year 0-20)
        - State of Health (SOH) measurements from laboratory testing
        - Non-linear degradation pattern with initial steep drop then gradual decline
        - End-of-life defined at 80% SOH (typically achieved around year 15)
        
        📊 **Key Degradation Characteristics:**
        - **Year 0:** 100.00% SOH (new battery)
        - **Year 1:** 93.78% SOH (6.22% initial loss - typical for Li-ion)
        - **Years 1-15:** Gradual linear decline (~0.93% per year)
        - **Year 15:** 79.95% SOH (warranty end-of-life)
        - **Year 20:** 60.48% SOH (calendar life end)
        
        🎯 **Advantages over Linear Models:**
        - More accurate capacity predictions
        - Better financial planning capabilities  
        - Realistic performance expectations
        - Validated against real test data
        
        ⚠️ **Important Notes:**
        - Data represents laboratory conditions
        - Real-world performance may vary with operating conditions
        - Temperature, charge/discharge patterns affect actual degradation
        - Regular monitoring recommended for validation
        """)
    
    st.markdown("---")
    
    # Load battery database from JSON file with fallback to hardcoded data
    def load_battery_database():
        """Load battery database from JSON file with fallback to hardcoded data"""
        try:
            with open('vendor_battery_database.json', 'r') as f:
                battery_db = json.load(f)
                st.success("✅ Battery database loaded from vendor_battery_database.json")
                return battery_db
        except FileNotFoundError:
            st.warning("⚠️ vendor_battery_database.json not found. Using hardcoded battery database.")
            # Fallback to hardcoded database
            return {
                "TIANWU-50-233-0.25C": {
                    "company": "WEIHENG",
                    "model": "WH-TIANWU-50-233B",
                    "c_rate": 0.25,
                    "power_kW": 50,
                    "energy_kWh": 233,
                    "voltage_V": 832,
                    "lifespan_years": 15,
                    "eol_capacity_pct": 80,
                    "cycles_per_day": 1.0,
                    "cooling": "Liquid (Battery), Air (PCS)",
                    "weight_kg": 2700,
                    "dimensions_mm": [1400, 1350, 2100]
                },
                "TIANWU-100-233-0.5C": {
                    "company": "WEIHENG",
                    "model": "WH-TIANWU-100-233B",
                    "c_rate": 0.5,
                    "power_kW": 100,
                    "energy_kWh": 233,
                    "voltage_V": 832,
                    "lifespan_years": 15,
                    "eol_capacity_pct": 80,
                    "cycles_per_day": 1.0,
                    "cooling": "Liquid (Battery + PCS)",
                    "weight_kg": 2700,
                    "dimensions_mm": [1400, 1350, 2100]
                },
                "TIANWU-250-233-1C": {
                    "company": "WEIHENG",
                    "model": "WH-TIANWU-250-A",
                    "c_rate": 1.0,
                    "power_kW": 250,
                    "energy_kWh": 233,
                    "voltage_V": 832,
                    "lifespan_years": 15,
                    "eol_capacity_pct": 80,
                    "cycles_per_day": 1.0,
                    "cooling": "Liquid (Battery), Air (PCS)",
                    "weight_kg": 2600,
                    "dimensions_mm": [1400, 1350, 2100]
                }
            }
        except json.JSONDecodeError as e:
            st.error(f"❌ Error reading vendor_battery_database.json: {e}. Using hardcoded database.")
            # Fallback to hardcoded database on JSON error
            return {
                "TIANWU-50-233-0.25C": {
                    "company": "WEIHENG",
                    "model": "WH-TIANWU-50-233B",
                    "c_rate": 0.25,
                    "power_kW": 50,
                    "energy_kWh": 233,
                    "voltage_V": 832,
                    "lifespan_years": 15,
                    "eol_capacity_pct": 80,
                    "cycles_per_day": 1.0,
                    "cooling": "Liquid (Battery), Air (PCS)",
                    "weight_kg": 2700,
                    "dimensions_mm": [1400, 1350, 2100]
                },
                "TIANWU-100-233-0.5C": {
                    "company": "WEIHENG",
                    "model": "WH-TIANWU-100-233B",
                    "c_rate": 0.5,
                    "power_kW": 100,
                    "energy_kWh": 233,
                    "voltage_V": 832,
                    "lifespan_years": 15,
                    "eol_capacity_pct": 80,
                    "cycles_per_day": 1.0,
                    "cooling": "Liquid (Battery + PCS)",
                    "weight_kg": 2700,
                    "dimensions_mm": [1400, 1350, 2100]
                },
                "TIANWU-250-233-1C": {
                    "company": "WEIHENG",
                    "model": "WH-TIANWU-250-A",
                    "c_rate": 1.0,
                    "power_kW": 250,
                    "energy_kWh": 233,
                    "voltage_V": 832,
                    "lifespan_years": 15,
                    "eol_capacity_pct": 80,
                    "cycles_per_day": 1.0,
                    "cooling": "Liquid (Battery), Air (PCS)",
                    "weight_kg": 2600,
                    "dimensions_mm": [1400, 1350, 2100]
                }
            }
    
    # Load battery database
    battery_db = load_battery_database()
    
    # Section 1: Upload Load Profile
    st.header("📊 Section 1: Upload Load Profile")
    st.markdown("Upload a CSV file containing peak event data with the following columns:")
    
    expected_columns = [
        "Start Date", "Start Time", "End Date", "End Time",
        "Peak Load (kW)", "Excess (kW)", "Duration (min)",
        "Energy to Shave (kWh)", "Energy to Shave (Peak Period Only)",
        "MD Cost Impact (RM)"
    ]
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("**Expected columns:**")
        for col in expected_columns[:5]:
            st.markdown(f"• {col}")
    with col2:
        st.markdown("**Additional columns:**")
        for col in expected_columns[5:]:
            st.markdown(f"• {col}")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CSV file with load profile data",
        type=["csv"],
        help="Upload your peak events data from MD shaving analysis"
    )
    
    if uploaded_file is not None:
        try:
            # Read the uploaded file
            df = pd.read_csv(uploaded_file)
            st.success("✅ File uploaded successfully!")
            
            # Show basic info about the uploaded data
            st.subheader("📋 Data Overview")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                if "Energy to Shave (kWh)" in df.columns:
                    total_energy = df["Energy to Shave (kWh)"].sum()
                    st.metric("Total Energy to Shave", f"{total_energy:.1f} kWh")
                else:
                    st.metric("Energy Column", "Not Found")
            
            # Display first few rows
            st.subheader("📊 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Column validation
            missing_cols = [col for col in expected_columns if col not in df.columns]
            if missing_cols:
                st.warning(f"⚠️ Missing columns: {', '.join(missing_cols)}")
                st.info("The analysis will continue with available columns.")
            else:
                st.success("✅ All expected columns found!")
            
            # Proceed with analysis if we have the minimum required columns
            if "Energy to Shave (kWh)" in df.columns:
                # Section 2: Battery Selection and Sizing
                st.header("🔋 Section 2: Battery Selection and Sizing")
                
                # Battery selection
                battery_options = list(battery_db.keys())
                selected_battery = st.selectbox(
                    "Select Battery Model",
                    battery_options,
                    help="Choose from available WEIHENG TIANWU battery models"
                )
                
                # Display selected battery specifications
                battery_specs = battery_db[selected_battery]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Power Rating", f"{battery_specs['power_kW']} kW")
                    st.metric("Energy Capacity", f"{battery_specs['energy_kWh']} kWh")
                with col2:
                    st.metric("C-Rate", f"{battery_specs['c_rate']}C")
                    st.metric("Voltage", f"{battery_specs['voltage_V']} V")
                with col3:
                    st.metric("Lifespan", f"{battery_specs['lifespan_years']} years")
                    st.metric("EOL Capacity", f"{battery_specs['eol_capacity_pct']}%")
                
                # Battery quantity calculation
                st.subheader("🔢 Battery Sizing Calculation")
                
                # Calculate required energy and power
                total_energy_required = df["Energy to Shave (kWh)"].sum()
                if "Peak Load (kW)" in df.columns:
                    max_power_required = df["Peak Load (kW)"].max()
                else:
                    max_power_required = 0
                
                # Calculate number of batteries needed
                batteries_for_energy = math.ceil(total_energy_required / battery_specs['energy_kWh'])
                batteries_for_power = math.ceil(max_power_required / battery_specs['power_kW'])
                recommended_batteries = max(batteries_for_energy, batteries_for_power)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Batteries for Energy", batteries_for_energy)
                    st.metric("Total Energy Required", f"{total_energy_required:.1f} kWh")
                with col2:
                    st.metric("Batteries for Power", batteries_for_power)
                    st.metric("Max Power Required", f"{max_power_required:.1f} kW")
                
                st.info(f"**Recommended:** {recommended_batteries} battery units")
                
                # Allow manual override
                num_batteries = st.number_input(
                    "Number of Battery Units",
                    min_value=1,
                    value=recommended_batteries,
                    help="Adjust the number of battery units as needed"
                )
                
                # Calculate total system specifications
                total_power = num_batteries * battery_specs['power_kW']
                total_energy = num_batteries * battery_specs['energy_kWh']
                
                st.subheader("⚡ Total System Specifications")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Power", f"{total_power} kW")
                with col2:
                    st.metric("Total Energy", f"{total_energy} kWh")
                with col3:
                    st.metric("Total Weight", f"{num_batteries * battery_specs['weight_kg']:,} kg")
                with col4:
                    dimensions = battery_specs['dimensions_mm']
                    st.metric("Footprint", f"{dimensions[0]}×{dimensions[1]} mm")
                
                # Section 3: Real Degradation Analysis
                st.header("📉 Section 3: Real WEIHENG TIANWU Degradation Analysis")
                
                # WEIHENG TIANWU real degradation data (21 points over 20 years)
                degradation_data = {
                    'Year': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                    'SOH_Percent': [100.00, 93.78, 92.85, 91.92, 90.99, 90.06, 89.13, 88.20, 87.27, 86.34, 
                                   85.41, 84.48, 83.55, 82.62, 81.69, 79.95, 75.48, 71.01, 66.54, 62.07, 60.48]
                }
                
                degradation_df = pd.DataFrame(degradation_data)
                
                # Plot degradation curve
                fig_degradation = px.line(
                    degradation_df, 
                    x='Year', 
                    y='SOH_Percent',
                    title='WEIHENG TIANWU Real Degradation Curve (20-Year Laboratory Data)',
                    labels={'SOH_Percent': 'State of Health (%)', 'Year': 'Years of Operation'}
                )
                
                # Add EOL line at 80%
                fig_degradation.add_hline(
                    y=80, 
                    line_dash="dash", 
                    line_color="red",
                    annotation_text="End of Life (80% SOH)"
                )
                
                fig_degradation.update_layout(
                    xaxis_title="Years of Operation",
                    yaxis_title="State of Health (%)",
                    showlegend=False
                )
                
                st.plotly_chart(fig_degradation, use_container_width=True)
                
                # Calculate effective capacity over time
                st.subheader("🔋 Battery Capacity Over Time")
                
                degradation_df['Effective_Capacity_kWh'] = (degradation_df['SOH_Percent'] / 100) * total_energy
                degradation_df['Capacity_Loss_kWh'] = total_energy - degradation_df['Effective_Capacity_kWh']
                
                # Plot capacity over time
                fig_capacity = go.Figure()
                
                fig_capacity.add_trace(go.Scatter(
                    x=degradation_df['Year'],
                    y=degradation_df['Effective_Capacity_kWh'],
                    mode='lines+markers',
                    name='Effective Capacity',
                    line=dict(color='blue', width=3)
                ))
                
                fig_capacity.add_trace(go.Scatter(
                    x=degradation_df['Year'],
                    y=[total_energy] * len(degradation_df),
                    mode='lines',
                    name='Initial Capacity',
                    line=dict(color='green', dash='dash')
                ))
                
                fig_capacity.update_layout(
                    title=f'Battery System Capacity Degradation Over 20 Years ({num_batteries} Units)',
                    xaxis_title='Years of Operation',
                    yaxis_title='Capacity (kWh)',
                    showlegend=True
                )
                
                st.plotly_chart(fig_capacity, use_container_width=True)
                
                # Show capacity table
                st.subheader("📊 Capacity Degradation Table")
                display_df = degradation_df.copy()
                display_df['SOH_Percent'] = display_df['SOH_Percent'].round(2)
                display_df['Effective_Capacity_kWh'] = display_df['Effective_Capacity_kWh'].round(1)
                display_df['Capacity_Loss_kWh'] = display_df['Capacity_Loss_kWh'].round(1)
                
                st.dataframe(
                    display_df.rename(columns={
                        'Year': 'Year',
                        'SOH_Percent': 'SOH (%)',
                        'Effective_Capacity_kWh': 'Effective Capacity (kWh)',
                        'Capacity_Loss_kWh': 'Capacity Loss (kWh)'
                    }),
                    use_container_width=True
                )
                
                # Section 4: Financial Analysis
                st.header("💰 Section 4: Financial Analysis")
                
                col1, col2 = st.columns(2)
                with col1:
                    battery_cost_per_kwh = st.number_input(
                        "Battery Cost (RM/kWh)",
                        min_value=100.0,
                        max_value=5000.0,
                        value=800.0,
                        step=50.0,
                        help="Cost per kWh of battery capacity"
                    )
                
                with col2:
                    installation_cost_pct = st.number_input(
                        "Installation Cost (%)",
                        min_value=0.0,
                        max_value=100.0,
                        value=20.0,
                        step=5.0,
                        help="Installation cost as percentage of battery cost"
                    )
                
                # Calculate costs
                battery_cost = total_energy * battery_cost_per_kwh
                installation_cost = battery_cost * (installation_cost_pct / 100)
                total_system_cost = battery_cost + installation_cost
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Battery Cost", f"RM {battery_cost:,.0f}")
                with col2:
                    st.metric("Installation Cost", f"RM {installation_cost:,.0f}")
                with col3:
                    st.metric("Total System Cost", f"RM {total_system_cost:,.0f}")
                
                # Calculate annual savings if MD Cost Impact is available
                if "MD Cost Impact (RM)" in df.columns:
                    # Assume the data represents one period, calculate annual impact
                    period_savings = df["MD Cost Impact (RM)"].sum()
                    
                    # Estimate annual savings (adjust based on your data frequency)
                    data_period_days = st.number_input(
                        "Data Period (days)",
                        min_value=1,
                        max_value=365,
                        value=30,
                        help="Number of days the uploaded data represents"
                    )
                    
                    annual_savings = period_savings * (365 / data_period_days)
                    
                    st.subheader("💵 Return on Investment Analysis")
                    
                    if annual_savings > 0:
                        simple_payback = total_system_cost / annual_savings
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Annual Savings", f"RM {annual_savings:,.0f}")
                        with col2:
                            st.metric("Simple Payback", f"{simple_payback:.1f} years")
                        with col3:
                            roi_20_year = (annual_savings * 20 - total_system_cost) / total_system_cost * 100
                            st.metric("20-Year ROI", f"{roi_20_year:.1f}%")
                    else:
                        st.warning("⚠️ No cost savings detected in the uploaded data.")
                
                # Export functionality
                st.header("📤 Section 5: Export Results")
                
                if st.button("Generate Analysis Report"):
                    # Create a comprehensive report
                    report_data = {
                        'Analysis Summary': {
                            'Battery Model': selected_battery,
                            'Number of Units': num_batteries,
                            'Total Power (kW)': total_power,
                            'Total Energy (kWh)': total_energy,
                            'Total System Cost (RM)': total_system_cost
                        },
                        'Degradation Analysis': degradation_df.to_dict('records'),
                        'Raw Data': df.to_dict('records')
                    }
                    
                    # Convert to JSON for download
                    report_json = json.dumps(report_data, indent=2)
                    
                    st.download_button(
                        label="📥 Download Analysis Report (JSON)",
                        data=report_json,
                        file_name=f"md_shaving_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                    
                    # Also offer CSV download of degradation data
                    csv_data = degradation_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Degradation Data (CSV)",
                        data=csv_data,
                        file_name=f"battery_degradation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
                    st.success("✅ Reports generated successfully!")
            
            else:
                st.error("❌ Required column 'Energy to Shave (kWh)' not found in uploaded file.")
                st.info("Please ensure your CSV file contains the expected columns for MD shaving analysis.")
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.info("Please ensure the file is a valid CSV format with the expected columns.")
    
    else:
        st.info("👆 Please upload a CSV file to begin the analysis.")
        
        # Show example data format
        with st.expander("📋 Example Data Format"):
            example_data = {
                'Start Date': ['2024-01-15', '2024-01-16', '2024-01-17'],
                'Start Time': ['14:30', '09:15', '16:45'],
                'End Date': ['2024-01-15', '2024-01-16', '2024-01-17'],
                'End Time': ['15:00', '09:45', '17:15'],
                'Peak Load (kW)': [850, 920, 780],
                'Excess (kW)': [150, 220, 80],
                'Duration (min)': [30, 30, 30],
                'Energy to Shave (kWh)': [75, 110, 40],
                'Energy to Shave (Peak Period Only)': [75, 110, 40],
                'MD Cost Impact (RM)': [1245, 1680, 890]
            }
            
            example_df = pd.DataFrame(example_data)
            st.dataframe(example_df, use_container_width=True)
            st.caption("Sample format showing peak events that require MD shaving")