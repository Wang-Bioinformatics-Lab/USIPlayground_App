import streamlit as st
from gnpsdata import workflow_fbmn

# Write the page label
st.set_page_config(
    page_title="FBMN USI usage",
)


# Getting a GNPS2 Task
try:
    gnps2_task = st.experimental_get_query_params()["task"][0]
    gnps2_task = st.text_input("Enter GNPS2 Task", gnps2_task)
except:
    gnps2_task = st.text_input("Enter GNPS2 Task", "e949b4196672471fb321fe7838b1e48b")


networking_nodes_df = workflow_fbmn.get_clustersummary_dataframe(gnps2_task)
networking_nodes_df["usi"] = networking_nodes_df.apply(lambda x: "mzspec:GNPS2:TASK-{}-{}:scan:{}".format(gnps2_task, "nf_output/clustering/specs_ms.mgf", x["cluster index"]), axis=1)

networking_nodes_df = networking_nodes_df[["usi", "cluster index", "parent mass", "number of spectra", "component"]]

st.write(networking_nodes_df)

# Creating a download of this table
tsv = networking_nodes_df.to_csv(index=False, sep="\t").encode('utf-8')


st.download_button(
   "Click to Download with USIs",
   tsv,
   "file.tsv",
   "text/tsv",
   key='download-tsv'
)
