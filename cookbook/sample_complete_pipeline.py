
from triplea.service.repository.state.initial_arxiv import get_article_list_from_arxiv_all_store_to_arepo
from triplea.service.repository.state.initial import get_article_list_from_pubmed_all_store_to_arepo
from triplea.service.repository.pipeline_core import move_state_forward
import triplea.service.repository.persist as PERSIST
import triplea.service.repository.pipeline_flag as cPIPELINE
from triplea.service.repository.export.triplea_format import (
    export_triplea_csvs_in_relational_mode_save_file,
)

if __name__ == "__main__":
    # Step 1 - Get article from Arxiv
    arxiv_search_string = '(ti:“Large language model” OR ti:“Large language models” OR (ti:large AND ti:“language model”) OR (ti:large AND ti:“language models”) OR (ti:“large language” AND ti:model) OR (ti:“large language” AND ti:models) OR ti:“language model” OR ti:“language models” OR ti:LLM OR ti:LLMs OR ti:“GPT models” OR ti:“GPT model” OR ti:Gpt OR ti:gpts OR ti:Chatgpt OR ti:“generative pre-trained transformer” OR ti:“bidirectional encoder representations from transformers” OR ti:BERT OR ti:“transformer-based model” OR (ti:transformer AND ti:model) OR (ti:transformers AND ti:model) OR (ti:transformer AND ti:models) OR (ti:transformers AND ti:models)) AND (ti:Evaluation OR ti:Evaluat* OR ti:Assessment OR ti:Assess* OR ti:Validation OR ti:Validat* OR ti:Benchmarking OR ti:Benchmark*)'
    get_article_list_from_arxiv_all_store_to_arepo(arxiv_search_string,0,5000)

    # Step 2 - Get article from Pubmed
    pubmed_search_string = '("Large language model"[ti] OR "Large language models"[ti] OR (large[ti] AND "language model"[ti]) OR (large[ti] AND "language models"[ti]) OR ("large language"[ti] AND model[ti]) OR ("large language"[ti] AND models[ti]) OR "language model"[ti] OR "language models"[ti] OR LLM[ti] OR LLMs[ti] OR "GPT models"[ti] OR "GPT model"[ti] OR Gpt[ti] OR gpts[ti] OR Chatgpt[ti] OR "generative pre-trained transformer"[ti] OR "bidirectional encoder representations from transformers"[ti] OR BERT[ti] OR "transformer-based model"[ti] OR (transformer[ti] AND model[ti]) OR (transformers[ti] AND model[ti]) OR (transformer[ti] AND models[ti]) OR (transformers[ti] AND models[ti])) AND (Evaluation[ti] OR Evaluat*[ti] OR Assessment[ti] OR Assess*[ti] OR Validation[ti] OR Validat*[ti] OR Benchmarking[ti] OR Benchmark*[ti])'
    get_article_list_from_pubmed_all_store_to_arepo(pubmed_search_string)
 


    # Step 3 - Get info
    PERSIST.print_article_info_from_repo()


    # 0 - article identifier saved

    # Step 4 - Moving from `0` to `1`  - original details of article saved (json Form)
    move_state_forward(0)                    

    # Step 5 - Moving from `1` to `2` - parse details info of article
    move_state_forward(1)
                    
    # Step 6 - Moving from `2` to `3` - Get Citation
    move_state_forward(2)

    # Step 7 - Moving from `3` to `4` - Get Full Text
    move_state_forward(3)

    # Step 8 - Moving from `4` to `5` - Convert full text to string
    move_state_forward(4)

    # Moving forward in custom pipeline

    ### Extract Topic
    cPIPELINE.go_extract_topic()

    ### Affiliation Mining
    cPIPELINE.go_affiliation_mining(method="Titipata")

    ### Extract Triple
    cPIPELINE.go_extract_triple()

    ### Short Review Article
    cPIPELINE.go_article_review_by_llm()

    ### Export
    export_triplea_csvs_in_relational_mode_save_file("export.csv")
    