from triplea.schemas.article import Author


def _json_converter_author_general(author: Author):
    fullname = ""

    fullname = author.FullName

    affiliation_list = []
    if author.Affiliations is not None:
        for one_aff in author.Affiliations:
            # first_aff = author.Affiliations[0]
            department = ""
            hospital = ""
            institute = ""
            country = ""
            university = ""
            center = ""
            location = ""
            email = ""
            zipcode = ""

            if one_aff.Structural is not None:
                for s in one_aff.Structural:
                    if "department" in s:
                        department = s["department"]
                    elif "hospital" in s:
                        hospital = s["hospital"]
                    elif "institute" in s:
                        institute = s["institute"]
                    elif (
                        "institution" in s
                    ):  # aff.ParseMethod = AffiliationParseMethod.TITIPATA_API  # noqa: E501
                        institute = s["institution"]
                    elif "country" in s:
                        country = s["country"]
                    elif "university" in s:
                        university = s["university"]
                    elif "center" in s:
                        center = s["center"]

                    elif (
                        "location" in s
                    ):  # aff.ParseMethod = AffiliationParseMethod.TITIPATA_API  # noqa: E501
                        location = s["location"]
                    elif (
                        "email" in s
                    ):  # aff.ParseMethod = AffiliationParseMethod.TITIPATA_API  # noqa: E501
                        email = s["email"]
                    elif (
                        "zipcode" in s
                    ):  # aff.ParseMethod = AffiliationParseMethod.TITIPATA_API  # noqa: E501
                        zipcode = s["zipcode"]

                    else:
                        print(s)
            aff = one_aff.Text

            affiliation_list.append(
                {
                    "text": aff,
                    "country": country,
                    "university": university,
                    "location": location,
                    "center": center,
                    "institute": institute,
                    "department": department,
                    "hospital": hospital,
                    "email": email,
                    "zipcode": zipcode,
                }
            )

    else:
        aff = None

    return {"fullname": fullname, "affiliations": affiliation_list}
