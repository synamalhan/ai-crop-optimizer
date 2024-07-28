import streamlit as st
import backend as bk
import plotly.figure_factory as ff


df = bk.load_csv()

c1, c2, c3 = st.columns([1, 6, 1])
c1.page_link("pages/home.py", icon=":material/home:")
c3.page_link("pages/soil_predict.py", icon=":material/potted_plant:")
c2.write("")
c2.write("")
c1.image("assets/logo.png", width=100)
c2.markdown(
    "<h1 style='text-align: center;'>Ideal Crop Predictor</h1>", unsafe_allow_html=True
)
c3.write("")
if c3.button(" ℹ️ info"):
    sidebar = st.sidebar
    sidebar.title(":green[About the Model]")
    sidebar.subheader("Why We Chose Random Forest Classifier:", divider="green")
    sidebar.markdown(
        "We selected the :green[Random Forest Classifier] for our crop prediction model due to its accuracy, robustness, and ability to handle large datasets. This method reduces overfitting by constructing multiple decision trees and averaging their results, leading to more reliable predictions."
    )
    sidebar.subheader("What is Random Forest Classifier:", divider="green")
    sidebar.markdown(
        "The :green[Random Forest Classifier] builds numerous decision trees using random subsets of the data and features, then outputs the most common class among the trees. This ensemble approach enhances predictive performance by combining the strengths of individual trees and mitigating their weaknesses."
    )


container = st.container(border=True)

form = st.form("Crop Prediction")

location = form.text_input("Location:")
form.write("Soil Analysis")
c1, c2, c3, c4 = form.columns(4)
N = c1.text_input("Soil N%:")
P = c2.text_input("Soil P%:")
K = c3.text_input("Soil K%:")
pH = c4.text_input("Soil pH:")
if form.form_submit_button("Submit"):
    temp_c, humid, rain = bk.get_current_weather(location)
    cc1, cc2, cc3 = container.columns(3)
    cc1.write("Temperature: ", temp_c)
    cc2.write(" Humidity: ", humid)
    cc3.write(" Rainfall: ", rain)

    crop = bk.random_forest_classifier(N, P, K, temp_c, humid, rain, pH)

    container.subheader("Best Crop: ", crop)
    with container.expander("Learn More..."):
        container.write()

chart = st.container(border=True)
if chart.checkbox("View DataBase"):
    with chart.expander("About the graph"):
        st.caption(
            "The histogram in our application represents the distribution of temperature data for various crops. Each bar in the histogram corresponds to the frequency of temperature values within specific ranges, allowing us to visualize how temperatures vary for each crop. This comparison highlights common temperature ranges and patterns, providing valuable insights into the environmental conditions suitable for different crops."
        )
    hist_data = []
    c1, c2 = chart.columns([6, 3])

    group_labels = c2.multiselect(
        "Select the crops", df["label"].unique(), df["label"].unique()
    )

    # Gather histogram data
    for label in group_labels:
        data_list = df[df["label"] == label]["temperature"].tolist()
        if data_list:
            hist_data.append(data_list)

    # Filter out empty labels corresponding to empty hist_data lists
    filtered_labels = [
        group_labels[i] for i in range(len(group_labels)) if hist_data[i]
    ]

    if filtered_labels:
        # Create distplot with custom bin_size
        fig = ff.create_distplot(
            hist_data, filtered_labels, bin_size=[0.1 for _ in filtered_labels]
        )

        # Plot!
        c1.plotly_chart(fig, use_container_width=True)
    else:
        c1.write("No data available for the selected crops.")
