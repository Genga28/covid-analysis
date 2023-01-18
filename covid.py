# @Email:  contact@pythonandvba.com
# @Website:  https://pythonandvba.com
# @YouTube:  https://youtube.com/c/CodingIsFun
# @Project:  Sales Dashboard w/ Streamlit



import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Covid Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="covid.xlsx",
        engine="openpyxl",
        sheet_name="covid",
        skiprows=0,
        usecols="A:I",
        nrows=36570,
    )
    # Add 'hour' column to dataframe
    #f["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
country = st.sidebar.multiselect(
    "Select the Country:",
    options=df["Country"].unique()
)

date = st.sidebar.multiselect(
    "Select the Date:",
    options=df["Date"].unique(),
    
)

df_selection = df.query(
    "Country == @country & Date == @date"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Covid Dashboard")
st.markdown("##")

# TOP KPI's
total_confirmed_cases = int(df_selection["Confirmed"].sum())
average_deaths = round(df_selection["Deaths"].mean(), 1)

average_death_per_country = round(df_selection["Deaths"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Covid Cases:")
    st.subheader(f"US $ {total_confirmed_cases:,}")
with middle_column:
    st.subheader("Average Cases:")
    st.subheader(f"{average_deaths}")
with right_column:
    st.subheader("Average ases per Day:")
    st.subheader(f"US $ {average_death_per_country}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
death_by_country = (
    df_selection.groupby(by=["Country"]).sum()[["Deaths"]].sort_values(by="Deaths")
)
fig_death_country = px.bar(
    death_by_country,
    x="Deaths",
    y=death_by_country.index,
    orientation="h",
    title="<b>Deaths by Country</b>",
    color_discrete_sequence=["#0083B8"] * len(death_by_country),
    template="plotly_white",
)
fig_death_country.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [BAR CHART]
confirmed_cases_per_country = df_selection.groupby(by=["Country"]).sum()[["Confirmed"]]
fig_cases_country = px.bar(
    confirmed_cases_per_country,
    x=confirmed_cases_per_country.index,
    y="Confirmed",
    title="<b>Cases by Country</b>",
    color_discrete_sequence=["#0083B8"] * len(confirmed_cases_per_country),
    template="plotly_white",
)
fig_cases_country.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_death_country, use_container_width=True)
right_column.plotly_chart(fig_cases_country, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
