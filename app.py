import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style for better visualizations
plt.style.use('ggplot')
sns.set_palette("bright")
plt.rcParams['figure.figsize'] = [10, 6]
plt.rcParams['font.size'] = 12

# Page setup with custom styling
st.set_page_config(page_title="Walmart Restock Cycle Analyzer", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0071ce;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #004c91;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .insight-box {
        background-color: #f8f9fa;
        border-left: 4px solid #ffc220;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.3rem;
        color: #333333;
    }
    .insight-box h4 {
        color: #0071ce;
        margin-bottom: 0.5rem;
    }
    .insight-box ul {
        margin-top: 0.5rem;
    }
    .insight-box strong {
        color: #004c91;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 0.15rem 0.5rem rgba(0, 0, 0, 0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown('<div class="main-header">📦 Walmart Restock Cycle Analyzer</div>', unsafe_allow_html=True)
st.markdown("Comprehensive analysis of logistics operations, focusing on truck schedules, delay patterns, stockout behavior, and department performance.")


# Load dataset with caching for better performance
@st.cache_data
def load_data():
    df = pd.read_csv("Walmart_Logistics_Dataset.csv")
    # Convert date to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    # Convert time columns to datetime
    for col in ['Truck Arrival Time', 'Unloading Start Time', 'Shelf Stock Time']:
        df[col] = pd.to_datetime(df[col], format="%H:%M", errors='coerce')
    # Calculate delay in minutes
    df["Delay_Minutes"] = (df["Shelf Stock Time"] - df["Truck Arrival Time"]).dt.total_seconds() / 60
    # Handle negative delays (crossing midnight)
    df.loc[df["Delay_Minutes"] < 0, "Delay_Minutes"] += 24 * 60
    # Fill None values in Delay Reason
    df["Delay Reason"] = df["Delay Reason"].fillna("None")
    return df


df = load_data()

# Sidebar filters with improved UI
with st.sidebar:
    st.markdown('<div class="sub-header">📊 Filters</div>', unsafe_allow_html=True)
    
    # Date range filter
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    
    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date
    
    # Department filter
    all_departments = sorted(df["Department"].unique())
    selected_departments = st.multiselect(
        "Departments",
        options=all_departments,
        default=all_departments
    )
    
    # Delay reason filter
    all_reasons = sorted(df["Delay Reason"].unique())
    selected_reasons = st.multiselect(
        "Delay Reasons",
        options=all_reasons,
        default=all_reasons
    )
    
    # Stockout filter
    stockout_filter = st.radio(
        "Stockout Status",
        options=["All", "Stockout", "No Stockout"],
        index=0
    )
    
    # Reset filters button
    if st.button("Reset All Filters"):
        # This will trigger a rerun with default values
        st.experimental_rerun()

# Apply filters
filtered_df = df.copy()

# Date filter
filtered_df = filtered_df[
    (filtered_df["Date"].dt.date >= start_date) & 
    (filtered_df["Date"].dt.date <= end_date)
]

# Department filter
if selected_departments:
    filtered_df = filtered_df[filtered_df["Department"].isin(selected_departments)]

# Delay reason filter
if selected_reasons:
    filtered_df = filtered_df[filtered_df["Delay Reason"].isin(selected_reasons)]

# Stockout filter
if stockout_filter == "Stockout":
    filtered_df = filtered_df[filtered_df["Stockout Observed"] == "Yes"]
elif stockout_filter == "No Stockout":
    filtered_df = filtered_df[filtered_df["Stockout Observed"] == "No"]

# Display warning if no data after filtering
if len(filtered_df) == 0:
    st.warning("No data available with the current filter settings. Please adjust your filters.")
    st.stop()

# Key Metrics Section with improved styling
st.markdown('<div class="sub-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_deliveries = len(filtered_df)
    st.markdown(
        f"""
        <div class="metric-card">
            <div style="font-size: 2.2rem; font-weight: 700; color: #0071ce;">{total_deliveries}</div>
            <div style="font-size: 1rem; color: #4a4a4a;">Total Deliveries</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col2:
    delayed_deliveries = filtered_df[filtered_df["Delay Reason"] != "None"].shape[0]
    delay_percentage = round((delayed_deliveries / total_deliveries) * 100, 1)
    st.markdown(
        f"""
        <div class="metric-card">
            <div style="font-size: 2.2rem; font-weight: 700; color: #0071ce;">{delay_percentage}%</div>
            <div style="font-size: 1rem; color: #4a4a4a;">Deliveries Delayed ({delayed_deliveries})</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col3:
    stockouts = filtered_df[filtered_df["Stockout Observed"] == "Yes"].shape[0]
    stockout_percentage = round((stockouts / total_deliveries) * 100, 1)
    st.markdown(
        f"""
        <div class="metric-card">
            <div style="font-size: 2.2rem; font-weight: 700; color: #0071ce;">{stockout_percentage}%</div>
            <div style="font-size: 1rem; color: #4a4a4a;">Stockouts Observed ({stockouts})</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col4:
    avg_delay = round(filtered_df["Delay_Minutes"].mean(), 1)
    st.markdown(
        f"""
        <div class="metric-card">
            <div style="font-size: 2.2rem; font-weight: 700; color: #0071ce;">{avg_delay}</div>
            <div style="font-size: 1rem; color: #4a4a4a;">Avg. Delay (minutes)</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Create tabs for different analysis views
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Delay Analysis", 
    "⏱️ Department Performance", 
    "📦 Stockout Patterns",
    "📅 Time-Based Analysis"
])

# Tab 1: Delay Analysis
with tab1:
    st.markdown('<div class="sub-header">📊 Delay Reasons Frequency & Impact</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Delay Reason Frequency
        delay_data = filtered_df[filtered_df["Delay Reason"] != "None"]
        
        if len(delay_data) > 0:
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            sns.countplot(
                y=delay_data["Delay Reason"], 
                order=delay_data["Delay Reason"].value_counts().index, 
                ax=ax1, 
                palette="Reds_r"
            )
            ax1.set_title("Frequency of Delay Reasons", fontsize=16)
            ax1.set_xlabel("Number of Occurrences", fontsize=12)
            ax1.set_ylabel("Delay Reason", fontsize=12)
            
            # Add count labels
            for i, count in enumerate(delay_data["Delay Reason"].value_counts()):
                ax1.text(count + 1, i, f"{count} ({count/len(delay_data)*100:.1f}%)", va='center')
            
            st.pyplot(fig1)
        else:
            st.info("No delay data available with current filters.")
    
    with col2:
        # Average Delay Time by Reason
        if len(delay_data) > 0:
            avg_delay_by_reason = filtered_df.groupby("Delay Reason")["Delay_Minutes"].mean().sort_values()
            
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            avg_delay_by_reason.plot(kind='barh', ax=ax2, color=sns.color_palette("Reds_r", len(avg_delay_by_reason)))
            ax2.set_title("Average Delay Time by Reason", fontsize=16)
            ax2.set_xlabel("Average Delay (minutes)", fontsize=12)
            ax2.set_ylabel("Delay Reason", fontsize=12)
            
            # Add value labels
            for i, value in enumerate(avg_delay_by_reason):
                ax2.text(value + 1, i, f"{value:.1f} min", va='center')
            
            st.pyplot(fig2)
        else:
            st.info("No delay data available with current filters.")
    
    # Insights box
    st.markdown(
        """
        <div class="insight-box">
            <h4>📋 Key Insights - Delay Analysis</h4>
            <ul>
                <li><strong>Primary Delay Factors:</strong> The visualization reveals the most 
                frequent causes of delays in the restock cycle, highlighting areas that need 
                immediate attention.</li>
                <li><strong>Delay Severity:</strong> While some reasons may occur frequently, 
                others might cause longer delays on average. This helps prioritize which issues 
                to address first.</li>
                <li><strong>Impact Assessment:</strong> By comparing frequency with average delay 
                time, we can identify which delay reasons have the greatest overall impact on 
                operations.</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Tab 2: Department Performance
with tab2:
    st.markdown('<div class="sub-header">⏱️ Department Performance Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Average Delay by Department
        dept_delay = filtered_df.groupby("Department")["Delay_Minutes"].mean().sort_values()
        
        fig3, ax3 = plt.subplots(figsize=(10, 8))
        dept_delay.plot(
            kind='barh', 
            ax=ax3, 
            color=sns.color_palette("Blues_r", len(dept_delay))
        )
        ax3.set_title("Average Delay Time per Department", fontsize=16)
        ax3.set_xlabel("Average Delay (minutes)", fontsize=12)
        ax3.set_ylabel("Department", fontsize=12)
        
        # Add value labels
        for i, value in enumerate(dept_delay):
            ax3.text(value + 1, i, f"{value:.1f} min", va='center')
        
        st.pyplot(fig3)
    
    with col2:
        # Stockouts by Department
        stockouts = filtered_df[filtered_df["Stockout Observed"] == "Yes"]["Department"].value_counts().sort_values()
        
        fig4, ax4 = plt.subplots(figsize=(10, 8))
        stockouts.plot(
            kind='barh', 
            ax=ax4, 
            color=sns.color_palette("Oranges_r", len(stockouts))
        )
        ax4.set_title("Stockouts by Department", fontsize=16)
        ax4.set_xlabel("Number of Stockouts", fontsize=12)
        ax4.set_ylabel("Department", fontsize=12)
        
        # Add value labels
        for i, value in enumerate(stockouts):
            ax4.text(value + 0.1, i, str(value), va='center')
        
        st.pyplot(fig4)
    
    # Insights box
    st.markdown(
        """
        <div class="insight-box">
            <h4>📋 Key Insights - Department Performance</h4>
            <ul>
                <li><strong>Department Efficiency:</strong> The charts reveal which departments 
                have the most efficient restock cycles and which ones need improvement.</li>
                <li><strong>Stockout Correlation:</strong> Departments with longer delays often 
                experience more stockouts, indicating a direct relationship between delay time 
                and inventory availability.</li>
                <li><strong>Resource Allocation:</strong> Departments with higher delays may need 
                additional staff or process improvements to reduce restock cycle times.</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Tab 3: Stockout Patterns
with tab3:
    st.markdown('<div class="sub-header">📦 Stockout Patterns Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Stockout Percentage by Department
        dept_stockout = filtered_df.groupby("Department")["Stockout Observed"].apply(
            lambda x: (x == "Yes").mean() * 100
        ).sort_values()
        
        fig5, ax5 = plt.subplots(figsize=(10, 8))
        dept_stockout.plot(
            kind='barh', 
            ax=ax5, 
            color=sns.color_palette("Reds_r", len(dept_stockout))
        )
        ax5.set_title("Stockout Percentage by Department", fontsize=16)
        ax5.set_xlabel("Stockout Percentage (%)", fontsize=12)
        ax5.set_ylabel("Department", fontsize=12)
        
        # Add value labels
        for i, value in enumerate(dept_stockout):
            ax5.text(value + 0.5, i, f"{value:.1f}%", va='center')
        
        st.pyplot(fig5)
    
    with col2:
        # Correlation Between Delay Time and Stockouts
        delay_stockout_corr = filtered_df.groupby("Stockout Observed")["Delay_Minutes"].mean()
        
        fig6, ax6 = plt.subplots(figsize=(10, 6))
        delay_stockout_corr.plot(
            kind='bar', 
            ax=ax6, 
            color=['#4a4a4a', '#e01a2b']
        )
        ax6.set_title("Average Delay Time: Stockout vs. No Stockout", fontsize=16)
        ax6.set_xlabel("Stockout Observed", fontsize=12)
        ax6.set_ylabel("Average Delay (minutes)", fontsize=12)
        
        # Add value labels
        for i, value in enumerate(delay_stockout_corr):
            ax6.text(i, value + 1, f"{value:.1f} min", ha='center')
        
        st.pyplot(fig6)
    
    # Insights box
    st.markdown(
        """
        <div class="insight-box">
            <h4>📋 Key Insights - Stockout Patterns</h4>
            <ul>
                <li><strong>High-Risk Departments:</strong> Identifies departments with the 
                highest stockout rates, helping prioritize inventory management improvements.</li>
                <li><strong>Delay-Stockout Correlation:</strong> Shows how delays correlate with 
                stockout occurrences, revealing causal relationships.</li>
                <li><strong>Inventory Planning:</strong> Departments with high stockout 
                percentages may need revised inventory policies or buffer stock adjustments.</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Tab 4: Time-Based Analysis
with tab4:
    st.markdown('<div class="sub-header">📅 Time-Based Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily Truck Volume
        daily_counts = filtered_df["Date"].dt.date.value_counts().sort_index()
        
        fig7, ax7 = plt.subplots(figsize=(12, 6))
        daily_counts.plot(
            ax=ax7, 
            marker='o', 
            linestyle='-', 
            color='green',
            linewidth=2
        )
        ax7.set_title("Daily Truck Volume Over Time", fontsize=16)
        ax7.set_ylabel("Number of Deliveries", fontsize=12)
        ax7.set_xlabel("Date", fontsize=12)
        ax7.grid(True, alpha=0.3)
        
        # Add trend line
        if len(daily_counts) > 1:
            z = np.polyfit(range(len(daily_counts)), daily_counts, 1)
            p = np.poly1d(z)
            ax7.plot(daily_counts.index, p(range(len(daily_counts))), "r--", linewidth=1)
        
        st.pyplot(fig7)
    
    with col2:
        # Day of Week Analysis
        filtered_df["Day of Week"] = filtered_df["Date"].dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_delay = filtered_df.groupby("Day of Week")["Delay_Minutes"].mean()
        dow_delay = dow_delay.reindex(day_order)
        
        fig8, ax8 = plt.subplots(figsize=(12, 6))
        dow_delay.plot(
            kind='bar', 
            ax=ax8, 
            color=sns.color_palette("viridis", len(dow_delay))
        )
        ax8.set_title("Average Delay by Day of Week", fontsize=16)
        ax8.set_xlabel("Day of Week", fontsize=12)
        ax8.set_ylabel("Average Delay (minutes)", fontsize=12)
        
        # Add value labels
        for i, value in enumerate(dow_delay):
            ax8.text(i, value + 1, f"{value:.1f} min", ha='center')
        
        st.pyplot(fig8)
    
    # Insights box
    st.markdown(
        """
        <div class="insight-box">
            <h4>📋 Key Insights - Time-Based Analysis</h4>
            <ul>
                <li><strong>Volume Patterns:</strong> The daily truck volume chart reveals patterns 
                and trends in delivery frequency, helping with staff scheduling.</li>
                <li><strong>Weekly Patterns:</strong> The day of week analysis shows which days 
                experience the most delays, allowing for targeted process improvements.</li>
                <li><strong>Trend Analysis:</strong> The trend line indicates whether delivery 
                volumes are increasing or decreasing over time, informing capacity planning.</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Data Table Section
st.markdown('<div class="sub-header">🔍 Filtered Data</div>', unsafe_allow_html=True)
st.dataframe(filtered_df)
