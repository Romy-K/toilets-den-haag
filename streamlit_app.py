
import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pydeck as pdk
import plotly.express as px
from simulation import simulate_10_year_plan 

# ----------------------------
# CONFIG & TITLE
# ----------------------------
st.set_page_config(page_title="Den Haag: Toilets for Seniors", layout="centered")
st.markdown("<h1 style='font-size: 42px; font-weight: 400; color: grey;'>Public Toilets for Seniors in Den Haag</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 29px; font-style: italic; color: darkgrey'>When you lack toilets, you miss spending</p>", unsafe_allow_html=True)


# ----------------------------
# TAB NAMES (for consistent use across radio and content)
# ----------------------------
TAB_NAMES = ["Hello", "Facts", "1-Year Simulation", "10-Year Simulation", "Recommendations"]

if "current_selected_tab_name" in st.session_state and st.session_state.current_selected_tab_name not in TAB_NAMES:
    del st.session_state.current_selected_tab_name


# ----------------------------
# Initialize Session State for Controls
# ----------------------------
if "current_selected_tab_name" not in st.session_state:
    st.session_state.current_selected_tab_name = TAB_NAMES[0] # Default to 'Hello'

if "tab3_toilet_slider" not in st.session_state:
    st.session_state.tab3_toilet_slider = 67 # Default value for the slider

# Purge any old, unused session state keys that might conflict
# Keeping this clean-up for robustness, though debugging showed there are no more issues.
for key in ["active_tab", "temp_tab_selection_bug_fix", "toilet_count_sidebar_value", "tab_3_toilet_slider"]:
    if key in st.session_state:
        del st.session_state[key]
        
# ----------------------------
# GLOBAL DATA LOADING FROM SQL
# ----------------------------
@st.cache_data
def load_all_data():
    username = st.secrets["username"]
    password = st.secrets["password"]
    host = st.secrets["host"]
    database = st.secrets["database"]

    connection_string = f"mysql+pymysql://{username}:{password}@{host}/{database}"
    engine = create_engine(connection_string)

    scenarios = pd.read_sql("SELECT * FROM city_scenarios_all", con=engine)
    toilets = pd.read_sql("SELECT * FROM dh_toilets", con=engine)
    dh_seniors = pd.read_sql("SELECT * FROM dh_seniors", con=engine)
    return scenarios, toilets, dh_seniors

scenarios, current_toilets, dh_seniors = load_all_data()

# ----------------------------
# CALLBACK FUNCTION FOR RADIO BUTTON
# ----------------------------
def update_tab_selection():
    # This function is called when the 'main_tab_selector_radio' changes.
    # The value of the widget is available via st.session_state[widget_key].
    st.session_state.current_selected_tab_name = st.session_state.main_tab_selector_radio

# ----------------------------
# Conditional Sidebar Content
# ----------------------------
if st.session_state.current_selected_tab_name == "1-Year Simulation":
    st.sidebar.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div style='font-size: 28px; font-weight: 500;'>New toilet: €200.000</div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("<div style='font-size: 28px; font-weight: 500;'>Toilet count</div>", unsafe_allow_html=True)

    st.sidebar.slider(
        "",
        min_value=67,
        max_value=330,
        key="tab3_toilet_slider" # Unique key for this slider
    )

# ----------------------------
# PRIMARY NAVIGATION: Use st.radio for robust state management with callback
# ----------------------------
current_tab_index = TAB_NAMES.index(st.session_state.current_selected_tab_name)

st.radio(
    "",
    TAB_NAMES,
    index=current_tab_index,
    key="main_tab_selector_radio", # The key is crucial for on_change
    horizontal=True,
    on_change=update_tab_selection # Call our callback when the radio value changes
)

# ----------------------------
# CONTENT RENDERING based on `current_selected_tab_name`
# ----------------------------
# ============================================================================================================================== HELLO

if st.session_state.current_selected_tab_name == "Hello":
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    st.image("https://www.denhaag.nl/wp-content/uploads/2022/04/f46d406e-7a4d-4007-9071-e9ce4e288c5f_image4438220217146858732.jpg")
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 36px; font-weight: 600;'>Den Haag Toilet Policy: A Jumping-Off Point</div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    image_url = ("https://denhaag.groenlinks.nl/sites/groenlinks/files/styles/video_big/public/newsarticle/image/Openbare%20wc%20Buitenhof%20Foto%20app.ongehinderd.nl_.jpg?h=7652de0f&itok=W0B4_n_m")
    st.image(image_url)
    st.write("By Romy Koreman")
# ============================================================================================================================== FACTS
elif st.session_state.current_selected_tab_name == "Facts":
    st.markdown("<div style='font-size: 40px; font-weight: 600;'>Facts & Figures</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([56,22])
    # Styles
    label_style = "font-size: 36px; line-height: 2;"
    value_style = "font-size: 36px; line-height: 2; font-weight: 600;"

    # Column 1 — Labels
    col1.markdown(f"<div style='{label_style}'>Annual senior outings in NL</div>", unsafe_allow_html=True)
    col1.markdown(f"<div style='{label_style}'>Average spend per senior outing</div>", unsafe_allow_html=True)
    col1.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    col1.markdown(f"<div style='{label_style}'>Seniors <b>regularly</b> skip outings</div>", unsafe_allow_html=True)
    col1.markdown(f"<div style='{label_style}'>Seniors <b>sometimes</b> skip outings</div>", unsafe_allow_html=True)
    col1.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    col1.markdown(f"<div style='{label_style}'>Senior population of Den Haag</div>", unsafe_allow_html=True)
    col1.markdown(f"<div style='{label_style}'>Current toilet density Den Haag</div>", unsafe_allow_html=True)
    col1.markdown(f"<div style='{label_style}'>Toilet Utopia</div>", unsafe_allow_html=True)
    
    # Column 2 — Values
    col2.markdown(f"<div style='{value_style}'>575 million</div>", unsafe_allow_html=True)
    col2.markdown(f"<div style='{value_style}'>€ 22,-</div>", unsafe_allow_html=True)
    col2.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    col2.markdown(f"<div style='{value_style}'>11 %</div>", unsafe_allow_html=True)
    col2.markdown(f"<div style='{value_style}'>39 %</div>", unsafe_allow_html=True)
    col2.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    col2.markdown(f"<div style='{value_style}'>86 thousand</div>", unsafe_allow_html=True)
    col2.markdown(f"<div style='{value_style}'>0.81 / km2</div>", unsafe_allow_html=True)
    col2.markdown(f"<div style='{value_style}'>4 / km2</div>", unsafe_allow_html=True)
# ========================================================================================================================== 1-YEAR SIMULATION
elif st.session_state.current_selected_tab_name == "1-Year Simulation":
    st.markdown("<div style='font-size: 40px; font-weight: 600;'>Toilet Simulation: 1-Year Results</div>", unsafe_allow_html=True)

    # Use the value from the sidebar slider stored in session_state
    toilet_count = st.session_state.tab3_toilet_slider

    # Filter scenario based on the slider value
    scenario = scenarios[scenarios["toilets"] == toilet_count].squeeze()

    # Derived values
    baseline_scenario = scenarios[scenarios["toilets"] == 67].squeeze()
    extra_outings = baseline_scenario["missed_outings"] - scenario["missed_outings"]
    extra_spending = extra_outings * 22

    net_gain = scenario["net_gain_eur"]
    net_gain_color = "green" if net_gain >= 0 else "red"

    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

    # ---- Row 1: What changed ----
    st.markdown("<h3 style='font-size: 30px; font-weight: 300; font-style: italic; color: grey;'>Changes from Baseline</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div style='font-size: 28px; font-weight: 600;'>Toilets Added</div>", unsafe_allow_html=True)
    col1.markdown(f"<div style='font-size: 34px;'>{toilet_count - 67}</div>", unsafe_allow_html=True)

    col2.markdown(f"<div style='font-size: 28px; font-weight: 600;'>Extra Outings</div>", unsafe_allow_html=True)
    col2.markdown(f"<div style='font-size: 34px;'>{extra_outings:,.0f}</div>", unsafe_allow_html=True)

    col3.markdown(f"<div style='font-size: 28px; font-weight: 600;'>Extra Spending (€)</div>", unsafe_allow_html=True)
    col3.markdown(f"<div style='font-size: 34px;'>{extra_spending:,.0f}</div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

    # ---- Row 2: Outcome ----
    st.markdown("<h3 style='font-size: 30px; font-weight: 300; font-style: italic; color: grey;'>Outcome</h3>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)

    col4.markdown(f"<div style='font-size: 28px; font-weight: 600;'>Missed Outings</div>", unsafe_allow_html=True)
    col4.markdown(f"<div style='font-size: 34px;'>{scenario['missed_outings']:,.0f}</div>", unsafe_allow_html=True)

    col5.markdown(f"<div style='font-size: 28px; font-weight: 600;'>Cost of Toilets (€)</div>", unsafe_allow_html=True)
    col5.markdown(f"<div style='font-size: 34px;'>{scenario['cost_new_toilets_eur']:,.0f}</div>", unsafe_allow_html=True)

    col6.markdown(
        f"""<div style='font-size: 30px; font-weight: 600;'>Net Result (€)</div>
            <div style='font-size: 44px; font-weight: 700; color: {net_gain_color};'>
            {net_gain:,.0f}
            </div>""",
        unsafe_allow_html=True
    )

    # Get toilet map
    def generate_fake_toilets(n, seed=42):
        np.random.seed(seed)
        lat = np.random.uniform(52.05, 52.11, n)
        lon = np.random.uniform(4.25, 4.36, n)
        return pd.DataFrame({"lat": lat, "lon": lon, "type": "simulated"})

    extra_toilets = toilet_count - current_toilets.shape[0]
    print(f"Extra toilets to generate: {extra_toilets}")
    simulated = generate_fake_toilets(extra_toilets) if extra_toilets > 0 else pd.DataFrame(columns=["lat", "lon", "type"])
    current_toilets["type"] = "existing"
    map_df = pd.concat([current_toilets[["lat", "lon", "type"]], simulated], ignore_index=True)
    color_map = {"existing": [255, 0, 0], "simulated": [65, 62, 222]}
    map_df["color"] = map_df["type"].map(color_map)

    layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_df,
    get_position='[lon, lat]',
    get_radius=45,
    get_fill_color='color',
    pickable=True,
    )
    view_state = pdk.ViewState(
    latitude=52.08,
    longitude=4.32,
    zoom=11.75,
    pitch=0,
    )
    deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/streets-v11",
    )
    st.pydeck_chart(deck)

    # Add hidden sigmoid illustration
    with st.expander("Sigmoid illustration"):
    
        fig = px.line(
                scenarios,
                x="toilets",
                y="net_gain_eur",
                title="Net Result (€) by Total Toilets",
                labels={"toilets": "Total Toilets in Scenario", "net_gain_eur": "Scenario Net Result (€)"},
                markers=True # Adds dots at each data point
            )
    
            # Highlight the currently selected toilet count from the slider
        fig.add_scatter(
                x=[toilet_count],
                y=[scenario["net_gain_eur"]],
                mode='markers',
                marker=dict(size=15, color='red', symbol='star', line=dict(width=2, color='DarkSlateGrey')),
                name=f'Current Selection: {toilet_count} Toilets',
                hovertemplate=f'<b>Current Selection</b><br>Toilets: {toilet_count}<br>Scenario Net Gain: {scenario["net_gain_eur"]:.2f}€<extra></extra>'
            )
    
        fig.update_layout(hovermode="x unified") # Improves hover experience
    
        st.plotly_chart(fig, use_container_width=True)
# ========================================================================================================================== 10-YEAR SIMULATION
elif st.session_state.current_selected_tab_name == "10-Year Simulation":
    st.markdown("<div style='font-size: 40px; font-weight: 600;'>10-Year Toilet Simulation (2025–2034)</div>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size: 24px; font-weight: 500;'>Number of toilets to add per year</h3>", unsafe_allow_html=True)
    toilets_per_year = st.slider("", 1, 26, 1)

    starting_toilets = 67
    sim_df = simulate_10_year_plan(starting_toilets, toilets_per_year, scenarios, dh_seniors)

    # Get graph
    fig = px.line(sim_df, x="year", y=["net_gain_eur"],
                    height=550,
                    labels={
                        "value": "Euros (€)",
                        "variable": "Metric",
                        "year": "Year"
                    },
                    title="Yearly Result")
    fig.update_traces(mode="lines+markers",
                     hovertemplate=(
        "<span style='font-size: 20px;'>Year: <b>%{x}</b></span><br>" + 
        "<span style='font-size: 20px;'>Result: <b>€%{y:,.0f}</b></span><extra></extra>")
                     )
    fig.update_layout(
    title={
        "text": "Yearly Result",
        "font": {"size": 28}
    },
    # axis font sizes
    xaxis=dict(
        tickfont=dict(size=16, family="Source Sans Pro, sans-serif", color="black"), # Adjust x-axis numbers (years)
        title_font=dict(size=20, family="Source Sans Pro, sans-serif", color="black", weight="bold"), # Adjust x-axis title ('Year')
    ),
    yaxis=dict(
        tickfont=dict(size=18, family="Source Sans Pro, sans-serif", color="black"), # Adjust y-axis numbers (euros)
        title_font=dict(size=20, family="Source Sans Pro, sans-serif", color="black", weight="bold"), # Adjust y-axis title ('Euros (€)')
        tickformat="€~s",
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor="gray"
    ),
    showlegend=False) # no need
    
    st.plotly_chart(fig, use_container_width=True)

    # Show cumulative results under annual results graph 
    st.markdown("### Cumulative Totals")

    cumulative_cost = sim_df["cumulative_toilet_cost_eur"].iloc[-1]
    cumulative_gain = sim_df["cum_gain_eur"].iloc[-1]

    # Define net_gain_color for cumulative gain
    net_gain_color_10year = "green" if cumulative_gain >= 0 else "red"
                         
    col1, col2 = st.columns(2)
    col1.metric("Cumulative Toilet Costs (10y)", f"€{cumulative_cost:,.0f}")
    col2.markdown(
        f"""
        <div style='font-size: 24px; font-weight: 600;'>Cumulative Net Result (10y)</div>
        <div style='font-size: 38px; font-weight: 700; color: {net_gain_color_10year};'>
        €{cumulative_gain:,.0f}
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
    
    # Detailed table for extra info 
    with st.expander("View Detailed Table"):
        display_df = sim_df[["year", "total_toilets", "seniors", "missed_outings",
                     "additional_senior_spending_eur", "cost_new_toilets_eur",
                     "net_gain_eur", "cumulative_toilet_cost_eur", "cum_gain_eur"]].copy()

        display_df.columns = ["Year", "Toilets", "Seniors", "Missed Outings",
                      "Extra Spending (€)", 
                      "Toilet Cost (€)",
                      "Net Result (€)", "Cumulative Toilet Cost (€)", "Cumulative Net Result (€)"]

    # Rounding the numbers w/ a dictionary
    
        format_dict = {
            "Year": "{:.0f}",              # No decimals, thousands separator
            "Toilets": "{:,.0f}",           # No decimals, thousands separator
            "Seniors": "{:,.0f}",           # No decimals, thousands separator
            "Missed Outings": "{:,.0f}",    # No decimals, thousands separator
            "Extra Spending (€)": "€{:,.0f}", # No decimals, thousands separator, with Euro symbol
            "Toilet Cost (€)": "€{:,.0f}",   # No decimals, thousands separator, with Euro symbol
            "Net Result (€)": "€{:,.0f}",    # No decimals, thousands separator, with Euro symbol
            "Cumulative Toilet Cost (€)": "€{:,.0f}", # No decimals, thousands separator, with Euro symbol
            "Cumulative Net Result (€)": "€{:,.0f}" # No decimals, thousands separator, with Euro symbol
            } 
        st.dataframe(display_df.style.format(format_dict))
# ============================================================================================================================ RECOMMENDATIONS
elif st.session_state.current_selected_tab_name == "Recommendations":
    st.markdown("<div style='font-size: 42px; font-weight: 600;'>Recommendations & Further Use</div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div>
        <ul>
            <li style="font-size: 38px;">Money spent in city ≠ money for city</li>
            <li style="font-size: 38px;">Are toilets free?</li>
            <li style="font-size: 38px;">Toilet placement</li>
            <li style="font-size: 38px;">Not just seniors!</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)