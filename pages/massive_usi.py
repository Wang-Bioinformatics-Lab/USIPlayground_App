import streamlit as st
import requests
import requests_cache
from pathlib import Path

requests_cache.install_cache('dataset_usi_cache', backend='sqlite')

# Write the page label
st.set_page_config(
    page_title="Dataset USI usage",
)


# Enter all the datasets accessions in textarea
st.write("Enter all MassIVE File Paths, e.g. massive/v03/MSV")

dataset_file_strings = st.text_area("Enter MassIVE Paths", "massive/v03/MSV000087572/raw/mzML/NEG_MSMS_mzML/DOM_Interlab-LC-MS_Lab20_A45M_Neg_MS2_rep1.mzML")

file_paths = dataset_file_strings.split("\n")

all_paths = []

for file_path in file_paths:
    # Lets use path and get the USI for it
    path = Path(file_path)

    dataset_accession = None
    massive_file_path = None

    # go from root til we find one that starts with MSV
    for i in range(1, len(path.parts)):
        if path.parts[i].startswith("MSV"):
            dataset_accession = path.parts[i]

            # lets get the rest of the path
            massive_file_path = "/".join(path.parts[i+1:])
            break

    if dataset_accession is not None:
        file_path_dict = {}
        file_path_dict["massive_file_path"] = massive_file_path
        file_path_dict["dataset_accession"] = dataset_accession

        # Creating the MRI
        mri = "mzspec:{}:{}".format(dataset_accession, massive_file_path)

        file_path_dict["mri"] = mri

        all_paths.append(file_path_dict)

    
# Creating a df
import pandas as pd
df = pd.DataFrame(all_paths)

# Wrtiign this
st.write(df)
