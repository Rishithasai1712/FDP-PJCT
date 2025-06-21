import streamlit as st
import pandas as pd
import joblib
import altair as alt

# Load the trained Random Forest model
rf_model = joblib.load('rf_model3.pkl')

# Feature list used in the model
features = ['step', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest', 'isFlaggedFraud']

# Fraud detection logic using the trained model
def detect_fraud(transaction):
    transaction_df = pd.DataFrame([transaction], columns=features)
    prediction = int(rf_model.predict(transaction_df)[0])
    issues = {'origin': False, 'destination': False}  # Placeholder for any custom logic
    return prediction, "ML model prediction: Fraud" if prediction == 1 else "ML model prediction: Not Fraud", issues

# Prevention logic for flagging potential fraud
def prevent_fraud(transaction):
    step, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, isFlaggedFraud = transaction
    actions = []

    if isFlaggedFraud == 1:
        actions.append("⚠️ WARNING: Transaction is flagged as fraud and may not be safe.")
    if amount > 50000:
        actions.append("🚨 High transaction amount")
    if oldbalanceOrg < amount:
        actions.append("🚨 Insufficient origin balance")
    if oldbalanceDest == 0 and newbalanceDest == 0:
        actions.append("🚨 Destination balance anomaly")

    ml_result, _, _ = detect_fraud(transaction)
    if ml_result == 1:
        actions.append("🚨 detected fraud")

    return "✅ ALLOWED" if not actions else " | ".join(actions)

# Streamlit interface for bulk fraud detection using CSV upload
def render_bulk_check(uploaded_file):
    try:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Validate if the uploaded file has the required columns
        if not all(col in df.columns for col in features):
            st.error(f"Uploaded CSV must contain the following columns:\n{features}")
            return None

        st.success("File uploaded successfully!")
        st.dataframe(df.head())  # Show first few rows of the dataframe

        # Fraud detection and prevention logic
        st.markdown("## 🔎 Fraud Detection Results")

        # Apply fraud detection to each row of the DataFrame
        fraud_results = df[features].apply(lambda row: detect_fraud(row.tolist()), axis=1)
        df['FraudDetected'] = fraud_results.apply(lambda x: x[0])
        df['FraudReason'] = fraud_results.apply(lambda x: x[1])
        df['FraudIssue'] = fraud_results.apply(lambda x: x[2])
        df['PreventionAction'] = df[features].apply(lambda row: prevent_fraud(row.tolist()), axis=1)

        # Display fraud detection results for each transaction
        for idx, row in df.iterrows():
            st.markdown(f"---\n### 📄 Transaction {idx + 1}")
            st.write(f"**Step:** {row['step']}  |  **Amount:** {row['amount']}")
            st.write(f"**Origin Balance:** {row['oldbalanceOrg']} → {row['newbalanceOrig']}")
            st.write(f"**Destination Balance:** {row['oldbalanceDest']} → {row['newbalanceDest']}")
            st.write(f"**Flagged by System:** {'✅ Yes' if row['isFlaggedFraud'] == 1 else '❌ No'}")
            st.info(f"**Fraud Status:** {' ❌ FRAUD' if row['FraudDetected'] == 1 else '✅ Not Fraud'}")
            st.write(f"**Reason:** {row['FraudReason']}")
            st.warning(f"**Prevention Advice:** {row['PreventionAction']}")

        # Optional: Download the results as a CSV file
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results as CSV", data=csv, file_name='fraud_results.csv', mime='text/csv')

        # Visualization: Fraud detection vs flagged status
        st.markdown("### 📊 Visualize Fraud Detection")
        df["FlaggedStr"] = df["isFlaggedFraud"].map({0: "Not Flagged", 1: "Flagged"})

        chart = alt.Chart(df).mark_point(size=100).encode(
            x=alt.X('step:Q', title='Step'),
            y=alt.Y('amount:Q', title='Amount'),
            color=alt.Color('FraudDetected:N', scale=alt.Scale(domain=[0, 1], range=['green', 'red']),
                            legend=alt.Legend(title='Fraud Detected')),
            shape=alt.Shape('FlaggedStr:N', scale=alt.Scale(domain=['Not Flagged', 'Flagged'],
                            range=['circle', 'triangle']), legend=alt.Legend(title='User Flagged')),
            tooltip=['step', 'amount', 'FraudDetected', 'FlaggedStr']
        ).properties(
            width=700, height=400,
            title="Fraud Detection (ML Prediction & Flag Status)"
        )

        st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.error(f"Error reading or processing file: {e}")

# Streamlit main function
def main():
    st.title("📂 Bulk Fraud Detection using CSV Upload")

    uploaded_file = st.file_uploader("Upload your Transactions CSV file", type=["csv"])
    
    if uploaded_file:
        render_bulk_check(uploaded_file)

if __name__ == '__main__':
    main()
