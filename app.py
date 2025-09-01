import streamlit as st
from search import get_search_results
from scraper import scrape_content
from ollama_rag import get_answer
from predictor import predict_sales

st.set_page_config(layout="wide")
st.title("📈 BizAI – Real-Time Business Insights Chatbot")

query = st.text_input("🔍 Ask a business question:", placeholder="e.g., Latest revenue of TCS or Infosys CEO")

if query:
    with st.spinner("🔎 Searching the web..."):
        urls = get_search_results(query)

    with st.spinner("📰 Scraping and analyzing articles..."):
        documents = scrape_content(urls)

    with st.spinner("🤖 Generating answer from AI..."):
        answer, sources = get_answer(query, documents)

    st.subheader("📢 Answer")
    st.markdown(answer)

    st.subheader("🔗 Sources")
    for url in sources:
        st.markdown(f"- [Source]({url})")

    # 🧠 Add ML-based prediction if it's a revenue/sales question
    if any(word in query.lower() for word in ["revenue", "sales", "growth", "prediction"]):
        with st.spinner("📈 Predicting next year's revenue..."):
            df, prediction = predict_sales(query)

            if df is not None:
                st.subheader("📊 Historical Revenue Data")
                st.dataframe(df)

                st.success(f"📈 Predicted revenue for {df['Year'].max() + 1}: **${prediction:,.0f}**")
            else:
                st.warning(prediction)
