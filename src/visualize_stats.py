#!/usr/bin/env python3
"""
Query Processing Visualization Script

This script generates visualizations based on the query processing statistics
from a JSON file and saves them as image files.
"""

import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import argparse

# Set visualization style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 12

# Create output directory for images
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'visualizations')
os.makedirs(output_dir, exist_ok=True)

def load_stats(stats_file='stats.json'):
    """
    Load the statistics from the JSON file.

    Args:
        stats_file (str): The name of the JSON file with statistics

    Returns:
        tuple: (latest_stats, all_stats) where latest_stats is the last object and all_stats is the complete array
    """
    stats_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), stats_file)
    with open(stats_path, 'r') as file:
        data = json.load(file)

    # Check if the loaded data is an array
    if isinstance(data, list):
        latest_stats = data[-1]  # Get the last object from the array
        all_stats = data  # Keep the complete array for time-series visualization
        print(f"Loaded stats from entry {len(data)} of {len(data)} in the array")
        print(f"Found {len(data)} stats entries for time-series visualization")
    else:
        # Handle case where it's already a single object
        latest_stats = data
        all_stats = [data]  # Wrap in list for consistent handling
        print("Loaded single stats entry (no time-series data available)")

    return latest_stats, all_stats

def create_summary_dataframe(stats):
    """Create a summary DataFrame from the stats."""
    summary_data = {
        'Metric': ['Total Queries', 'Processed Queries', 'Remaining Queries', 'Pass Count', 'Fail Count'],
        'Value': [stats['total_queries'], stats['processed_queries'], stats['remaining_queries'],
                  stats['pass_count'], stats['fail_count']]
    }
    return pd.DataFrame(summary_data)

def generate_pass_fail_pie_chart(stats, output_dir):
    """Generate a pie chart showing the pass/fail distribution."""
    labels = ['Pass', 'Fail']
    values = [stats['pass_count'], stats['fail_count']]

    fig = px.pie(
        names=labels,
        values=values,
        title='Query Processing Results',
        color=labels,
        color_discrete_map={'Pass': '#4CAF50', 'Fail': '#F44336'},
        hole=0.4
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        title_x=0.5,
        annotations=[dict(text=f'Total: {stats["total_queries"]}', x=0.5, y=0.5, font_size=15, showarrow=False)]
    )

    output_path = os.path.join(output_dir, 'pass_fail_pie_chart.png')
    fig.write_image(output_path, scale=2)
    print(f"Saved pie chart to {output_path}")
    return fig

def generate_success_rate_gauge(stats, output_dir):
    """Generate a gauge chart showing the success rate percentage."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=stats['pass_percentage'],
        title={'text': "Success Rate (%)"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#1f77b4"},
            'steps': [
                {'range': [0, 50], 'color': "#ffcccb"},
                {'range': [50, 75], 'color': "#ffff99"},
                {'range': [75, 100], 'color': "#c8e6c9"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': stats['pass_percentage']
            }
        }
    ))

    fig.update_layout(
        height=400,
        width=500
    )

    output_path = os.path.join(output_dir, 'success_rate_gauge.png')
    fig.write_image(output_path, scale=2)
    print(f"Saved success rate gauge to {output_path}")
    return fig

def generate_success_rate_over_time(all_stats, output_dir):
    """
    Generate a bar chart showing success rate over time across multiple stats entries.

    Args:
        all_stats (list): List of stats objects containing pass_percentage values
        output_dir (str): Directory to save the visualization

    Returns:
        Figure: The generated plotly figure
    """
    # Create data for the chart
    data = []
    for i, stats in enumerate(all_stats):
        # Use either timestamp if available, or just the entry number
        timestamp = stats.get('timestamp', f'Run {i+1}')
        data.append({
            'Run': timestamp,
            'Success Rate (%)': stats['pass_percentage'],
            'Index': i + 1  # For sorting
        })

    # Convert to dataframe for easier plotting
    df = pd.DataFrame(data)

    # Create the bar chart
    fig = px.bar(
        df,
        x='Index',
        y='Success Rate (%)',
        title='Success Rate Over Time',
        text_auto='.1f',
        labels={'Index': 'Run Number', 'Success Rate (%)': 'Success Rate (%)'}
    )

    # Improve layout
    fig.update_layout(
        title_x=0.5,
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ),
        yaxis=dict(
            range=[0, 100]
        ),
        plot_bgcolor='rgba(0,0,0,0.02)'
    )

    # Add a trendline if more than 2 data points
    if len(all_stats) > 2:
        x = list(range(1, len(all_stats) + 1))
        y = [stats['pass_percentage'] for stats in all_stats]

        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines',
            name='Trend',
            line=dict(color='red', width=2, dash='dot')
        ))

    # Save the figure
    output_path = os.path.join(output_dir, 'success_rate_over_time.png')
    fig.write_image(output_path, scale=2)
    print(f"Saved success rate over time chart to {output_path}")

    return fig

def generate_summary_report(stats, output_dir):
    """Generate a text-based summary report."""
    report = f"""
    # Query Processing Analysis Summary

    ## Overview
    - Total Queries: {stats['total_queries']}
    - Processed Queries: {stats['processed_queries']} ({stats['completion_percentage']:.1f}%)
    - Remaining Queries: {stats['remaining_queries']}

    ## Results
    - Pass Count: {stats['pass_count']} ({stats['pass_percentage']:.1f}%)
    - Fail Count: {stats['fail_count']} ({stats['fail_percentage']:.1f}%)

    ## Conclusions
    - The completion rate is {stats['completion_percentage']:.1f}%
    - The success rate is {stats['pass_percentage']:.1f}%
    - The failure rate is {stats['fail_percentage']:.1f}%
    """

    output_path = os.path.join(output_dir, 'summary_report.md')
    with open(output_path, 'w') as f:
        f.write(report)
    print(f"Saved summary report to {output_path}")

def generate_combined_dashboard(stats, all_stats, output_dir):
    """Generate a combined dashboard with all visualizations.

    Args:
        stats (dict): Latest stats object for current visualizations
        all_stats (list): List of all stats objects for time-series visualization
        output_dir (str): Directory to save the visualization
    """
    fig = make_subplots(
        rows=2, cols=2,
        specs=[
            [{"type": "pie"}, {"type": "indicator"}],
            [{"type": "bar", "colspan": 2}, None]
        ],
        subplot_titles=("Pass/Fail Distribution", "Success Rate",
                        "Success Rate Over Time")
    )

    # Add pie chart
    labels = ['Pass', 'Fail']
    values = [stats['pass_count'], stats['fail_count']]
    fig.add_trace(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=['#4CAF50', '#F44336'])
        ),
        row=1, col=1
    )

    # Add success rate gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=stats['pass_percentage'],
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#1f77b4"},
                'steps': [
                    {'range': [0, 50], 'color': "#ffcccb"},
                    {'range': [50, 75], 'color': "#ffff99"},
                    {'range': [75, 100], 'color': "#c8e6c9"}
                ],
            }
        ),
        row=1, col=2
    )

    # Add success rate over time chart
    x_values = list(range(1, len(all_stats) + 1))
    y_values = [s['pass_percentage'] for s in all_stats]

    fig.add_trace(
        go.Bar(
            x=x_values,
            y=y_values,
            marker_color='#2196F3',
            text=[f"{val:.1f}%" for val in y_values],
            textposition='auto',
            name='Success Rate'
        ),
        row=2, col=1
    )

    # Add trend line if we have enough data points
    if len(all_stats) > 2:
        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=y_values,
                mode='lines',
                name='Trend',
                line=dict(color='red', width=2, dash='dot')
            ),
            row=2, col=1
        )

    # Update layout for the dashboard
    fig.update_layout(
        height=800,  # Reduced height since we have fewer visualizations
        width=1000,
        title_text="Query Processing Analysis Dashboard",
        title_x=0.5
    )

    # Update x-axis for the success rate over time chart
    fig.update_xaxes(title_text="Run Number", row=2, col=1)
    fig.update_yaxes(title_text="Success Rate (%)", range=[0, 100], row=2, col=1)

    output_path = os.path.join(output_dir, 'dashboard.png')
    fig.write_image(output_path, scale=2)
    print(f"Saved combined dashboard to {output_path}")
    return fig

def main():
    """Main function to generate all visualizations."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate visualizations from query processing statistics')
    parser.add_argument('--file', '-f', dest='stats_file', default='stats.json',
                      help='JSON file containing statistics (default: stats.json)')
    args = parser.parse_args()

    print(f"Loading statistics from: {args.stats_file}")
    latest_stats, all_stats = load_stats(args.stats_file)
    summary_df = create_summary_dataframe(latest_stats)
    print("Summary Statistics:")
    print(summary_df)

    # Generate all visualizations
    generate_pass_fail_pie_chart(latest_stats, output_dir)
    generate_success_rate_gauge(latest_stats, output_dir)
    generate_success_rate_over_time(all_stats, output_dir)
    generate_summary_report(latest_stats, output_dir)
    generate_combined_dashboard(latest_stats, all_stats, output_dir)

    print(f"\nAll visualizations saved to: {output_dir}")

if __name__ == "__main__":
    main()
