import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Data Visualization Dashboard", layout="wide")

# Load dataset from a specific file path or show an upload option
file_path = r"C:\\Users\\salon\\Downloads\\freshwalmart\\Walmart_cleaned_filtered_limited.csv"
try:
    data = pd.read_csv(file_path)
    st.success("Default dataset loaded successfully!")
except FileNotFoundError:
    st.warning("Default dataset not found. Please upload a dataset.")

# File uploader fallback if default file isn't found
uploaded_file = st.file_uploader("Upload a CSV file if default dataset is unavailable", type=["csv"])
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.success("Uploaded dataset loaded successfully!")

# Stop app if no data is available
if 'data' not in locals():
    st.error("No dataset available to proceed. Please check the file path or upload a dataset.")
    st.stop()

# Custom CSS for styling
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
        }
    </style>
""", unsafe_allow_html=True)

# Login Page
def login_page():
    st.markdown("<h1 class='main-title'>Login</h1>", unsafe_allow_html=True)
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Login"):
        if username == "Admin" and password == "saloni123":
            st.session_state["logged_in"] = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

# Graph plotting function
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

# Data Visualization Dashboard
def data_visualization_page():
    st.markdown("<h1 class='main-title'>Data Visualization Dashboard</h1>", unsafe_allow_html=True)

    # Visualization type selection
    visualization_type = st.sidebar.selectbox("Choose Visualization Type", ["Static Visualization", "Dynamic Visualization"])

    # Static Visualization
    if visualization_type == "Static Visualization":
        st.markdown("<h2 class='header'>Static Data Visualization</h2>", unsafe_allow_html=True)
        column = st.selectbox("Select Column for Visualization", data.columns)
        chart_type = st.selectbox("Select Chart Type", ["Donut Chart", "Bar Graph", "Line Graph", "Pie Chart", "Histogram"])
        plot_graph(chart_type, column, data, f"Static Visualization: {column}")

    # Dynamic Visualization
    elif visualization_type == "Dynamic Visualization":
        st.markdown("<h2 class='header'>Dynamic Data Visualization</h2>", unsafe_allow_html=True)

        # File upload for comparison
        file1 = st.file_uploader("Upload First Dataset", type=["csv"])
        file2 = st.file_uploader("Upload Second Dataset", type=["csv"])

        if file1 and file2:
            data1 = pd.read_csv(file1)
            data2 = pd.read_csv(file2)

            st.write("First Dataset Preview:")
            st.dataframe(data1)

            st.write("Second Dataset Preview:")
            st.dataframe(data2)

            common_columns = list(set(data1.columns).intersection(data2.columns))
            if common_columns:
                column = st.selectbox("Select Column for Comparison", common_columns)
                chart_type = st.selectbox("Select Chart Type", ["Donut Chart", "Bar Graph", "Line Graph", "Pie Chart", "Histogram"])

                col1, col2 = st.columns(2)

                with col1:
                    st.write("First Dataset")
                    plot_graph(chart_type, column, data1, "First Dataset")

                with col2:
                    st.write("Second Dataset")
                    plot_graph(chart_type, column, data2, "Second Dataset")
            else:
                st.warning("No common columns found between datasets.")

# Main Logic
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    data_visualization_page()
else:
    login_page()

# Footer
st.markdown("""
    <div class="footer">
        <p>For help & support, contact:</p>
        <p>Email: <a href="mailto:ss6372370@gmail.com">ss6372370@gmail.com</a></p>
        <p>Phone: +91800012386</p>
    </div>
""", unsafe_allow_html=True)

