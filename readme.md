# Generative AI for Software Development - Experiment
This repository contains the code for the experiment that was conducted during the master's thesis by Wendi Shu. 

The application can be locally ran with the following command (see also [Streamlit Docs: streamlit run](https://docs.streamlit.io/develop/api-reference/cli/run)):

```streamlit run app.py```

Please be aware that the GenAI chat might not work. If you want the whole functionality of the experiment, some information must be added in the .streamlit > secrets.toml file. More specifically, you must add the following information as strings:
- OpenAI API key
- admin username (for admin page only)
- admin password (for admin page only)
- mail (email address for participant file upload updates only)
- mail_pw (email address password for participant file upload upadates only)
- connections.gcs (information for Google Cloud Bucket connection)

For GCS connection, see also [Streamlit Doc: Connect Streamlit to Google Cloud Storage](https://docs.streamlit.io/develop/tutorials/databases/gcs)
