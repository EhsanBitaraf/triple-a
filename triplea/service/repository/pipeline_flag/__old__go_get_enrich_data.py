

# def model_altmetric_by_doi(article, overwrite = False):
#     if article.DOI is not None:
#         data = get_altmetric("10.1038/nphys1170", id_type="doi")
#         if article.EnrichedData is None:
#             article.EnrichedData = {}

#         if 'altmetric' in article.EnrichedData:
#             if overwrite:
#                 article.EnrichedData['altmetric'] = {
#                         "date": datetime.now(),
#                         "data": data
#                                     }
#                 return article
#             else:
#                 return None                 
#         else:
#             article.EnrichedData['altmetric'] = {
#                                             "date": datetime.now(),
#                                             "data": data
#                                                         }
#             return article
#     else:
#         return None
    
# def go_get_enrich_data(model, overwrite = False):
#     max_refresh_point = SETTINGS.AAA_CLI_ALERT_POINT
#     l_id = persist.get_all_article_id_list()
#     total_article = len(l_id)
#     n = 0
#     logger.DEBUG(f" {len(l_id)} Article(s) ")

#     tqdm = get_tqdm()
#     bar = tqdm(total=len(l_id), desc="Processing ")
#     refresh_point = 0
#     for id in l_id:
#         try:
#             n = n + 1
#             updated = False

#             if refresh_point == max_refresh_point:
#                 refresh_point = 0
#                 persist.refresh()
#                 print()
#                 logger.DEBUG(f"There are {str(total_article - n)} article(s) left ")
#             else:
#                 refresh_point = refresh_point + 1

#             a = persist.get_article_by_id(id)
#             try:
#                 updated_article = Article(**a.copy())
#             except Exception:
#                 print()
#                 print(logger.ERROR(f"Error in parsing article with ID = {id}"))
#                 raise Exception("Article Not Parsed.")



#             if model=="altmetric_by_doi":
#                 bar.set_description(f"Article {id} enrich with altmetric")
#                 updated_article = model_altmetric_by_doi(updated_article)
#                 if updated_article is not None:
#                     persist.update_article_by_id(updated_article, id)
#             elif model == "altmetric_by_pmid":
#                 pass # ....
            
#             else:
#                 raise Exception("model not recognised.")


#             bar.update(1)
#         except Exception:
#                 print_error()

#     persist.refresh()
#     bar.close()

