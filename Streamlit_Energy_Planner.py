import streamlit as st
import matplotlib.pyplot as plt

# Title of the app
st.title("Solar Panel Calculator for Net-Zero Carbon Emissions")

# Sidebar header
st.sidebar.header("Input Parameters")

# Slider and text input for number of solar panels
number_of_panels = st.sidebar.slider(
    "Current number of solar panels:",
    min_value=1,  # Minimum value of 1 panel
    max_value=10_000,  # Maximum value (can be adjusted)
    value=3805,  # Default value
    step=1
)

# Manual input for number of solar panels
number_of_panels_text = st.sidebar.text_input(
    "Or enter the number of solar panels:",
    value=f"{number_of_panels}"
)

# Convert manual input to integer and validate
try:
    number_of_panels_manual = int(number_of_panels_text)
    # Update the slider value based on manual input
    number_of_panels = number_of_panels_manual
except ValueError:
    st.sidebar.warning("Please enter a valid number for solar panels.")

# Add a faint line to separate the sections
st.sidebar.markdown("<hr style='border: 1px solid #ddd;'/>", unsafe_allow_html=True)

# Energy section
st.sidebar.write("### Energy Production Parameters")
energy_unit = st.sidebar.selectbox(
    "Select the unit for energy production:",
    ["kWh", "MWh", "GWh"]
)

# Define maximum values based on units
max_energy = {
    "kWh": 1_000_000.0,
    "MWh": 1_000.0,
    "GWh": 1.0
}

# Slider and text input for energy production
total_energy_production = st.sidebar.slider(
    f"Total energy produced ({energy_unit}):",
    min_value=0.0,
    max_value=max_energy[energy_unit],
    value=50_000.0 if energy_unit == "kWh" else (50.0 if energy_unit == "MWh" else 0.05),
    step=0.01
)

# Manual input for energy production
total_energy_production_text = st.sidebar.text_input(
    f"Or enter the total energy produced ({energy_unit}):",
    value=f"{total_energy_production:.2f}"
)

# Convert manual input to float and validate
try:
    total_energy_production_manual = float(total_energy_production_text)
    # Update the slider value based on manual input
    total_energy_production = total_energy_production_manual
except ValueError:
    st.sidebar.warning("Please enter a valid number for energy production.")

# Add a faint line to separate the sections
st.sidebar.markdown("<hr style='border: 1px solid #ddd;'/>", unsafe_allow_html=True)

# Carbon emissions section
st.sidebar.write("### Carbon Emissions Parameters")
carbon_unit = st.sidebar.selectbox(
    "Select the unit for carbon emissions:",
    ["kg CO₂", "tons CO₂"]
)

GRID_EMISSION_FACTOR = 0.417

# Define maximum values based on units
max_carbon_emissions = {
    "kg CO₂": 10_000_000.0,
    "tons CO₂": 10_000.0
}

# Slider and text input for carbon emissions
total_carbon_emissions = st.sidebar.slider(
    f"Current total carbon emissions ({carbon_unit}):",
    min_value=0.0,
    max_value=max_carbon_emissions[carbon_unit],
    value=500_000.0 if carbon_unit == "kg CO₂" else 500.0,
    step=0.01
)

# Manual input for carbon emissions
total_carbon_emissions_text = st.sidebar.text_input(
    f"Or enter the current total carbon emissions ({carbon_unit}):",
    value=f"{total_carbon_emissions:.2f}"
)

# Convert manual input to float and validate
try:
    total_carbon_emissions_manual = float(total_carbon_emissions_text)
    # Update the slider value based on manual input
    total_carbon_emissions = total_carbon_emissions_manual
except ValueError:
    st.sidebar.warning("Please enter a valid number for carbon emissions.")

# Convert energy to kWh and carbon emissions to kg CO₂
if energy_unit == "MWh":
    total_energy_production_kWh = total_energy_production * 1_000
elif energy_unit == "GWh":
    total_energy_production_kWh = total_energy_production * 1_000_000
else:
    total_energy_production_kWh = total_energy_production

if carbon_unit == "tons CO₂":
    total_carbon_emissions_kg = total_carbon_emissions * 1_000
else:
    total_carbon_emissions_kg = total_carbon_emissions

# Calculate button
if st.button("Calculate"):
    if total_energy_production_kWh > 0:
        # Calculate the total amount of carbon offset by current solar panels
        carbon_offset_from_current_panels = total_energy_production_kWh * GRID_EMISSION_FACTOR
        
        # Calculate the remaining carbon emissions that need to be offset
        remaining_carbon_emissions = total_carbon_emissions_kg - carbon_offset_from_current_panels
        
        # Calculate the additional energy needed to offset the remaining carbon emissions
        additional_energy_needed = remaining_carbon_emissions / GRID_EMISSION_FACTOR
        
        # Calculate the number of additional panels needed to produce the additional energy
        energy_per_panel = total_energy_production_kWh / number_of_panels
        additional_panels_needed = additional_energy_needed / energy_per_panel
        
        # Check if net-zero carbon emissions are reached
        if additional_panels_needed <= 0:
            st.markdown("<p style='font-size: 20px; color: green;'>Net-Zero Carbon Emissions reached</p>", unsafe_allow_html=True)
            remaining_carbon_emissions = 0  # No remaining emissions
        else:
            # Format numbers with commas
            carbon_offset_from_current_panels_formatted = f"{carbon_offset_from_current_panels:,.2f}"
            remaining_carbon_emissions_formatted = f"{remaining_carbon_emissions:,.2f}"
            additional_energy_needed_formatted = f"{additional_energy_needed:,.2f}"
            additional_panels_needed_formatted = f"{additional_panels_needed:,.0f}"
            
            # Display results with adjustable text size
            st.markdown(f"<p style='font-size: 23px;'><strong>Total carbon offset from current {number_of_panels} panels:</strong> <b>{carbon_offset_from_current_panels_formatted} kg CO₂</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 23px;'><strong>Remaining carbon emissions to offset:</strong> <b>{remaining_carbon_emissions_formatted} kg CO₂</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 23px;'><strong>Additional energy needed to offset remaining emissions:</strong> <b>{additional_energy_needed_formatted} kWh</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 23px;'><strong>Additional solar panels needed:</strong> <b>{additional_panels_needed_formatted}</b></p>", unsafe_allow_html=True)
        
        # Add a faint line above the pie chart
        st.markdown("<hr style='border: 1px solid #ddd;'/>", unsafe_allow_html=True)
        
        # Plot pie chart with title
        fig, ax = plt.subplots(figsize=(8, 6))  # Adjust the figsize here
        labels = ['Carbon Offset', 'Remaining Emissions']
        sizes = [carbon_offset_from_current_panels, remaining_carbon_emissions]
        colors = ['#ff9999','#66b3ff']
        explode = (0.1, 0)  # explode 1st slice

        wedges, texts, autotexts = ax.pie(
            sizes, explode=explode, labels=labels, colors=colors,
            autopct=lambda p: '{:.1f}%'.format(p),  # Format percentage
            shadow=True, startangle=140, 
            textprops={'fontsize': 13, 'fontweight': 'bold'}  # Bold labels
        )
        
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        # Add title to pie chart with specific font properties
        ax.set_title('Carbon Offset vs. Remaining Emissions', fontsize=20, fontweight='bold')

        # Adjust percentage font size and make it bold
        for autotext in autotexts:
            autotext.set_fontsize(16)
            autotext.set_fontweight('bold')

        # Adjust label font size and make it bold
        for text in texts:
            text.set_fontsize(16)
            text.set_fontweight('bold')

        st.pyplot(fig)
    else:
        st.error("Total energy production must be greater than zero.")
