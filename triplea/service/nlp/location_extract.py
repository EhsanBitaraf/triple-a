import re

affiliation = "Department of Computer Science, University of California, Los Angeles"
location_pattern = r"([A-Za-z\s]*),\s*([A-Za-z\s]*),\s*([A-Za-z\s]*)$"

match = re.search(location_pattern, affiliation)
if match:
    city = match.group(1)
    state = match.group(2)
    country = match.group(3)

    print(f"City: {city}")
    print(f"State: {state}")
    print(f"Country: {country}")
else:
    print("No location information found in the affiliation.")
