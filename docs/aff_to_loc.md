To convert author affiliations to geographical locations using Python, you would typically need to utilize a geocoding service or an external API that can map the affiliation information to specific geographic coordinates.

Here's a general approach using the Geopy library and the OpenCage Geocoding API:

1. Install the Geopy library by running the following command:

```python
pip install geopy
```

2. Sign up for an account and obtain an API key from the OpenCage Geocoding service (https://opencagedata.com/) to access their geocoding API.

3. Import the necessary modules in your Python script:

```python
from geopy.geocoders import OpenCage
from geopy.exc import GeocoderTimedOut
```

4. Set up the OpenCage geocoder by providing your API key:

```python
geocoder = OpenCage('YOUR_API_KEY')
```

5. Define a function that takes an affiliation string as input and returns the corresponding geographic location:

```python
def get_geolocation(affiliation):
    try:
        location = geocoder.geocode(affiliation, timeout=10)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        return get_geolocation(affiliation)  # Retry if timeout occurs
    return None, None  # Return None if geolocation is not found
```

6. Iterate through your list of author affiliations and call the `get_geolocation()` function to convert each affiliation to a geographic location:

```python
affiliations = [...]  # Your list of author affiliations

for affiliation in affiliations:
    latitude, longitude = get_geolocation(affiliation)
    print(f"Affiliation: {affiliation}")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
    print()
```

Note that the geocoding process might not always yield accurate results, especially if the affiliation information is ambiguous or incomplete. Additionally, some geocoding services have usage limitations or require payment for large-scale usage, so be sure to review the terms and conditions of the chosen service.

Remember to replace `'YOUR_API_KEY'` with the actual API key obtained from OpenCage Geocoding service.

This is a basic example to get you started. Depending on the structure and format of the affiliation information you have, you may need to preprocess and clean the data to improve the geocoding results.

##  affiliation_parser
Simple python parser for MEDLINE, Pubmed OA affiliation string

Fast and simple parser for MEDLINE and Pubmed Open-Access affiliation string. We can parse multiple fields from the affiliation string including department, affiliation, location, country, email and zip code from affiliation text.

We also provide function to match affiliation string to [GRID](https://grid.ac/) dataset.


https://github.com/titipata/affiliation_parser