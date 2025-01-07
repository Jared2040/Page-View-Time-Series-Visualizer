import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data: Filter out top and bottom 2.5% of the data
lower_limit = df['value'].quantile(0.025)
upper_limit = df['value'].quantile(0.975)
df = df[(df['value'] >= lower_limit) & (df['value'] <= upper_limit)]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='r', linewidth=1)
    
    # Set titles and labels
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    # Save image and return fig
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    df_bar_monthly = df_bar.groupby(['year', 'month']).mean()['value'].unstack()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(12, 6))
    df_bar_monthly.plot(kind='bar', ax=ax, legend=True)

    # Set titles and labels
    ax.set_title('Average Monthly Page Views')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_xticklabels([str(year) for year in df_bar_monthly.index], rotation=0)

    # Update the legend to show full month names
    ax.legend(title='Months', labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    
    # Save image and return fig
    fig.savefig('bar_plot.png')
    return fig



def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box['year'] = df_box.index.year
    df_box['month'] = df_box.index.strftime('%b')  # Abbreviated month names
    df_box['month_number'] = df_box.index.month  # Add a month number column for sorting
    df_box = df_box.sort_values('month_number')  # Sort by month number

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise box plot
    sns.boxplot(
        x='month',
        y='value',
        data=df_box,
        ax=axes[1],
        order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    )
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].tick_params(axis='x', rotation=45)  # Rotate month labels

    # Save image and return fig
    fig.savefig('box_plot.png')
    return fig