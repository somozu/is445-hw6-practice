import streamlit as st
import altair as alt

bfro_url = 'https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/bfro_reports_fall2022.csv'

st.set_page_config(
    page_title="IS445 BFRO Viz", 
    page_icon="🫈",
    layout="wide",
)

st.title('Bigfoot Field Researchers Organization Data Visualizations')


chart1 = alt.Chart(bfro_url).mark_rect().encode(
    alt.X('season:N', axis=alt.Axis(title='Season', labelAngle=0), sort=['Spring', 'Summer', 'Fall', 'Winter']),
    alt.Y('state:N', axis=alt.Axis(title='State', labelOverlap=False)),
    alt.Color('count()', scale=alt.Scale(scheme='blues'),
              legend=alt.Legend(title='Number of Reports'))
).transform_filter(
    alt.datum.season != 'Unknown'
).properties(
    width=300,
    height=750
)



brush = alt.selection_interval(encodings=['x'])


scatter = alt.Chart(bfro_url).mark_circle(opacity=0.7).encode(
    alt.X('date:T', axis=alt.Axis(title='Year of Report')),
    alt.Y('temperature_mid:Q', axis=alt.Axis(title='Daily Median Temperature (°F)')),
    color=alt.Color('season:N', scale=alt.Scale(domain=['Spring', 'Summer', 'Fall', 'Winter'],
                                                range=['green', 'yellow', 'orange', 'blue']))
).transform_filter(
    (alt.datum.season != 'Unknown') & (alt.expr.isValid(alt.datum.temperature_mid)) & (alt.datum.temperature_mid > 0)
).properties(
    height=350
).add_params(
    brush
)

bar = alt.Chart(bfro_url).mark_bar().encode(
    alt.X('count()', axis=alt.Axis(title='Number of Reports')),
    alt.Y('season:N', sort=['Spring', 'Summer', 'Fall', 'Winter']),
    color=alt.Color('season:N',
                    scale=alt.Scale(domain=['Spring', 'Summer', 'Fall', 'Winter'],
                                    range=['green', 'yellow', 'orange', 'blue']))
).transform_filter(
    (alt.datum.season != 'Unknown') & (alt.expr.isValid(alt.datum.temperature_mid)) & (alt.datum.temperature_mid > 0)
).transform_filter(
    brush
).properties(
    height=350
)

chart2 = (scatter.properties(width=550) | bar.properties(width=400))




st.header("Reports by State and Season")
st.altair_chart(chart1)
st.write(""" 
In the first visualization, I chose to display the US state and season in which the bigfoot reports are from in a heatmap
based on the amount of reports. This was for the purpose of showing patterns on when sightings are recorded, which can
give insight into when people in different states are likeliest to spot bigfoot for those who are interested in such. It
can also be interpreted, however, as data on when people are most active in searching for bigfoot outdoors. I
initially considered trying to make each column a color corresponding to the season represented in order to further
emphasize how the visualization leads into the second visualization, but I chose to keep them as the same color
gradient in order to allow easier comparison between columns. Additionally, I chose to do a gradient of blue rather
than a multi-color gradient so that the data is easier to read, given it is a straightforward scale from more to less
reports. If I had more time, I would include the option to have the visualization show only a portion of the states
through interactive filtering so that the rows are larger and the state labels are easier to read. Increasing the
font size as it is would only stretch the visualization beyond the length of a computer screen, which defeats the
choice of showing all 50 states together for clarity.
""")

st.header("Reports by Year and Median Temperature, Split Into Seasons")
st.write("Brush along the scatter plot to filter the data shown in the bar plot.")
st.altair_chart(chart2)
st.write("""
In my second visualization, I am showing bigfoot reports over the years with the median temperature of the day they
were reported. These are also filtered by seasons, which is counted on the right in a graph that displays the number
of reports by season in the time frame selected in the scatter plot. Showing temperature data makes how temperature
influences reports more straightforward, as opposed to people assuming that seasons are hotter than others, especially
since it is visible that some seasons can be both warmer and colder than other seasons at different times. The filtered
bar graph enables the viewer to see how the trend of more reports in certain seasons, or the proportion of reports
between seasons, has changed over time. I chose to color the seasons by (at least what I perceive to be) intuitive
colors related to each season so that the graphs are both easy to read without the viewer jumping back to the legend.
Because of this, I also adjusted the opacity of the scatter plot marks, since the circles overlapping led to the bright
yellow summer datapoints to seem much more prominent than the other points. If I had more time, I would try to add a
way for the viewer to make specific year selections on the scatter plot, such as the brush snapping to every 5 years,
since it is hard to draw specific comparisons with the freehand selection. I would also add the choice to change the
temperature to be a different feature of the data through a dropdown, such as humidity and precipitation probability,
after better handling the large amount of missing values in the features.
""")
