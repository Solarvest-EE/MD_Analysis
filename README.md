# MD Shaving Analysis Tool

A comprehensive Maximum Demand (MD) shaving analysis tool with battery energy storage solutions.

## Features

- **MD Shaving Solution**: Basic MD shaving analysis and battery sizing
- **Advanced MD Shaving**: Real WEIHENG TIANWU battery degradation modeling
- **Real Degradation Data**: 20-year battery lifecycle analysis with non-linear patterns
- **Financial Analysis**: ROI calculations and payback period analysis
- **Export Capabilities**: Download analysis reports and degradation data

## Live Demo

🚀 **[Try the app here](https://md-analysis.streamlit.app)**

## Key Features

### 🔋 Battery Analysis
- Real WEIHENG TIANWU degradation curves (not linear approximations)
- 21 data points over 20-year period
- State of Health (SOH) measurements from laboratory testing
- End-of-life defined at 80% SOH

### 📊 Analysis Capabilities
- CSV file upload for peak event data
- Automatic battery sizing calculations
- Interactive degradation charts
- Comprehensive financial modeling

### 💰 Financial Planning
- Battery cost calculations
- Installation cost estimates
- ROI and payback period analysis
- 20-year investment projections

## Usage

1. **Upload Data**: Upload a CSV file with peak event data
2. **Select Battery**: Choose from WEIHENG TIANWU battery models
3. **Configure System**: Adjust battery quantities and costs
4. **Analyze Results**: View degradation curves and financial analysis
5. **Export Reports**: Download analysis reports and data

## Expected CSV Format

Your CSV file should contain the following columns:
- Start Date, Start Time, End Date, End Time
- Peak Load (kW), Excess (kW), Duration (min)
- Energy to Shave (kWh), Energy to Shave (Peak Period Only)
- MD Cost Impact (RM)

## Installation (Local Development)

```bash
git clone https://github.com/yourusername/MD_Analysis.git
cd MD_Analysis
pip install -r requirements.txt
streamlit run main.py
```

## Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **NumPy**: Numerical computations

## About

This tool integrates actual WEIHENG TIANWU series degradation data to provide accurate battery performance predictions and financial analysis for MD shaving applications.

## License

MIT License - see LICENSE file for details.
