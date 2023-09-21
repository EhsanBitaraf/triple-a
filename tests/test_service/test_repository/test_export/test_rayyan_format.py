from triplea.service.repository.export.rayyan_format import export_rayyan_csv



# Exporting a CSV file with at least one article containing the word "biobank" or "Biobank".
def test_export_csv_with_one_article_containing_biobank(self, mocker):
    # Mocking the persist.get_all_article_pmid_list() function to return a list with one article
    mocker.patch('triplea.service.repository.persist.get_all_article_pmid_list', return_value=[1])

    # Mocking the persist.get_article_by_pmid() function to return an article with the word "biobank" in the title
    mocker.patch('triplea.service.repository.persist.get_article_by_pmid', return_value={'Title': 'Biobank Article'})

    # Mocking the logger.DEBUG() function to check if it is called with the correct message
    mock_debug = mocker.patch('triplea.service.click_logger.logger.DEBUG')

    # Calling the export_rayyan_csv() function
    result = export_rayyan_csv()

    # Asserting that the logger.DEBUG() function was called with the correct message
    mock_debug.assert_called_with('1 Article(s) Selected.')

    # Asserting that the result is not empty
    assert result != ''

    # Asserting that the result contains the correct CSV header
    assert 'key,title,authors,issn,volume,issue,pages,year,publisher,url,abstract,notes,doi,keywords' in result

    # Asserting that the result contains the correct CSV row for the article
    assert '1,Biobank Article,,,,,,,https://pubmed.ncbi.nlm.nih.gov/1/,,,,' in result