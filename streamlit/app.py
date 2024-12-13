import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    # Example data generation
    data = pd.DataFrame({
        'x': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'y': [1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
        'values': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    })
    return data

# Main app
def main():
    st.title("Streamlit Plots with Sidebar Menu")

    # Load data
    data = load_data()

    # Sidebar menu
    plot_type = st.sidebar.selectbox(
        "Select an Option",
        ["Introduction", "Histogram", "Scatter Plot", "Bar Chart", "Static Image"]
    )

    # Render the selected option
    if plot_type == "Introduction":
        st.header("Welcome to the Streamlit Plots App")
        st.markdown("""
        This app demonstrates different types of visualizations using Streamlit.
        - **Histogram:** Visualize the distribution of values.
        - **Scatter Plot:** Show the relationship between two variables.
        - **Bar Chart:** Compare categorical data values.
        
        Use the menu on the left to navigate between the visualizations.
        
        **Happy Exploring!**
        """)
    elif plot_type == "Histogram":
        st.header("Histogram")
        bins = st.slider("Number of bins", min_value=5, max_value=50, value=10)
        fig, ax = plt.subplots()
        ax.hist(data['values'], bins=bins, color='skyblue', edgecolor='black')
        ax.set_title("Histogram")
        ax.set_xlabel("Values")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    elif plot_type == "Scatter Plot":
        st.header("Scatter Plot")
        fig, ax = plt.subplots()
        ax.scatter(data['x'], data['y'], color='red')
        ax.set_title("Scatter Plot")
        ax.set_xlabel("X Values")
        ax.set_ylabel("Y Values")
        st.pyplot(fig)

    elif plot_type == "Bar Chart":
        st.header("Bar Chart")
        fig, ax = plt.subplots()
        ax.bar(data['x'], data['values'], color='green')
        ax.set_title("Bar Chart")
        ax.set_xlabel("X Values")
        ax.set_ylabel("Values")
        st.pyplot(fig)
        
    elif plot_type == "Static Image":
        st.header("Static Image")
        st.markdown("Below is an example of a static image:")
        st.image("https://via.placeholder.com/600x400.png?text=Sample+Static+Image", 
                 caption="Sample Static Image", 
                 use_container_width=True)

if __name__ == "__main__":
    main()