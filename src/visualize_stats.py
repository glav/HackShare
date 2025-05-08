#!/usr/bin/env python3
"""
Query Processing Visualization Script

This script generates visualizations based on the query processing statistics
from stats.json and saves them as image files.
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

# Set visualization style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = [12, 8]
plt.rcParams['font.size'] = 12

# Create output directory for images
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'visualizations')
os.makedirs(output_dir, exist_ok=True)

def load_stats():
    """Load the statistics from the JSON file."""
    stats_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stats.json')
    with open(stats_path, 'r') as file:
        stats = json.load(file)
    return stats

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

def generate_completion_gauge(stats, output_dir):
    """Generate a gauge chart showing the completion percentage."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=stats['completion_percentage'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Completion Rate"},
        delta={'reference': 100},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 100], 'color': "#E0F2F1"}
            ]
        }
    ))

    fig.update_layout(
        height=300
    )

    output_path = os.path.join(output_dir, 'completion_gauge.png')
    fig.write_image(output_path, scale=2)
    print(f"Saved completion gauge to {output_path}")
    return fig

def generate_comparative_bar_chart(stats, output_dir):
    """Generate a bar chart comparing pass and fail counts."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=['Results'],
        y=[stats['pass_count']],
        name='Pass',
        marker_color='#4CAF50',
        text=[f"{stats['pass_count']} ({stats['pass_percentage']:.1f}%)"],
        textposition='auto'
    ))

    fig.add_trace(go.Bar(
        x=['Results'],
        y=[stats['fail_count']],
        name='Fail',
        marker_color='#F44336',
        text=[f"{stats['fail_count']} ({stats['fail_percentage']:.1f}%)"],
        textposition='auto'
    ))

    fig.update_layout(
        title='Pass vs Fail Counts',
        yaxis=dict(title='Count'),
        barmode='group',
        title_x=0.5
    )

    output_path = os.path.join(output_dir, 'pass_fail_bar_chart.png')
    fig.write_image(output_path, scale=2)
    print(f"Saved bar chart to {output_path}")
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

def generate_combined_dashboard(stats, output_dir):
    """Generate a combined dashboard with all visualizations."""
    fig = make_subplots(
        rows=2, cols=2,
        specs=[
            [{"type": "pie"}, {"type": "indicator"}],
            [{"type": "bar"}, {"type": "indicator"}]
        ],
        subplot_titles=("Pass/Fail Distribution", "Success Rate",
                        "Pass vs Fail Counts", "Completion Rate")
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

    # Add bar chart
    fig.add_trace(
        go.Bar(
            x=['Pass'],
            y=[stats['pass_count']],
            marker_color='#4CAF50',
            showlegend=False
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Bar(
            x=['Fail'],
            y=[stats['fail_count']],
            marker_color='#F44336',
            showlegend=False
        ),
        row=2, col=1
    )

    # Add completion gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=stats['completion_percentage'],
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 100], 'color': "#E0F2F1"}
                ],
            }
        ),
        row=2, col=2
    )

    fig.update_layout(
        height=800,
        width=1000,
        title_text="Query Processing Analysis Dashboard",
        title_x=0.5
    )

    output_path = os.path.join(output_dir, 'dashboard.png')
    fig.write_image(output_path, scale=2)
    print(f"Saved combined dashboard to {output_path}")
    return fig

def main():
    """Main function to generate all visualizations."""
    stats = load_stats()
    summary_df = create_summary_dataframe(stats)
    print("Summary Statistics:")
    print(summary_df)

    # Generate all visualizations
    generate_pass_fail_pie_chart(stats, output_dir)
    generate_success_rate_gauge(stats, output_dir)
    generate_completion_gauge(stats, output_dir)
    generate_comparative_bar_chart(stats, output_dir)
    generate_summary_report(stats, output_dir)
    generate_combined_dashboard(stats, output_dir)

    print(f"\nAll visualizations saved to: {output_dir}")

if __name__ == "__main__":
    main()
