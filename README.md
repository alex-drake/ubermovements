# ubermovements
Uber Movement data meets OpenStreetMap to see if we can detect where the average Uber vehicle is breaking the speed limit, and by how much.

## Things you'll need
- Python 3.5 with pandas, numpy, osmnx, geopandas
- Uber Movements Segments to OSM Ways lookup and Speeds data for your area: [https://movement.uber.com/cities/<your city>/downloads/speeds?lang=en-US&tp[y]=<year>&tp[q]=<quarter>](https://movement.uber.com/cities/london/downloads/speeds?lang=en-US&tp[y]=<2018&tp[q]=4)
- somewhere to store the Uber data (for querying) - I used an MS Azure SQL database
- a shapefile/geojson of your city (for getting the right ways/nodes from OpenStreetMap) - I used London but it's too big to upload to GitHub.

## Speed Calculations
Uber only reports speeds for OSM ways where 5 or more Uber vehicles have been detected within that particular period (eg on that day, in the hour), and then provide a mean speed and standard deviation. Ideally they would also provide a vehicle count so mean speeds can be weighted appropriately, however, I've used 1/standard deviation to act as a weighting instead - this prevents a mean speed with high sd from skewing the calculated total average speed unless it is the only recording available. This is to suggest that we are less confident in mean speeds that have a high sd (any other suggestions, let me know!)

I've used speed data for June 2018, between the hours of 19:00-06:59 as this is when congestion is lower and so vehicle are 'more able' to speed.

Colour scheme is classic RAG status and shows:
- Grey: No data available (either no Uber data or no reported speed limit)
- Green: Average Uber vehicle travelling within reported speed limit
- Yellow: Average Uber vehicle travelling above reported speed limit, but within speed limit + 25% (eg 20-25 mph in a 20 zone)
- Red: Average Uber vehicle travelling above reported speed limit by at least speed limit + 25% (eg greater than 25 mph in a 20 zone)

## Caveats
This work assumes the speed limits detailed in OpenStreetMap are correct and up to date. This means some areas may be falsely flagged as speeding issues, and some might just be down-right wrong. 

Some ways have multiple speed limits listed. I've taken the largest limit provided (quick and dirty) but you could try to compare it to OS OpenRoads or similar to reach a consensus rather than taking a guess.

<img src="https://github.com/alex-drake/ubermovements/blob/master/plots/londonspeeds.png?raw=true" width="650">
<img src="https://github.com/alex-drake/ubermovements/blob/master/plots/centrallondonspeeds.png?raw=true" width="650">