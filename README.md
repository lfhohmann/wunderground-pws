[![](https://img.shields.io/badge/MAINTAINER-%40lfhohmann-blue?style=for-the-badge)](https://github.com/lfhohmann)
[![](https://img.shields.io/github/license/lfhohmann/codewars-katas?style=for-the-badge)](LICENSE)

# Wunderground PWS Scraper
Simple web scraping with Beaultiful Soup on Wunderground Personal Weather Stations (PWS) without API key. This script allows multiple station IDs to be specified and it will average the results based on last updated time, so more recently updated stations will have a higher weight on the average calculation.

## config variable

The config variable takes the following parameters:

+ **units:** (Dictionary)(Required)
  + The default units for the returned values.
    + **temp:** (String)(Required)
      + The temperature unit.
        + `"c"`: Celsius
        + `"f"`: Farenheit
    + **pressure:** (String)(Required)
      + The pressure unit.
        + `"hpa"`: Hectopascals
        + `"in"`: Inches of mercury
    + **speed:** (String)(Required)
      + The wind speed unit.
        + `"kmph"`: Kilometers per Hour
        + `"mph"`: Miles per Hour
        + `"mps"`: Meters per Second
    + **precip:** (String)(Required)
      + The rain precipitation unit.
        + `"mm"`: Milimeters
        + `"in"`: Inches
+ **stations:** (List)(Required)
  + A list of the desired stations and its parameters.
    + **id:** (String)(Required)
      + The station id from the Wunderground website.
    + **parameters:** (List)(Required)
      + A list of optional parameters to be scraped.
        + **`"temp"`:** (String)(Optional)
          + Temperature reading of the weather station.
        + **`"wind_speed"`:** (String)(Optional)
          + Wind Speed reading of the weather station.
        + **`"wind_gust"`:** (String)(Optional)
          + Wind Gust Speed reading of the weather station.
        + **`"wind_bearing"`:** (String)(Optional)
          + Wind Bearing reading of the weather station.
        + **`"pressure"`:** (String)(Optional)
          + Barometric Pressure reading of the weather station.
        + **`"humidity"`:** (String)(Optional)
          + Humidity reading of the weather station.
        + **`"precip_rate"`:** (String)(Optional)
          + Precipitation Rate reading of the weather station.
        + **`"precip_total"`:** (String)(Optional)
          + Accumulated Precipitation reading of the weather station.
        + **`"uv_index"`:** (String)(Optional)
          + UV Index reading of the weather station.
        + **`"radiation"`:** (String)(Optional)
          + Solar radiation reading of the weather station in Watts per squared meter.

#
[![Buy me a coffe!](https://www.buymeacoffee.com/assets/img/custom_images/black_img.png)](https://www.buymeacoffee.com/lfhohmann)
