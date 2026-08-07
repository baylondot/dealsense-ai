import streamlit as st
from pipeline import run_pipeline
from analysis import analyze_company
from report import generate_report

st.set_page_config(
    page_title="DealSense AI",
    page_icon="📊",
    layout="centered"

)

st.title("📊 DealSense AI")
st.caption("AI-Powered Due Diligence Assistant")

st.divider()

url = st.text_input(
    "Company Website",
    placeholder="Enter the Company URL"
)

if st.button("🔍 Analyze Company", use_container_width=True):

    if not url:
        st.warning("Please enter a company website.")
        st.stop()

    with st.spinner("Analyzing company..."):

        try:
            result = run_pipeline(url)

        except Exception as e:
            st.error(str(e))
            st.stop()

    st.success("Analysis Complete!")

    st.divider()

    col1, col2 = st.columns([3, 1])

    with col1:
        st.header(result.company)

    with col2:
        st.metric(
            "Acquisition Score",
            f"{result.acquisition_score}/100"
        )

    st.subheader("Executive Summary")
    st.write(result.summary)

    st.subheader("Business Model")
    st.write(result.business_model)

    st.subheader("Industry")
    st.write(result.industry)

    st.subheader("Products")

    if result.products:
        for product in result.products:
            st.markdown(f"- {product}")
    else:
        st.write("Not enough information.")

    st.subheader("Customers")

    if result.customers:
        for customer in result.customers:
            st.markdown(f"- {customer}")
    else:
        st.write("Not enough information.")

    st.subheader("Competitive Landscape")

    if result.competitors:
        for competitor in result.competitors:
            with st.container(border=True):
                st.markdown(f"### {competitor.name}")
                st.write(competitor.reason)
    else:
        st.write("Not enough information.")

    st.subheader("Risks")

    if result.risks:
        for risk in result.risks:
            st.markdown(f"- {risk}")
    else:
        st.write("Not enough information.")

    st.subheader("SWOT Analysis")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### ✅ Strengths")
        for item in result.swot.strengths:
            st.markdown(f"- {item}")

        st.markdown("### 📈 Opportunities")
        for item in result.swot.opportunities:
            st.markdown(f"- {item}")

    with c2:
        st.markdown("### ❌ Weaknesses")
        for item in result.swot.weaknesses:
            st.markdown(f"- {item}")

        st.markdown("### ⚠ Threats")
        for item in result.swot.threats:
            st.markdown(f"- {item}")

    st.subheader("Recommendation")
    st.info(result.recommendation)
    report = generate_report(result)

    st.divider()

    st.subheader("Investment Memo")

    st.markdown(report)

    st.download_button(
    label="📄 Download Investment Memo",
    data=report,
    file_name=f"{result.company}_Investment_Memo.md",
    mime="text/markdown"
)