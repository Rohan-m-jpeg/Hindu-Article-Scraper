import streamlit as st
import pandas as pd
import os
import subprocess
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.scraper.spiders.hindu_spider import HinduSpider

subprocess.run(["scrapy","crawl","hindu","-o","output.csv"])

file = "output.csv"

os.path.exists(file)
history_df = pd.read_csv(file)

st.set_page_config(layout="wide")
st.title("News Scraper")

url = st.text_input("Article URL:", " ")

col1, col2 = st.columns([3, 1])

with col1:
    if st.button("Scrape Article") and url.strip():
        if os.path.exists(file):
            os.remove(file)

        process = CrawlerProcess(get_project_settings())
        process.crawl(HinduSpider, start_urls=[url], output_file=file)
        process.start()

        if os.path.exists(file):
            try:
                df = pd.read_csv(file)
                st.subheader("Scraped Data")
                st.dataframe(df)

                history_df = pd.concat([history_df, df], ignore_index=True)
                history_df.to_csv(file, index=False)
            except pd.errors.EmptyDataError:
                st.error("No data scraped")
        else:
            st.error("No output file created")

with col1:
    st.subheader("History")
    if not history_df.empty:
        st.dataframe(history_df)
    else:
        st.info("No history yet.")
