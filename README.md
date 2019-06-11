# ubermovements
Uber Movement data meets OpenStreetMap

## Things you'll need
- pandas, numpy, osmnx, geopandas
- Uber Movements Segments to OSM Ways lookup and Speeds data for your area: [https://movement.uber.com/cities/<your city>/downloads/speeds?lang=en-US&tp[y]=<year>&tp[q]=<quarter>](https://movement.uber.com/cities/london/downloads/speeds?lang=en-US&tp[y]=<2018&tp[q]=4)
- somewhere to store the Uber data (for querying) - I used an MS Azure SQL database
- a shapefile/geojson of your city (for getting the right ways/nodes from OpenStreetMap) - I used London but it's too big to upload to GitHub.

## Caveats
This work assumes the speed limits detailed in OpenStreetMap are correct and up to date. This means some areas may be falsely flagged as speeding issues, and some might just be down-right wrong. 

Some ways have multiple speed limits listed. I've taken the largest limit provided (quick and dirty) but you could try to compare it to OS OpenRoads or similar to reach a consensus rather than taking a guess.

<img src="https://github.com/alex-drake/ubermovements/blob/master/plots/londonspeeds.png?raw=true" width="650">
<img src="https://github.com/alex-drake/ubermovements/blob/master/plots/centrallondonspeeds.png?raw=true" width="650">