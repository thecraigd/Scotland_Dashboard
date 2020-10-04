import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk

# Title - The title and introductory text and images are all written in Markdown format here, using st.write()
st.title('Scotland Covid-19 Dashboard')

st.write("""
[![craigdoesdata logo][logo]][link]
[logo]: https://www.craigdoesdata.de/img/logo/logo_w_sm.gif
[link]: https://www.craigdoesdata.de/


------------

This dashboard provides the latest information about the Covid 19 situation in Scotland.

The data are the latest official figures provided by the Scottish government, sourced from [statistics.gov.scot](https://statistics.gov.scot/resource?uri=http%3A%2F%2Fstatistics.gov.scot%2Fdata%2Fcoronavirus-covid-19-management-information).

The default view is the number of positive cases in the last 7 days ([running total](https://en.wikipedia.org/wiki/Running_total)), showing the last 14 days of data. Other options can be selected in the sidebar on the left.

If you are viewing this on a mobile device, tap **>** in the top left corner to select options.
""")
st.write("---")

####################################
# Getting Data

def get_data():
    data_url = 'https://statistics.gov.scot/downloads/cube-table?uri=http%3A%2F%2Fstatistics.gov.scot%2Fdata%2Fcoronavirus-covid-19-management-information'
    data = pd.read_csv(data_url, sep=',', encoding = 'unicode_escape')

    return data

data_df = get_data()

data_df = data_df.sort_values(by=['DateCode']) # sorting the df in place by date


data_df = data_df[data_df['Value'] != '*']
data_df['Date'] = pd.to_datetime(data_df['DateCode'])
data_df['Value'] = pd.to_numeric(data_df['Value'])


####################################
# Selecting Data to Display - User entry

categories = data_df.Units.unique()
categories = sorted(categories)

category = st.sidebar.selectbox('Select data to display:', categories, index=33)



# Creating a slider on the sidebar to adjust dates
days_to_show = st.sidebar.slider(
    'Number of days to display:',
    0, 100, 14
)

# Creating a Checkbox in the sidebar to turn off the mplcyberpunk style
st.sidebar.write('---')
st.sidebar.write('Chart Presentation Settings:')
nocyber = st.sidebar.checkbox('Light Style')
lockaxis = st.sidebar.checkbox('Lock y-axis at 0 (makes absolute values clearer)')


####################################
# Manipulating Data based on User Input

selected_data = data_df[data_df['Units'] == category]

data_for_display = selected_data.iloc[-days_to_show:,:]



####################################
# Output - Producing the plots

# Selecting the style for the plots
if nocyber == False:
    plt.style.use('cyberpunk')
else:
    plt.style.use('ggplot')

st.header(category)

# Defining the figure 
fig, ax = plt.subplots()

plt.plot(data_for_display['Date'], data_for_display['Value'])

plt.xticks(rotation=45, 
    horizontalalignment='right',
    fontweight='normal',
    fontsize='small',
    color= '1')
plt.yticks(color = '1')

#Locking the y-axis at zero if selected
if lockaxis == True:
    plt.ylim((0))

# Removing the mplcyberpunk glow effects if checkbox selected
if nocyber == False:
    mplcyberpunk.add_glow_effects()

# Displaying the plot and the last 3 days' values
st.pyplot(fig)
table = data_for_display.iloc[-3:,:]
table = table.drop(['FeatureCode', 'Measurement', 'Variable', 'Date'], axis=1)
st.table(table)

st.write('---')














st.write('''
    Dashboard created by [Craig Dickson](https://www.craigdoesdata.de), with [Streamlit](https://www.streamlit.io).
    See the code on [GitHub](https://github.com/thecraigd/Scotland_Covid_Dashboard).

    I have made every effort to ensure the accuracy and reliability of the information on this dashboard. However, the information is provided "as is" without warranty of any kind.
''')