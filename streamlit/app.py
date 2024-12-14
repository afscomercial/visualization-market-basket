import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load data
@st.cache_data
def load_data():
    data = pd.read_csv("data.csv")
    return data


# Main app
def main():

    # Load data
    data = load_data()
    # Convert to numeric, coercing invalid entries to NaN
    data["order_hour_of_day"] = pd.to_numeric(
        data["order_hour_of_day"], errors="coerce"
    )

    # Drop rows with NaN values
    data = data.dropna(subset=["order_hour_of_day"])

    # Sidebar menu
    plot_type = st.sidebar.selectbox(
        "Select an Option",
        [
            "Introduction",
            "Pre Processing",
            "Reorder Proportions",
            "Reorder Department",
            "Reorder Days",
            "Reorder Add To Cart",
            "Reorder Heatmap",
            "Conclusions"
        ],
    )

    # Render the selected option
    if plot_type == "Introduction":
        st.header("Introduction")
        st.markdown(
            """
        - **Objective**: Analyze Instacart Market Basket data to understand customer purchasing patterns and reordering probability.
        
        - **Source:** Instacart open-source dataset with over 3 million grocery orders from 200,000 users.
	    
        - **Key Features**:
        
            - Product details, user behavior, and transaction data.
            - Information such as days since prior order, aisle category, and reorder status.
        """
        )
    elif plot_type == "Pre Processing":
        st.header("Pre-Processing")
        missing_values = """
            # Missing Value Imputations:
            days_since_prior_order, aisle_category, department
        """
        st.code(missing_values, language="python")
        dropping = """
            # Dropping Irrelevant Columns :
            Eval_set,department_id,user_id, product_id
        """
        st.code(dropping, language="python")
        encoding = """
            # Encoding Techniques:
            > Onehot Encoding
            > Lable Encoding
            > Frequency Encoding
        """
        st.code(encoding, language="python")
        outliers = """
            # Outliers Detection:
            > days_since_prior_order
            > order_hour_of_day
             """
        st.code(outliers, language="python")

        plt.figure(figsize=(6, 6))
        plt.boxplot(
            data["order_hour_of_day"],
            vert=True,
            patch_artist=True,
            boxprops=dict(facecolor="skyblue", color="black"),
        )

        # Set title
        plt.title("Distribution of Order Hour of Day", fontsize=14)

        # Remove x-axis ticks and labels
        plt.xticks([])

        # Render the plot in Streamlit
        st.pyplot(plt.gcf())

    elif plot_type == "Reorder Proportions":

        # Calculate proportions
        reordered_counts = data["reordered"].value_counts()
        reordered_labels = ["Not Reordered", "Reordered"]

        # Plot the pie chart
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(
            reordered_counts,
            labels=reordered_labels,
            autopct="%1.1f%%",  # Show percentages
            startangle=140,  # Rotate for better view
            colors=["skyblue", "salmon"],  # Distinct colors
        )
        ax.set_title("Proportion of Reordered vs. Not Reordered Products", fontsize=14)

        # Render the plot in Streamlit
        st.pyplot(fig)

        # Explanation
        st.markdown(
            """
        The proportion of "Not Reordered" is significantly greater than "Reordered."  
        This indicates that the majority of products are purchased only once, likely because they are less essential or do not meet the customers' recurring needs.
        """
        )
    elif plot_type == "Reorder Department":

        # Calculate reorder rate by department
        dept_reorder = (
            data.groupby("department", observed=True)["reordered"]
            .mean()
            .sort_values(ascending=False)
        )

        # Plot the bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        dept_reorder.plot(kind="bar", color=plt.cm.tab20.colors, ax=ax)
        ax.set_title("Reorder Rate by Department", fontsize=14)
        ax.set_xlabel("Department", fontsize=12)
        ax.set_ylabel("Reorder Rate", fontsize=12)
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig)

        # Explanation
        st.markdown(
            """
        We can see that "Dairy & Eggs" are a basic prod in the households and have the highest reorder rate.
        """
        )
    elif plot_type == "Reorder Days":
        # Plot the bar chart
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(
            x="order_dow",
            y="reordered",
            data=data,
            errorbar=None,  # Suppress error bars
            hue="order_dow",  # Color differentiation by day
            palette="viridis",  # Use the 'viridis' color palette
            dodge=False,  # Avoid separation of bars
        )

        ax.set_title("Reorder Rate by Day of the Week", fontsize=14)
        ax.set_xlabel("Day of Week (0 = Sunday)", fontsize=12)
        ax.set_ylabel("Reorder Rate", fontsize=12)
        ax.legend([], [], frameon=False)  # Remove legend

        # Render the plot in Streamlit
        st.pyplot(fig)
        # Explanation
        st.markdown(
            """
        The day 1 is the one with the highest reorder rate, so is more likely the customers reorder product on Monday, maybe that means the customer trend to restocking groceries after the weekend, preparing for the week ahead. Marketing emails will be very effective on Sunday night, helping the sells the next day. 
        """
        )
    elif plot_type == "Reorder Add To Cart":

        # Plot the histogram
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.histplot(
            data=data,
            x="add_to_cart_order",
            hue="reordered",
            kde=True,  # Include kernel density estimate
            element="step",  # Style the histogram as step lines
            palette="viridis",  # Use Viridis colormap
        )

        ax.set_title("Reorder Rate by Add-to-Cart Order", fontsize=14)
        ax.set_xlabel("Add-to-Cart Position", fontsize=12)
        ax.set_ylabel("Density", fontsize=12)

        # Render the plot in Streamlit
        st.pyplot(fig)

        # Add explanation
        st.markdown(
            """
        This plot shows that reorder a product is more likely on the first products added to the cart, that means the customers prioritize more regular purchased items because are part of their routines
        """
        )
    elif plot_type == "Reorder Heatmap":

        # Bin `add_to_cart_order` and `days_since_prior_order`
        data["cart_bin"] = pd.cut(
            data["add_to_cart_order"],
            bins=[0, 5, 10, 20, 50, 100],
            labels=["1-5", "6-10", "11-20", "21-50", "51+"],
        )
        data["days_bin"] = pd.cut(
            data["days_since_prior_order"],
            bins=[0, 5, 10, 15, 20, 30],
            labels=["0-5", "6-10", "11-15", "16-20", "21+"],
        )

        # Create the pivot table
        heatmap_data = data.pivot_table(
            index="cart_bin",
            columns="days_bin",
            values="reordered",
            aggfunc="mean",
            observed=True,
        )

        # Plot the heatmap
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(
            heatmap_data,
            annot=True,
            cmap="viridis",
            fmt=".2f",
            cbar_kws={"label": "Reorder Likelihood"},
            ax=ax,
        )
        ax.set_title(
            "Reorder Rate by Cart Position and Days Since Prior Order", fontsize=14
        )
        ax.set_xlabel("Days Since Prior Order", fontsize=12)
        ax.set_ylabel("Cart Position Bin", fontsize=12)

        # Render the plot in Streamlit
        st.pyplot(fig)

        # Add explanation
        st.markdown(
            """
        with this heatmap for bins of cart position and days since prior order we can analyze that the products added first to the cart are reorder more quickly, that identify a pattern or essential products that needs to be replaced frequently 
        """
        )
    elif plot_type == "Conclusions":
        st.header("Conclusion")

        st.markdown("""
        The analysis of customer reorder behavior reveals important patterns that are crucial for understanding shopping habits and optimizing business strategies. The data demonstrates that **reorder likelihood** is significantly influenced by factors such as the timing of orders, the positioning of items in the cart, and the interval between purchases.

        **Implications for Business:**
        The insights derived from this analysis provide a solid foundation for building predictive models that classify products based on their reorder potential. Such models can drive personalized recommendations, targeted promotions, and better inventory management, ultimately enhancing customer loyalty and operational efficiency.
        """)

        st.image(
        "https://via.placeholder.com/800x200.png?text=+THANK+YOU", 
        use_container_width=True
    )



if __name__ == "__main__":
    main()
