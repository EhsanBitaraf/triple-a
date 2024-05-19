from triplea.service.llm.calculate import post_calculate, precalculate
from triplea.utils.general import print_pretty_dict

if __name__ == "__main__":
    #--------------------------Calculate before go_article_review_by_llm-----
    # This function averages numbers given to it before calling the LLM.
    # It calculates the cost, time and the total number of tokens in the
    # whole calling process and returns it as a Json format.
    d = precalculate(6,22)
    print()
    print_pretty_dict(d)
    #--------------------------Calculate before go_article_review_by_llm-----

    #--------------------------Calculate after go_article_review_by_llm------
    o = post_calculate(template_id = "")
    print()
    print_pretty_dict(o)
    #--------------------------Calculate after go_article_review_by_llm------