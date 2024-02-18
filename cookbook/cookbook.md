# CookBook

Example code for accomplishing common tasks with the LangChain library

## Check Configuration
Settings in the TripleA are very important. Before running long and important processes, make sure that the configuration variables are correct. The [`check_config.py`]()  is a simple example of checking settings


## Export to multiple CSV format
After performing various steps on the collection of articles in TripleA, a lot of information is collected. If we want to get an output from this information that includes information related to questions and answers from artificial intelligence, the export_engine function should be used. This function allows you to write the functions related to filtering and transformation of the data model and outputs as you wish. and provides a list of normalized dictionaries. You can convert this list to csv files by using convert_unified2csv_dynamically function.


sample-export-engine-advanced.py