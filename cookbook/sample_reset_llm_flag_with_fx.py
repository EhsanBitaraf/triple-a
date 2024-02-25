# Reset FlagShortReviewByLLM to 0 with fx

from triplea.schemas.article import Article
from triplea.service.llm.recycle import reset_flag_llm_by_function
from triplea.service.repository import persist

def my_fx(TemplateID, lr):
    # True Must Be Updated
    for r in lr:
        if r['TemplateID'] == TemplateID:
            if 'Response' in r:
                answer = r['Response']
                if answer['A'] == True and answer['B'] == True and answer['C'] == True: 
                    print(answer)
                    return True
                else:
                    return False                    
        else:
            pass
    return False

if __name__ == "__main__":
    reset_flag_llm_by_function("Ass11",my_fx,limit_sample=0)
    print()


