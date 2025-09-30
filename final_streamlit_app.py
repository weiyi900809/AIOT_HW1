
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

st.set_page_config(page_title="Interactive Linear Regression Visualizer", layout="wide")

st.title("HW1-1: Interactive Linear Regression Visualizer")

# Sidebar for user inputs
st.sidebar.header("Configuration")

# Data Generation Parameters
n_points = st.sidebar.slider("Number of data points (n)", 100, 1000, 500)
coefficient_a = st.sidebar.slider("Coefficient 'a' (y = ax + b + noise)", -10.0, 10.0, 2.0, 0.1)
coefficient_b = st.sidebar.slider("Intercept 'b' (y = ax + b + noise)", -10.0, 10.0, 5.0, 0.1)
noise_variance = st.sidebar.slider("Noise Variance (var)", 0, 1000, 100)

# Option to change random seed for different data patterns
use_random_seed = st.sidebar.checkbox("Use random seed (42) for reproducibility", value=True)
if use_random_seed:
    np.random.seed(42)

# Generate data
x = np.random.rand(n_points) * 10
y_true = coefficient_a * x + coefficient_b
noise = np.random.normal(0, np.sqrt(noise_variance), n_points)
y = y_true + noise

# Create a DataFrame for easier handling
df = pd.DataFrame({'x': x, 'y': y})

st.subheader("Generated Data and Linear Regression")

# Perform Linear Regression
model = LinearRegression()
model.fit(x.reshape(-1, 1), y)

# Generate predictions for a smooth regression line
x_sorted = np.sort(x)
y_pred_sorted = model.predict(x_sorted.reshape(-1, 1))

# Calculate residuals for outlier detection
y_pred = model.predict(x.reshape(-1, 1))
residuals = np.abs(y - y_pred)
df['residuals'] = residuals

# Identify top 5 outliers
outliers = df.nlargest(5, 'residuals')

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot data points
ax.scatter(df['x'], df['y'], label='Generated Data', alpha=0.6, s=30, color='skyblue')

# Plot regression line in red
ax.plot(x_sorted, y_pred_sorted, color='red', label='Linear Regression Line', linewidth=3)

# Highlight and label outliers
colors = ['purple', 'orange', 'green', 'brown', 'pink']  # Different colors for each outlier
for i, (idx, row) in enumerate(outliers.iterrows()):
    color = colors[i % len(colors)]
    ax.scatter(row['x'], row['y'], color=color, s=150, edgecolors='black', 
              linewidth=2, zorder=5)
    ax.annotate(f'Outlier {i+1}', (row['x'], row['y']), 
               textcoords="offset points", xytext=(10, 10), 
               ha='center', color=color, fontweight='bold', fontsize=10,
               bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

ax.set_xlabel("X", fontsize=14)
ax.set_ylabel("Y", fontsize=14)
ax.set_title("Linear Regression with Top 5 Outliers Highlighted", fontsize=16)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# Display model information
col1, col2 = st.columns(2)

with col1:
    st.subheader("Model Coefficients")
    st.metric("Coefficient (a)", f"{model.coef_[0]:.4f}")
    st.metric("Intercept (b)", f"{model.intercept_:.4f}")

    # Show true vs estimated parameters
    st.write("**True vs Estimated Parameters:**")
    st.write(f"True a: {coefficient_a:.4f} | Estimated a: {model.coef_[0]:.4f}")
    st.write(f"True b: {coefficient_b:.4f} | Estimated b: {model.intercept_:.4f}")

    # Parameter differences
    diff_a = abs(coefficient_a - model.coef_[0])
    diff_b = abs(coefficient_b - model.intercept_)
    st.write(f"Difference in a: {diff_a:.4f}")
    st.write(f"Difference in b: {diff_b:.4f}")

with col2:
    st.subheader("Model Statistics")
    # Calculate R-squared and other metrics
    r2 = r2_score(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)

    st.metric("R-squared", f"{r2:.4f}")
    st.metric("Mean Squared Error", f"{mse:.4f}")
    st.metric("Root Mean Squared Error", f"{rmse:.4f}")
    st.metric("Standard Deviation of Residuals", f"{np.std(residuals):.4f}")

# Display outliers table
st.subheader("Top 5 Outliers")
outliers_display = outliers[['x', 'y', 'residuals']].copy()
outliers_display.columns = ['X Value', 'Y Value', 'Distance from Regression Line']
outliers_display = outliers_display.round(4)
outliers_display.index = [f"Outlier {i+1}" for i in range(len(outliers_display))]
st.dataframe(outliers_display, use_container_width=True)

# Additional information section
st.subheader("Data Generation Information")
st.latex(r"y = ax + b + \varepsilon")
st.write("Where:")
st.write(f"- **a** (coefficient): {coefficient_a}")
st.write(f"- **b** (intercept): {coefficient_b}")
st.write(f"- **ε** (noise): Normal distribution N(0, σ²) where σ² = {noise_variance}")
st.write(f"- **n** (data points): {n_points}")

# Show data distribution info
st.subheader("Data Distribution Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.write(f"**X values:**")
    st.write(f"Min: {x.min():.4f}")
    st.write(f"Max: {x.max():.4f}")
    st.write(f"Mean: {x.mean():.4f}")

with col2:
    st.write(f"**Y values:**")
    st.write(f"Min: {y.min():.4f}")
    st.write(f"Max: {y.max():.4f}")
    st.write(f"Mean: {y.mean():.4f}")

with col3:
    st.write(f"**Residuals:**")
    st.write(f"Min: {residuals.min():.4f}")
    st.write(f"Max: {residuals.max():.4f}")
    st.write(f"Mean: {residuals.mean():.4f}")

# Instructions for running the app
st.sidebar.markdown("---")
st.sidebar.subheader("How to Use")
st.sidebar.write("1. Adjust the parameters using the sliders")
st.sidebar.write("2. The plot will update automatically")
st.sidebar.write("3. Observe how changes affect the regression line and outliers")
st.sidebar.write("4. Compare true vs estimated parameters")
