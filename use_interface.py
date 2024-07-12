import streamlit as st
import xarray as xr
import calendar
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)


# Load dataset
ds = xr.open_dataset('data.nc').sel(expver=1)

# Function to plot data based on selected year and month
def plot_data(year, month):
    selected_date = f'{year}-{month:02d}-01'
    data=ds.skt.sel(time=selected_date).values
    plt.figure(figsize=(10, 5))
    img = plt.imshow(data, cmap='coolwarm', vmin=None, vmax=None, aspect='auto')
    plt.title(f'Temperature Distribution for {selected_date}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.colorbar(img,label='Temperature (°C)')
    plt.grid(True)
    st.pyplot()

# Function to compute statistics (mean, median, std) for selected data range
def compute_statistics(start_year, end_year):
    selected_data = ds.sel(time=slice(f'{start_year}-01-01', f'{end_year}-12-31'))
    mean_data = selected_data.mean(dim='time')
    median_data = selected_data.median(dim='time')
    std_data = selected_data.std(dim='time')
    return mean_data, median_data, std_data

# Streamlit UI
st.title('Climate Data Analysis of Uttarakhand')

# Tab selection for plotting by year and month
tab_selection = st.selectbox('Select Analysis Type', ['Plot by Year and Month', 'Compute Statistics'])

month_to_index = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

if tab_selection == 'Plot by Year and Month':
    st.sidebar.header('Select Year and Month')
    year = st.sidebar.selectbox('Select Year', options=list(range(1950, 2024)))
    month = st.sidebar.selectbox('Select Month', options=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    month_index = month_to_index[month]
    plot_data(year, month_index)

elif tab_selection == 'Compute Statistics':
    st.sidebar.header('Select Year Range')
    start_year = st.sidebar.select_slider('Select Start Year', options=list(range(1950, 2025)))
    end_year = st.sidebar.select_slider('Select End Year', options=list(range(1950, 2025)))
    
    if start_year <= end_year:
        mean_data, median_data, std_data = compute_statistics(start_year, end_year)
        st.subheader('Mean Temperature')
        st.write(mean_data)

        st.subheader('Median Temperature')
        st.write(median_data)

        st.subheader('Standard Deviation of Temperature')
        st.write(std_data)
    else:
        st.error('Please select a valid range of years (Start year should be less than or equal to End year).')

