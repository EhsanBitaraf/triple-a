# CookBook

Example code for accomplishing common tasks with the LangChain library

## Check Configuration
Settings in the TripleA are very important. Before running long and important processes, make sure that the configuration variables are correct. The [`check_config.py`](https://github.com/EhsanBitaraf/triple-a/blob/main/cookbook/check_config.py)  is a simple example of checking settings


## Complete Pipeline


[`sample_complete_pipeline.py`](https://github.com/EhsanBitaraf/triple-a/blob/main/cookbook/sample_complete_pipeline.py)


## Export to multiple CSV format
After performing various steps on the collection of articles in TripleA, a lot of information is collected. If we want to get an output from this information that includes information related to questions and answers from artificial intelligence, the export_engine function should be used. This function allows you to write the functions related to filtering and transformation of the data model and outputs as you wish. and provides a list of normalized dictionaries. You can convert this list to csv files by using convert_unified2csv_dynamically function in Class `Converter`.

[`sample-export-engine-advanced.py`](https://github.com/EhsanBitaraf/triple-a/blob/main/cookbook/sample-export-engine-advanced.py)


## Calculate calling of LLM
[`sample_calculate_llm_call.py`](https://github.com/EhsanBitaraf/triple-a/blob/main/cookbook/sample_calculate_llm_call.py)

## Reset LLM flag with function


[`sample_reset_llm_flag_with_fx.py`](https://github.com/EhsanBitaraf/triple-a/blob/main/cookbook/sample_reset_llm_flag_with_fx.py)


## Reset LLM flag and recall another LLM QA

[`sample_recall_llm.py`](https://github.com/EhsanBitaraf/triple-a/blob/main/cookbook/sample_recall_llm.py)


## Update LLM response
[`sample_update_response.py`]

## Update LLM response with determined JSONDecodeError

[`sample_update_response_jsondecodererror.py`](https://github.com/EhsanBitaraf/triple-a/blob/main/cookbook/sample_update_response_jsondecodererror.py)

## Update LLM response with advanced technique
In this method, special methods are used, which can be used in general for any structured LLM answer.
The `remodel_llm_response` function is produced as a dynamic engine that allows changing the LLM response model using another customer order function such as `fx_response_remodel`.

[`sample_update_response_advance.py`](https://github.com/EhsanBitaraf/triple-a/blob/main/cookbook/sample_update_response_advance.py)