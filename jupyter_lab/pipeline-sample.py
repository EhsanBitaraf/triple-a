from triplea.service.repository.export.triplea_format import (
    export_triplea_csvs_in_relational_mode_save_file,
)
from triplea.service.repository.state.initial_arxiv import get_article_list_from_arxiv_all_store_to_arepo
from triplea.service.repository.state.initial import get_article_list_from_pubmed_all_store_to_arepo
from triplea.service.repository.pipeline_core import move_state_forward
import triplea.service.repository.persist as PERSIST
import triplea.service.repository.pipeline_flag as cPIPELINE
if __name__ == "__main__":
    pass

    # Pipeline Sample

    # Step 1 - Get article from Arxiv
    arxiv_search_string = 'ti:"large language model" AND ti:Benchmark AND abs:medical'
    get_article_list_from_arxiv_all_store_to_arepo(arxiv_search_string,0,10)

    # Step 2 - Get article from Pubmed
    pubmed_search_string = '("large language model"[Title]) AND (Benchmark[Title/Abstract])'
    get_article_list_from_pubmed_all_store_to_arepo(pubmed_search_string)
 


    # Step 3 - Get info
    PERSIST.print_article_info_from_repo()

    # Step 4 - Moving from `0` to `1`
    move_state_forward(0)                    

    # Step 5 - Moving from `1` to `2`
    move_state_forward(1)
                    
    # Step 6 - Moving from `2` to `3`
    move_state_forward(2)

    # Moving forward in custom pipeline

    ### Extract Topic
    cPIPELINE.go_extract_topic()

    ### Affiliation Mining
    cPIPELINE.go_affiliation_mining(method="Titipata")

    ### Extract Triple
    cPIPELINE.go_extract_triple()

    # Export
    export_triplea_csvs_in_relational_mode_save_file("export.csv")
    