import streamlit as st
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Out-of-Stock Demand Tracker", page_icon="📦", layout="wide")

COLUMNS = ["ID", "Date", "Product Name", "Category", "Brand", "Size", "Color",
           "Quantity", "Store Location", "Customer Contact", "Notes"]

CATEGORIES = ["Apparel", "Grocery", "Electronics", "Household", "Accessories"]

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=COLUMNS)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main { background-color: #f7f9fc; }
.kpi-card {
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    color: white;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    margin-bottom: 10px;
}
.kpi-value { font-size: 26px; font-weight: 700; margin: 0; }
.kpi-label { font-size: 13px; opacity: 0.9; margin: 0; }
h1, h2, h3 { color: #1e293b; }
.stButton>button {
    background-color: #2575fc;
    color: white;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    border: none;
}
.stButton>button:hover { background-color: #6a11cb; }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📦 Demand Tracker")
page = st.sidebar.radio("Navigate", ["🏠 Dashboard", "📝 Add Request", "📋 Demand Database", "📊 Analytics", "📥 Reports"])
st.sidebar.markdown("---")
st.sidebar.caption("Out-of-Stock Demand Tracker — Retail Demand Intelligence System")

# Simple date input replaces datetime
selected_date = st.sidebar.date_input("Current Date")
current_date_str = str(selected_date)

df = st.session_state.data

# ---------------- DASHBOARD ----------------
if page == "🏠 Dashboard":
    st.title("📦 Out-of-Stock Demand Tracker")
    st.markdown("### Transform Lost Sales Into Inventory Intelligence")
    st.write("Capture customer demand for unavailable products and make smarter inventory decisions.")

    total_requests = len(df)
    today_requests = (df["Date"] == current_date_str).sum() if not df.empty else 0
    most_requested_product = df["Product Name"].mode()[0] if not df.empty else "N/A"
    most_requested_category = df["Category"].mode()[0] if not df.empty else "N/A"
    lost_sales_estimate = int(total_requests * 0.68)
    risk = "High" if total_requests > 20 else "Medium" if total_requests > 5 else "Low"

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        st.markdown(f"<div class='kpi-card'><p class='kpi-value'>{total_requests}</p><p class='kpi-label'>Total Requests</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='kpi-card'><p class='kpi-value'>{today_requests}</p><p class='kpi-label'>Requests Today</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='kpi-card'><p class='kpi-value'>{most_requested_product}</p><p class='kpi-label'>Most Requested Product</p></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='kpi-card'><p class='kpi-value'>{most_requested_category}</p><p class='kpi-label'>Most Requested Category</p></div>", unsafe_allow_html=True)
    with col5:
        st.markdown(f"<div class='kpi-card'><p class='kpi-value'>{lost_sales_estimate}</p><p class='kpi-label'>Estimated Lost Sales</p></div>", unsafe_allow_html=True)
    with col6:
        st.markdown(f"<div class='kpi-card'><p class='kpi-value'>{risk}</p><p class='kpi-label'>Inventory Risk Score</p></div>", unsafe_allow_html=True)

    st.markdown("---")

    if not df.empty:
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Demand by Category")
            st.bar_chart(df["Category"].value_counts())
        with col_b:
            st.subheader("Demand Trend by Date")
            trend = df.groupby("Date").size()
            st.line_chart(trend)

        st.subheader("📋 Recent Activity")
        st.dataframe(df.sort_values("ID", ascending=False).head(5), use_container_width=True)
    else:
        st.info("No requests recorded yet. Add a request to see analytics.")

# ---------------- ADD REQUEST ----------------
elif page == "📝 Add Request":
    st.title("📝 Record Out-of-Stock Request")
    st.write("Fill in the details of the unavailable product requested by the customer.")

    with st.form("request_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            product_name = st.text_input("Product Name*")
            category = st.selectbox("Category*", CATEGORIES)
            brand = st.text_input("Brand")
            size = st.text_input("Size")
        with col2:
            color = st.text_input("Color")
            quantity = st.number_input("Quantity", min_value=1, value=1)
            store_location = st.text_input("Store Location*")
            customer_contact = st.text_input("Customer Contact (optional)")

        notes = st.text_area("Additional Notes")
        request_date = st.date_input("Request Date", value=selected_date)

        submitted = st.form_submit_button("✅ Submit Request")

        if submitted:
            if not product_name or not store_location:
                st.error("Please fill in all required fields (marked with *).")
            else:
                new_id = len(df) + 1
                new_row = {
                    "ID": new_id,
                    "Date": str(request_date),
                    "Product Name": product_name,
                    "Category": category,
                    "Brand": brand,
                    "Size": size,
                    "Color": color,
                    "Quantity": quantity,
                    "Store Location": store_location,
                    "Customer Contact": customer_contact,
                    "Notes": notes
                }
                st.session_state.data = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                st.success("✅ Request recorded successfully!")

# ---------------- DEMAND DATABASE ----------------
elif page == "📋 Demand Database":
    st.title("📋 Centralized Demand Database")

    if df.empty:
        st.info("No records found yet.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            cat_filter = st.selectbox("Filter by Category", ["All"] + CATEGORIES)
        with col2:
            store_filter = st.text_input("Filter by Store Location")
        with col3:
            search_term = st.text_input("Search Product Name")

        filtered_df = df.copy()
        if cat_filter != "All":
            filtered_df = filtered_df[filtered_df["Category"] == cat_filter]
        if store_filter:
            filtered_df = filtered_df[filtered_df["Store Location"].str.contains(store_filter, case=False, na=False)]
        if search_term:
            filtered_df = filtered_df[filtered_df["Product Name"].str.contains(search_term, case=False, na=False)]

        st.dataframe(filtered_df, use_container_width=True)

        st.markdown("---")
        st.subheader("🗑️ Delete a Record")
        if not filtered_df.empty:
            del_id = st.selectbox("Select ID to delete", filtered_df["ID"].tolist())
            if st.button("Delete Record"):
                st.session_state.data = df[df["ID"] != del_id].reset_index(drop=True)
                st.success(f"Record {del_id} deleted.")
                st.rerun()

# ---------------- ANALYTICS ----------------
elif page == "📊 Analytics":
    st.title("📊 Analytics & Insights")

    if df.empty:
        st.info("No data available for analytics yet.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top Requested Products")
            st.bar_chart(df["Product Name"].value_counts().head(10))
        with col2:
            st.subheader("Most Requested Categories")
            st.bar_chart(df["Category"].value_counts())

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Most Requested Sizes")
            if df["Size"].astype(str).str.strip().ne("").any():
                st.bar_chart(df["Size"].value_counts())
            else:
                st.write("No size data available.")
        with col4:
            st.subheader("Most Requested Colors")
            if df["Color"].astype(str).str.strip().ne("").any():
                st.bar_chart(df["Color"].value_counts())
            else:
                st.write("No color data available.")

        st.subheader("Regional Demand Analysis (by Store)")
        st.bar_chart(df["Store Location"].value_counts())

        st.markdown("---")
        st.subheader("💡 AI-Style Recommendations")
        top_category = df["Category"].value_counts().idxmax()
        top_product = df["Product Name"].value_counts().idxmax()
        recommendations = [
            f"📌 Restock **{top_product}** immediately — highest demand product.",
            f"📌 Increase inventory allocation for the **{top_category}** category.",
            "📌 Monitor recurring shortages and set up automatic reorder alerts.",
        ]
        for rec in recommendations:
            st.info(rec)

# ---------------- REPORTS ----------------
elif page == "📥 Reports":
    st.title("📥 Reports Center")

    if df.empty:
        st.info("No data available to generate reports.")
    else:
        st.subheader("Report Preview")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Full Report as CSV",
            data=csv,
            file_name="demand_report.csv",
            mime="text/csv"
        )

        st.markdown("---")
        st.subheader("Summary Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Requests", len(df))
        with col2:
            st.metric("Total Quantity Requested", int(df["Quantity"].sum()))
        with col3:
            st.metric("Unique Products", df["Product Name"].nunique())