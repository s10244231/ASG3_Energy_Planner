import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Title of the app
st.title("Solar Panel Calculator for Zero Carbon Footprint")

# Input fields
current_carbon_emissions = st.number_input("Enter your current annual carbon emissions (kg CO2):", min_value=0.0)
energy_per_panel = st.number_input("Enter the energy produced per solar panel per year (kWh):", min_value=0.0)
cost_per_panel = st.number_input("Enter the cost per solar panel ($):", min_value=0.0)

# Default values
grid_emission_factor = 0.417
cost_per_kwh = 0.267

# Calculate button
if st.button("Calculate"):
    # Calculate carbon offset per panel
    carbon_offset_per_panel = energy_per_panel * grid_emission_factor
    
    # Calculate number of panels needed
    number_of_panels_needed = current_carbon_emissions / carbon_offset_per_panel
    
    # Calculate total cost
    total_installation_cost = number_of_panels_needed * cost_per_panel
    
    # Calculate potential savings
    potential_savings = number_of_panels_needed * energy_per_panel * cost_per_kwh
    
    # Display results
    st.write(f"Number of solar panels needed to achieve zero carbon footprint: {number_of_panels_needed:.0f}")
    st.write(f"Total installation cost: ${total_installation_cost:.2f}")
    st.write(f"Potential savings on electricity: ${potential_savings:.2f}")
