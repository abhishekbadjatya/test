1. The requirements.txt tells about the dependencies required
2. The config.py file defines the config values. It expects the absolute full path of the file cities1000.txt and the elasticsearch host url
3. parseAndDump.py file reads the input file parses it and stores the required data in elasticsearch in two different indexes.
	a) the cities index contains documents for each of the city data
	b) country_code index is for storing all the unique country codes
4. the application.py defines 3 different routes:
	a) /cities/proximity route takes latitude, longitude, size and country_code as query params. Based on that it will search all the docs in the elasticsearch based on cities in 10000km radius of the given lat, lon values. It will filter the docs corresponding to selected country code. (If ANYWHERE is selected in country_code it will not restrict based on country codes). Then it will sort the data based on distance and give the required number (defined by size) of city details

	b) /cities/lexical gives the city list based on the input keywords. it will treat each word (separated by space) as a separate keyword and perform an 'OR' query and list out the cities.

	c) /countries route is required to populate the drop down of the country codes on the UI.

I have run this on localhost environment with the elasticsearch and flask server both running locally.

I went ahead with elasticsearch as it provided me with all the capabilities required in the program.

The code has been tested for Python 2.7 and ELasticsearch version 5.6.3