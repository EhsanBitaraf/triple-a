

from triplea.service.llm.recycle import reset_flag_llm_by_function
import triplea.service.repository.persist as PERSIST
import triplea.service.llm as LLM_fx
from triplea.utils.general import pretty_print_dict
import triplea.service.repository.pipeline_flag as cPIPELINE

if __name__ == "__main__":
    pass
    # # ------------------------Read PMID And Question From LLM-----------------
    # id = "37264679"

    # a = PERSIST.get_article_by_pmid(id)
    # q = LLM_fx.get_prompt_with_template(a['Title'],a['Abstract'])
    # print("Question:")
    # print(q)
    # r = LLM_fx.question_with_template_for_llm(a['Title'],a['Abstract'])
    # print()
    # pretty_print_dict(r)
    # # ------------------------Read PMID And Question From LLM-----------------

    # #-------------------------Reset FlagShortReviewByLLM to 0 with fx----------
    # def my_fx(TemplateID, lr):
    #     # True Must Be Updated
    #     for r in lr:
    #         if 'Response' in r:
    #             if r['TemplateID'] == TemplateID:
    #                 if 'B' in r['Response']:
    #                     if r['Response']['B'] is True:
    #                         return True
                  
    #         else:
    #             print(r)
    #             return False

    #     return False
    # reset_flag_llm_by_function("T102",my_fx,limit_sample=0)
    # print()
    # #-------------------------Reset FlagShortReviewByLLM to 0 with fx----------

    # # ------------------------Run Short Review Article Pipeline----------------
    # cPIPELINE.go_article_review_by_llm()
    # # ------------------------Run Short Review Article Pipeline----------------