

import json
from triplea.db.mongo_nav import get_article_info_with_llm_response,get_groupby_with_llm_response

if __name__ == "__main__":
    # data= get_article_info_with_llm_response("Yes")
    # print(data)
    # with open('The-given.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)

    data = get_groupby_with_llm_response()


    for i in data:
        if 'No' in i['_id']:
            i['Response'] = 'No'
        elif 'Yes' in i['_id']:
            i['Response'] = 'Yes'
        else:
            i['Response'] = 'Unknown'
        
        total_tokens =  i['totalInputTokens'] + i['totalOutputTokens']
        token_per_second = total_tokens / i['totalTimeTaken']

        i['TokenPerSecond'] = token_per_second
        i['SecondPerRequest'] = i['totalTimeTaken']/i['count']
        i['gCO2e'] = ((total_tokens)/1000)* 0.3
        # The input tokens for GPT-4 Turbo cost $0.01 per 1,000 tokens,
        # and the output tokens cost $0.03 per 1,000 tokens
        i['Price'] = ((i['totalInputTokens']/1000) * 0.01) + ((i['totalOutputTokens']/1000) * 0.03)



    with open('gResp.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    def added_element(d,i,element):
        for element in ['count','totalInputTokens','totalOutputTokens','totalTimeTaken','TokenPerSecond','SecondPerRequest','gCO2e','Price']:
            d[element] = d[element] + i[element]
        return d

    yes ={"Response": "Yes", "count":0,'totalInputTokens':0,'totalOutputTokens':0,'totalTimeTaken':0,'TokenPerSecond':0,'SecondPerRequest':0,'gCO2e':0,'Price':0 }
    no ={"Response": "No", "count":0, 'totalInputTokens':0,'totalOutputTokens':0,'totalTimeTaken':0,'TokenPerSecond':0,'SecondPerRequest':0,'gCO2e':0,'Price':0}
    unknown= {"Response": "Unknown", "count":0,'totalInputTokens':0,'totalOutputTokens':0,'totalTimeTaken':0,'TokenPerSecond':0,'SecondPerRequest':0,'gCO2e':0,'Price':0 }
    total= {"Response": "total", "count":0,'totalInputTokens':0,'totalOutputTokens':0,'totalTimeTaken':0,'TokenPerSecond':0,'SecondPerRequest':0,'gCO2e':0,'Price':0 }
    for i in data:
        if 'No' in i['Response']:
            d = no
            d = added_element(d, i, 'count')
            no = d
        elif 'Yes' in i['Response']:
            d= yes
            d = added_element(d, i, 'count')
            yes = d
        elif 'Unknown' in i['Response']:
            d = unknown
            d = added_element(d, i, 'count')
            unknown = d
        else:
            print(i)
        d = total
        d = added_element(d, i, 'count')
        total = d
        

    
    gdata =[]
    gdata.append(yes)
    gdata.append(no)
    gdata.append(unknown)
    gdata.append(total)

    with open('gData.json', 'w', encoding='utf-8') as f:
        json.dump(gdata, f, ensure_ascii=False, indent=4)






