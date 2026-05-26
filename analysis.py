# ==========================================
# E-COMMERCE DATA ANALYSIS PROJECT
# ==========================================

# Step 1: Import libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# Step 2: Load dataset
# ==========================================

df = pd.read_csv("amazon_sales.csv")

# ==========================================
# Step 3: Basic dataset information
# ==========================================

print("First 5 Rows")
print(df.head())

print("\nDataset Shape")
print(df.shape)

print("\nColumns")
print(df.columns)

print("\nData Types")
print(df.dtypes)

print("\nMissing Values")
print(df.isnull().sum())

print("\nStatistical Summary")
print(df.describe())

# ==========================================
# Step 4: Data Cleaning
# ==========================================

# Convert date column

df['purchase_date'] = pd.to_datetime(
    df['purchase_date'],
    format='%d-%m-%Y'
)

# Remove duplicate rows

df = df.drop_duplicates()

print("\nDuplicates Removed")

# ==========================================
# Step 5: Total Revenue
# ==========================================

total_revenue = df['final_price'].sum()

print("\nTotal Revenue:")
print(total_revenue)

# ==========================================
# Step 6: Category Analysis
# ==========================================

category_sales = df.groupby('category')['final_price'].sum()

print("\nCategory Sales")
print(category_sales)

# Plot

plt.figure(figsize=(8,5))
category_sales.plot(kind='bar')

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.show()

# ==========================================
# Step 7: Brand Analysis
# ==========================================

brand_sales = df.groupby('brand')['final_price'].sum()

print("\nBrand Sales")
print(brand_sales.sort_values(ascending=False))

plt.figure(figsize=(10,5))

brand_sales.sort_values().plot(kind='barh')

plt.title("Brand Revenue")

plt.xlabel("Revenue")

plt.show()

# ==========================================
# Step 8: Return Analysis
# ==========================================

return_count = df['is_returned'].value_counts()

print("\nReturn Analysis")
print(return_count)

plt.figure(figsize=(6,6))

return_count.plot(
    kind='pie',
    autopct='%1.1f%%'
)

plt.ylabel("")

plt.title("Returned vs Not Returned")

plt.show()

# ==========================================
# Step 9: Payment Method Analysis
# ==========================================

payment = df.groupby('payment_method')['final_price'].sum()

print("\nPayment Analysis")
print(payment)

plt.figure(figsize=(8,5))

payment.plot(kind='bar')

plt.title("Revenue by Payment Method")

plt.xlabel("Payment Method")

plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.show()

# ==========================================
# Step 10: Device Analysis
# ==========================================

device = df.groupby('device')['final_price'].sum()

print("\nDevice Sales")
print(device)

plt.figure(figsize=(7,5))

device.plot(kind='bar')

plt.title("Sales by Device")

plt.xlabel("Device")

plt.ylabel("Revenue")

plt.show()

# ==========================================
# Step 11: City Analysis
# ==========================================

location = df.groupby('location')['final_price'].sum()

print("\nLocation Sales")
print(location)

plt.figure(figsize=(8,5))

location.plot(kind='bar')

plt.title("Revenue by City")

plt.xlabel("Location")

plt.ylabel("Revenue")

plt.show()

# ==========================================
# Step 12: Delivery Status Analysis
# ==========================================

delivery = df['delivery_status'].value_counts()

print("\nDelivery Status")

print(delivery)

plt.figure(figsize=(7,5))

delivery.plot(kind='bar')

plt.title("Delivery Status")

plt.xlabel("Status")

plt.ylabel("Count")

plt.show()

# ==========================================
# Step 13: Monthly Sales Trend
# ==========================================

df['month'] = df['purchase_date'].dt.month

monthly_sales = df.groupby('month')['final_price'].sum()

print("\nMonthly Sales")

print(monthly_sales)

plt.figure(figsize=(10,5))

monthly_sales.plot(marker='o')

plt.title("Monthly Sales Trend")

plt.xlabel("Month")

plt.ylabel("Revenue")

plt.grid()

plt.show()

# ==========================================
# Step 14: Correlation Analysis
# ==========================================

numeric_data = df.select_dtypes(include=np.number)

correlation = numeric_data.corr()

print("\nCorrelation Matrix")

print(correlation)

# Heatmap

import seaborn as sns

plt.figure(figsize=(12,8))

sns.heatmap(
    correlation,
    annot=True,
    cmap='coolwarm'
)

plt.title("Correlation Heatmap")

plt.show()

# ==========================================
# Step 15: Top Selling Products
# ==========================================

top_products = df.groupby(
    'product_id'
)['final_price'].sum()

print("\nTop Products")

print(
top_products.sort_values(
ascending=False
).head(10)
)

# ==========================================
# Step 16: Seller Performance
# ==========================================

seller = df.groupby(
'seller_id'
)['seller_rating'].mean()

print("\nSeller Performance")

print(
seller.sort_values(
ascending=False
)
)

# ==========================================
# Step 17: Insights Summary
# ==========================================

print("\n========= BUSINESS INSIGHTS =========")

print("Total Revenue:", total_revenue)

print("Best Category:",
category_sales.idxmax())

print("Best Brand:",
brand_sales.idxmax())

print("Most Used Device:",
df['device'].mode()[0])

print("Most Common Payment Method:",
df['payment_method'].mode()[0])

print("Highest Sales City:",
location.idxmax())

print("===================================")