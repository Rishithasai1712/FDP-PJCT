import streamlit as st

def data_plots():
    st.title("Data Visualization Dashboard")

    # Section 1: Data Exploration
    st.subheader("Data Exploration")

    # Dropdown to select which plot to display (under Data Exploration)
    plot_selection = st.selectbox(
        'Select Plot to Display:',
        [
            'Transaction Types',
            'Fraud vs. Flagged Fraud',
            'Percentage of Fraud by Hour',
            'KDE Plot of Amount by Class'
        ]
    )

    # Display the selected plot image dynamically with custom size
    if plot_selection == 'Transaction Types':
        st.image('img/types.png', caption='Transaction Types', width=800)
    elif plot_selection == 'KDE Plot of Amount by Class':
        st.image('img/kde.png', caption='KDE Plot of Amount by Class', width=800)
    elif plot_selection == 'Fraud vs. Flagged Fraud':
        st.image('img/pie.png', caption='Fraud vs. Flagged Fraud', width=800)
    elif plot_selection == 'Percentage of Fraud by Hour':
        st.image('img/hours.png', caption='Percentage of Fraud by Hour', width=800)

    # Section 2: Outliers
    st.subheader("Outliers")

    plot_selection = st.selectbox(
        'Select Plot to Display:',
        [
            'Outliers',
            'Handle outliers'
        ]
    )

    if plot_selection == 'Outliers':
        st.image('img/outliers.png', caption='Outliers', width=800)
    elif plot_selection == 'Handle outliers':
        st.image('img/ao.png', caption='Handle outliers', width=800)

    # Section 3: Visualization
    st.subheader("Visualization")

    plot_selection = st.selectbox(
        'Select Plot to Display:',
        [
            'Correlation Matrix',
            'Transaction Amount Distribution'
        ]
    )

    if plot_selection == 'Correlation Matrix':
        st.image('img/corr.png', caption='Correlation Matrix', width=800)
    elif plot_selection == 'Transaction Amount Distribution':
        st.image('img/td.png', caption='Transaction Amount Distribution', width=800)

# Entry point
if __name__ == "__main__":
    data_plots()
