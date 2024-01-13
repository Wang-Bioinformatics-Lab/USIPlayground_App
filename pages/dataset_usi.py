import streamlit as st
import requests
import requests_cache

requests_cache.install_cache('dataset_usi_cache', backend='sqlite')

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

    try:
        all_files = requests.get(all_files_url).json()

        for file in all_files:
            filename = file["filename"]

            usi = "mzspec:{}:{}".format(dataset_accession, filename)

            usi_dict = {}
            usi_dict["usi"] = usi
            usi_dict["dataset"] = dataset_accession
            usi_dict["filename"] = filename

            all_usis.append(usi_dict)
    except:
        continue

# Creating a df
import pandas as pd
df = pd.DataFrame(all_usis)

st.write(df)

# Lets see about filtering by extension
st.write("Filtering by extension")

# get extension for filename column
df["extension"] = df["filename"].apply(lambda x: x.split(".")[-1])

# get unique extensions
unique_extensions = df["extension"].unique()

# Make a multiple selection to filter by extension
selected_extensions = st.multiselect("Select Extensions", unique_extensions, unique_extensions)

# Filter by extension
df = df[df["extension"].isin(selected_extensions)]

st.write(df)

# Making an option to remove potential duplications with precidence on dataset collection

# grouping files per dataset
grouped_df = df.groupby("dataset")

output_df_list = []
# for each dataset, lets see which collections are present
for dataset, files_df in grouped_df:
    # get all the collections
    collections = files_df["filename"].apply(lambda x: x.split("/")[0]).unique()

    if "ccms_peak" in collections:
        # filter to only ccms_peak
        filtered_df = files_df[files_df["filename"].apply(lambda x: x.split("/")[0]) == "ccms_peak"]

        output_df_list.append(filtered_df)

    elif "peak" in collections:
        # filter to only peak
        filtered_df = files_df[files_df["filename"].apply(lambda x: x.split("/")[0]) == "peak"]

        output_df_list.append(filtered_df)
    
    elif "raw" in collections:
        # filter to only raw
        filtered_df = files_df[files_df["filename"].apply(lambda x: x.split("/")[0]) == "raw"]

        output_df_list.append(filtered_df)
    
    else:
        output_df_list.append(filtered_df)

# Concatenating all the dataframes

final_df = pd.concat(output_df_list)

st.write("Filtered DF with precidence on dataset collection, from {} to {}".format(len(df), len(final_df)))
st.write(final_df)

