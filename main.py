import matplotlib.pyplot as plt
import streamlit as st
from calculator import Calculator as Calc

st.title("Shift Calculator")

if 'inputsReady' not in st.session_state: #state check before creating calculator
    st.session_state.inputsReady = [False, False]
# get date inputs and shit details
col1,col2 = st.columns(2)
with col1:
    start_date = st.date_input("Choose Start date", format= "DD/MM/YYYY")
    days_in = st.number_input("Days In", step=1, min_value=1, max_value=14)
with col2:
    end_date = st.date_input("Choose End date", min_value=start_date,format= "DD/MM/YYYY")
    days_out = st.number_input("Days Out", step=1, min_value=1, max_value=14)

# Define the number of input boxes
cycle_length = days_in+days_out
# Initialize session state for inputs
if 'cycleLen' not in st.session_state:
    st.session_state.cycleLen = [''] * 2
elif 'cycleLen' in st.session_state:
    st.session_state.cycleLen = ['']*cycle_length

# Function to handle form submission
def handle_submit():
    if len(st.session_state.cycleLen) != len(set(st.session_state.cycleLen)):
        st.error("Duplicate date detected, check inputs!")
        return
    st.session_state.inputsReady[0] = True #shift inputs ready

st.header('Shift Names - Enter in sequence')

# Display input boxes
for i in range(len(st.session_state.cycleLen)):
    st.session_state.cycleLen[i] = st.text_input(f'Day {i + 1}', value=st.session_state.cycleLen[i])

# Submit button
if st.button('Submit'):
    st.success("Submitted")
    handle_submit()

outCampDays = st.multiselect("Days Out",options = st.session_state.cycleLen, max_selections=days_out)
if len(outCampDays) == days_out:
    st.session_state.inputsReady[1] = True
    d1shift = st.selectbox("Shift on day 1", options = st.session_state.cycleLen)

if st.session_state.inputsReady:
    if st.button("Create Calculator"):
        st.success("Calculator Created")
        if "calculator" not in st.session_state:
            st.session_state.calculator = Calc(start_date,end_date,days_in,days_out,','.join(st.session_state.cycleLen),",".join(outCampDays),d1shift)
        else:
            st.session_state.calculator = Calc(start_date,end_date,days_in,days_out,','.join(st.session_state.cycleLen),",".join(outCampDays),d1shift)
if "calculator" in st.session_state:
    st.subheader("Calculator")

    queryDate = st.date_input("Choose date", format= "DD/MM/YYYY", min_value=start_date, max_value=end_date)
    if st.button("Shift Query"):
        day, shift = st.session_state.calculator.get_shift_on_date(queryDate)
        st.write(day,shift)

    fromDate = st.date_input("Start date", format="DD/MM/YYYY", min_value=start_date, max_value=end_date)
    if st.button("Calculate Working days"):
        s1, s2, sorted_df = st.session_state.calculator.calc_working_days(fromDate)
        st.subheader(s1)
        inner_labels = list(s2.keys())[1:]
        inner_values = list(s2.values())[1:]
        inner_values[0] -= inner_values[-1]

        #outer label
        outer_labels  = [f"Total ({s2['Total']})"]
        outer_values = [s2["Total"]]
        #update labels
        inner_labels = [f"{label} ({value})" for label, value in zip(inner_labels, inner_values)]

        # Create the nested pie chart
        fig, ax = plt.subplots()

        # Outer pie chart
        ax.pie(
            outer_values,
            labels=outer_labels,
            radius=1,
            startangle=90,
            wedgeprops=dict(width=0.3, edgecolor='w')
        )

        # Inner pie chart
        ax.pie(
            inner_values,
            labels=inner_labels,
            radius=0.7,
            startangle=90,
            wedgeprops=dict(width=0.3, edgecolor='w')
        )

        # Equal aspect ratio ensures the pie is drawn as a circle
        ax.axis('equal')

        st.pyplot(fig)
        st.dataframe(sorted_df,use_container_width=True)








