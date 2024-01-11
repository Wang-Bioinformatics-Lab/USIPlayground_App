import streamlit as st
import requests

# Write the page label
st.set_page_config(
    page_title="Dataset USI usage",
)

# Enter all the datasets accessions in textarea
st.write("Enter all the datasets")

dataset_strings = st.text_area("Enter all the datasets with new lines", "MSV000082622\nMSV000086873")

datasets = dataset_strings.split("\n")

# Getting all the USIs
all_usis = []
for dataset_accession in datasets:
    all_files_url = "https://explorer.gnps2.org/api/datasets/{}/files".format(dataset_accession)

    st.write(all_files_url)

    all_files = requests.get(all_files_url).json()

    for file in all_files:
        filename = file["filename"]

        usi = "mzspec:{}:{}".format(dataset_accession, filename)

        usi_dict = {}
        usi_dict["usi"] = usi
        usi_dict["dataset"] = dataset_accession

        all_usis.append(usi_dict)

# Creating a df
import pandas as pd
df = pd.DataFrame(usi_dict)

st.write(df)
