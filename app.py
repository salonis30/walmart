import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page configuration for better layout
st.set_page_config(page_title="Data Visualization Dashboard", layout="wide")

# CSS for colorful elements and background color with black titles and headings
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #F5F5DC, #81717A, #9D8CA1);
        }
        .main-title {
            color: black;
            font-size: 38px;
            text-align: center;
            font-weight: bold;
            margin-top: 30px;
            margin-bottom: 20px;
        }
        .header {
            font-size: 26px;
            color: black;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .footer {
            font-size: 14px;
            color: black;
            text-align: center;
            margin-top: 50px;
            padding: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# Function to show the login page
def login_page():
    st.markdown("<h1 class='main-title'>Login</h1>", unsafe_allow_html=True)
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Login"):
        if username == "Admin" and password == "saloni123":  # Replace with desired credentials
            st.session_state["logged_in"] = True
            st.success("Logged in successfully")
        else:
            st.error("Invalid username or password")

# Function for plotting graphs
def plot_graph(chart_type, column, dataset, title):
    fig, ax = plt.subplots(figsize=(8, 6))

    if chart_type == "Donut Chart":
        dataset[column].value_counts().plot.pie(autopct="%1.1f%%", ax=ax, wedgeprops=dict(width=0.4))
        ax.set_ylabel('')
    elif chart_type == "Bar Graph":
        sns.barplot(x=dataset[column].value_counts().index, y=dataset[column].value_counts(), ax=ax)
        ax.set_xlabel(column)
        ax.set_ylabel('Count')
    elif chart_type == "Line Graph":
        ax.plot(dataset[column])
        ax.set_xlabel('Index')
        ax.set_ylabel(column)
    elif chart_type == "Pie Chart":
        dataset[column].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
        ax.set_ylabel('')
    elif chart_type == "Histogram":
        sns.histplot(dataset[column], kde=True, ax=ax)
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')

    plt.title(title, fontsize=16)
    st.pyplot(fig)

# Function for the data visualization page
def data_visualization_page():
    st.markdown("<h1 class='main-title'>Data Visualization Dashboard</h1>", unsafe_allow_html=True)

    # Upload dataset dynamically
    uploaded_file = st.file_uploader("Upload your Walmart dataset (CSV)", type=["csv"])
    
    if uploaded_file:
        data = pd.read_csv(uploaded_file)

        # Choose between Static Visualization or Dynamic Visualization
        visualization_type = st.sidebar.selectbox("Choose Visualization Type", ["Static Visualization", "Dynamic Visualization"])

        # Static Data Visualization
        if visualization_type == "Static Visualization":
            st.markdown("<h2 class='header'>Static Data Visualization</h2>", unsafe_allow_html=True)
            static_column = st.selectbox("Select Column for Static Visualization", data.columns)
            static_chart_type = st.selectbox("Select Static Chart Type", ["Donut Chart", "Bar Graph", "Line Graph", "Pie Chart", "Histogram"])
            plot_graph(static_chart_type, static_column, data, "Static Data")

        # Dynamic Data Visualization
        elif visualization_type == "Dynamic Visualization":
            st.markdown("<h2 class='header'>Dynamic Data Visualization</h2>", unsafe_allow_html=True)

            # File upload section
            st.write("### Upload Two CSV Files")
            uploaded_file_1 = st.file_uploader("Choose the first CSV file", type=["csv"], key="dynamic_1")
            uploaded_file_2 = st.file_uploader("Choose the second CSV file", type=["csv"], key="dynamic_2")

            if uploaded_file_1 and uploaded_file_2:
                user_data_1 = pd.read_csv(uploaded_file_1)
                user_data_2 = pd.read_csv(uploaded_file_2)

                st.write("First Dataset Preview:")
                st.dataframe(user_data_1)

                st.write("Second Dataset Preview:")
                st.dataframe(user_data_2)

                # Display comparison between datasets
                st.write("### Data Comparison Summary")
                comparison_summary = {
                    "First Dataset Rows": len(user_data_1),
                    "Second Dataset Rows": len(user_data_2),
                    "Common Columns": list(set(user_data_1.columns).intersection(user_data_2.columns)),
                }
                st.json(comparison_summary)

                # Select column for visualization
                common_columns = comparison_summary["Common Columns"]
                if common_columns:
                    selected_column = st.selectbox("Select Column for Visualization", common_columns)
                    chart_type = st.selectbox("Select Chart Type", ["Donut Chart", "Bar Graph", "Line Graph", "Pie Chart", "Histogram"])

                    # Side-by-side comparison
                    st.markdown("<h2 class='header'>Graph Comparison</h2>", unsafe_allow_html=True)
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("First Dataset")
                        plot_graph(chart_type, selected_column, user_data_1, "First Dataset")

                    with col2:
                        st.write("Second Dataset")
                        plot_graph(chart_type, selected_column, user_data_2, "Second Dataset")
                else:
                    st.warning("No common columns found between the datasets.")
    else:
        st.info("Please upload a dataset to start the analysis.")

# Main app logic: Check login state and display appropriate page
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    data_visualization_page()
else:
    login_page()

# Footer with Help & Support contact information
st.markdown("""
    <div class="footer">
        <p>For help & support, please contact us at:</p>
        <p>Email: <a href="mailto:ss6372370@gmail.com">ss6372370@gmail.com</a></p>
        <p>Phone: +91800012386</p>
    </div>
""", unsafe_allow_html=True)
