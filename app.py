import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.header("Jose Nieves")


    url = "https://raw.githubusercontent.com/iantonios/dsc205/refs/heads/main/CT-towns-income-census-2020.csv"
    df = pd.read_csv(url)

    df['Per capita income'] = df['Per capita income'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(int)
    df['Median household income'] = df['Median household income'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(int)
    df['Median family income'] = df['Median family income'].str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(int)


    st.subheader("Filter by County")
    # Assumes there is a 'County' column in the dataset.
    counties = df['County'].unique()
    selected_county = st.selectbox("Select a County:", sorted(counties))
    
    county_df = df[df['County'] == selected_county]
    
    st.markdown("**Cities/Towns in Selected County:**")
    # Display the DataFrame with a fixed width and height of 800x200 pixels
    st.dataframe(county_df, width=800, height=200)

    # ------------------------------
    # Slider: Select Median Household Income Range
    # ------------------------------
    st.subheader("Filter by Median Household Income")
    min_income = int(df['Median household income'].min())
    max_income = int(df['Median household income'].max())
    
    income_range = st.slider(
        "Select a median household income range:",
        min_income,
        max_income,
        (min_income, max_income),
        step=1000
    )
    
    income_filtered_df = df[
        (df['Median household income'] >= income_range[0]) &
        (df['Median household income'] <= income_range[1])
    ]
    
    st.markdown("**Cities/Towns with Median Household Income in Selected Range:**")
    st.dataframe(income_filtered_df, width=800, height=200)

    # ------------------------------
    # Bonus: Bar Graph of Highest and Lowest 5 Median Household Incomes
    # ------------------------------
    st.subheader("Bar Graph: Top 5 Highest & Lowest Median Household Incomes")
    # Assumes there's a 'City/Town' column for the names.
    # If the column name is different (e.g., "City" or "Town"), adjust accordingly.
    lowest5 = df.nsmallest(5, 'Median household income')
    highest5 = df.nlargest(5, 'Median household income')
    combined = pd.concat([lowest5, highest5]).sort_values('Median household income')

    fig = px.bar(
        combined,
        x="City/Town",  # Adjust column name if needed
        y="Median household income",
        color="County",
        title="5 Cities with Lowest and 5 with Highest Median Household Income"
    )
    fig.update_layout(xaxis_title="City/Town", yaxis_title="Median Household Income")
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
