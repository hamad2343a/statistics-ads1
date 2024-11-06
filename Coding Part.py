import os
import zipfile

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Unzip the uploaded file to examine its contents
zip_path = 'world top companies.zip'
extract_path = 'world_top_companies/'

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# List the CSV files and load data
files = [
    'Companies_ranked_by_Dividend_Yield.csv',
    'Companies_ranked_by_Earnings.csv',
    'Companies_ranked_by_Market_Cap.csv',
    'Companies_ranked_by_P_E_ratio.csv',
    'Companies_ranked_by_Revenue.csv'
]

dataframes = {}
for file in files:
    file_path = os.path.join(extract_path, file)
    df = pd.read_csv(file_path)
    dataframes[file] = df

# Set plot style for clarity and consistency
plt.style.use('ggplot')
sns.set_palette('muted')
plt.rcParams.update({
    'axes.titlesize': 18,
    'axes.labelsize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14,
    'figure.figsize': (12, 8)
})

# Concatenate all datasets into one for an overview
combined_df = pd.concat(dataframes.values(), ignore_index=True)
combined_df.drop_duplicates(inplace=True)

# Data Cleaning - Handling Missing Values
for column in combined_df.columns:
    if combined_df[column].dtype in ['float64', 'int64']:
        combined_df[column].fillna(combined_df[column].median(), inplace=True)
    elif combined_df[column].dtype == 'object':
        combined_df[column].fillna(combined_df[column].mode()[0], inplace=True)

# Descriptive Statistics
print("Descriptive Statistics:\n", combined_df.describe())
print("\nCorrelation Matrix:\n", combined_df.corr(numeric_only=True))

# Function to plot Pie Chart of Market Cap Distribution by Country (Top 10 countries)
def plot_market_cap_pie_chart(df):
    top_10_countries = df['country'].value_counts().nlargest(10)
    plt.figure()
    top_10_countries.plot(kind='pie', autopct='%1.1f%%', startangle=140, cmap='viridis')
    plt.title('Market Cap Distribution by Country (Top 10)', fontweight='bold')
    plt.ylabel('')
    plt.tight_layout()
    plt.show()

# Function to plot Line Plot for Top 10 Companies by Revenue
# Adding year to the plot
def plot_top_revenue_line_chart(df):
    top_10_revenue = df.nlargest(10, 'revenue_ttm')
    plt.figure()
    sns.lineplot(x='Name', y='revenue_ttm', data=top_10_revenue, marker='o', linestyle='-', color='b')
    plt.title('Top 10 Companies by Revenue (Year: 2023)', fontweight='bold')
    plt.xlabel('Company Name', fontweight='bold')
    plt.ylabel('Revenue (in Billion GBP)', fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontweight='bold')
    plt.yticks(fontweight='bold')
    plt.tight_layout()
    plt.show()

# Function to plot Box Plot for Price by Country (Top 5 countries)
def plot_price_boxplot(df):
    top_5_countries = df['country'].value_counts().nlargest(5).index
    filtered_df = df[df['country'].isin(top_5_countries)]
    plt.figure()
    sns.boxplot(x='country', y='price (GBP)', data=filtered_df, palette='Set2')
    plt.title('Price Distribution by Country (Top 5 Countries)', fontweight='bold')
    plt.xlabel('Country', fontweight='bold')
    plt.ylabel('Price (GBP)', fontweight='bold')
    plt.xticks(fontweight='bold')
    plt.yticks(fontweight='bold')
    plt.tight_layout()
    plt.show()

# Call the plotting functions
plot_market_cap_pie_chart(combined_df)
plot_top_revenue_line_chart(dataframes['Companies_ranked_by_Revenue.csv'])
plot_price_boxplot(combined_df)