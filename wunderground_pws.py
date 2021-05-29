from bs4 import BeautifulSoup as bs
import requests
import math

"""
TODO
    Standard deviation calculation
    Calculate weight based on distance
    Add 3 weights (User set, distance, last_updated)
    Add wind bearing last_updated weights
"""


def process(config):
    def scrape(station, units):
        USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        LANGUAGE = "en-US,en;q=0.5"
        URL = "https://www.wunderground.com/dashboard/pws/"

        try:
            session = requests.Session()
            session.headers["User-Agent"] = USER_AGENT
            session.headers["Accept-Language"] = LANGUAGE
            session.headers["Content-Language"] = LANGUAGE
            html = session.get(URL + station["id"])

            soup = bs(html.text, "html.parser")
        except:
            return None

        if (
            soup.findAll("span", attrs={"_ngcontent-app-root-c173": ""})[21].text
            == "Online"
        ):
            data = {}

            # Last updated value
            data["LAST_UPDATED"] = soup.findAll(
                "span", attrs={"class": "ng-star-inserted"}
            )[0].text

            strings = data["LAST_UPDATED"].split()
            if (strings[0] == "(updated") and (strings[3] == "ago)"):
                value = int(strings[1])

                if (value >= 0) and (value <= 60):
                    if strings[2][0:6] == "second":
                        data["LAST_UPDATED"] = 1 / value

                    elif strings[2][0:6] == "minute":
                        data["LAST_UPDATED"] = 1 / (value * 60)

                    elif strings[2][0:4] == "hour":
                        if (value >= 0) and (value <= 24):
                            data["LAST_UPDATED"] = 1 / (value * 3600)

                        else:
                            return None

                    else:
                        return None

                else:
                    return None

            # Get Temperature
            if "temp" in station["parameters"]:
                data["temp"] = soup.find("span", attrs={"class": "wu-value"})
                data["temp"] = round(float(data["temp"].text))

                if units["temp"] == "c":
                    data["temp"] = round((data["temp"] - 32) * (5 / 9), 1)

            # Get Wind Speed
            if "wind_speed" in station["parameters"]:
                data["wind_speed"] = soup.findAll("span", attrs={"class": "wu-value"})
                data["wind_speed"] = round(float(data["wind_speed"][2].text), 1)

                if units["speed"] == "kmph":
                    data["wind_speed"] = round(data["wind_speed"] * 1.6, 1)

                elif units["speed"] == "mps":
                    data["wind_speed"] = round(data["wind_speed"] * (4 / 9), 1)

            # Get Wind Gust
            if "wind_gust" in station["parameters"]:
                data["wind_gust"] = soup.findAll("span", attrs={"class": "wu-value"})
                data["wind_gust"] = round(float(data["wind_gust"][3].text), 1)

                if units["speed"] == "kmph":
                    data["wind_gust"] = round(data["wind_gust"] * 1.6, 1)

                elif units["speed"] == "mps":
                    data["wind_gust"] = round(data["wind_gust"] * (4 / 9), 1)

            # # Get Wind Direction
            # if "wind_direction" in station["parameters"]:
            #     data["wind_direction"] = soup.find(
            #         "span", attrs={"class": "text-bold"}
            #     ).text

            # Get Wind Bearing
            if "wind_bearing" in station["parameters"]:
                data["wind_bearing"] = soup.find(
                    "div", attrs={"class": "arrow-wrapper"}
                )

                string_full = ((data["wind_bearing"]["style"]).split())[1]
                string_start = string_full[0:7]
                string_end = string_full[-5:-1]

                if (string_start == "rotate(") and (string_end == "deg)"):
                    data["wind_bearing"] = int(string_full[7:-5]) - 180
                else:
                    data["wind_bearing"] = None

            # Get Precipitation Rate
            if "precip_rate" in station["parameters"]:
                data["precip_rate"] = soup.findAll("span", attrs={"class": "wu-value"})
                data["precip_rate"] = round(float(data["precip_rate"][5].text), 2)

                if units["precip"] == "mm":
                    data["precip_rate"] = round(data["precip_rate"] * 25.4, 2)

            # Get Precipitation Total
            if "precip_total" in station["parameters"]:
                data["precip_total"] = soup.findAll("span", attrs={"class": "wu-value"})
                data["precip_total"] = round(float(data["precip_total"][8].text), 2)

                if units["precip"] == "mm":
                    data["precip_total"] = round(data["precip_total"] * 25.4, 2)

            # Get Pressure
            if "pressure" in station["parameters"]:
                data["pressure"] = soup.findAll("span", attrs={"class": "wu-value"})
                data["pressure"] = round(float(data["pressure"][6].text), 2)

                if units["pressure"] == "hpa":
                    data["pressure"] = round(data["pressure"] * 33.86, 2)

            # Get Humidity
            if "humidity" in station["parameters"]:
                data["humidity"] = soup.findAll("span", attrs={"class": "wu-value"})
                data["humidity"] = round(float(data["humidity"][7].text))

            # Get UV Index
            if "uv_index" in station["parameters"]:
                data["uv_index"] = soup.findAll("span", attrs={"class": "wu-value"})
                data["uv_index"] = round(float(data["uv_index"][9].text))

            # Get Solar Radiation
            if "radiation" in station["parameters"]:
                data["radiation"] = soup.findAll(
                    "div", attrs={"class": "weather__text"}
                )
                strings = data["radiation"][-1].text.split()

                if strings[1][-8:-3] == "watts":
                    data["radiation"] = round(float(strings[0]), 1)
                else:
                    data["radiation"] = None

        station["data"] = data
        return station

    stations = []
    avg_values = {}
    for station in config["stations"]:
        stations.append(scrape(station, config["units"]))

    # Get average values, except wind bearing and wind direction
    for parameter in [
        "temp",
        "wind_speed",
        "wind_gust",
        "pressure",
        "humidity",
        "precip_rate",
        "precip_total",
        "uv_index",
        "radiation",
    ]:
        last_updated_total = 0
        for station in stations:
            if parameter in station["data"] and station["data"][parameter] != None:
                last_updated_total += station["data"]["LAST_UPDATED"]

        avg_values[parameter] = 0
        for station in stations:
            if parameter in station["data"] and station["data"][parameter] != None:
                last_updated_weight = (
                    station["data"]["LAST_UPDATED"] / last_updated_total
                )
                avg_values[parameter] += (
                    last_updated_weight * station["data"][parameter]
                )

        avg_values[parameter] = round(avg_values[parameter], 2)

    # Get average wind bearing
    winds = []
    wind_vectors = []
    for station in stations:
        if (
            "wind_bearing" in station["data"]
            and station["data"]["wind_bearing"] != None
        ):
            winds.append(
                (station["data"]["wind_bearing"], station["data"]["wind_speed"])
            )

    for i, wind in enumerate(winds):
        wind_vectors.append([None, None])
        wind_vectors[i][0] = math.sin(math.radians(wind[0])) * wind[1]
        wind_vectors[i][1] = math.cos(math.radians(wind[0])) * wind[1]

    avg_x, avg_y = 0, 0
    for wind_vector in wind_vectors:
        avg_x += wind_vector[0]
        avg_y += wind_vector[1]

    avg_values["wind_bearing"] = round(math.degrees(math.atan2(avg_x, avg_y)))
    avg_values["wind_speed"] = round(
        math.sqrt(avg_x ** 2 + avg_y ** 2) / len(wind_vectors), 2
    )

    if avg_values["wind_bearing"] < 0:
        avg_values["wind_bearing"] += 360

    return avg_values


if __name__ == "__main__":
    config = {
        "units": {
            "temp": "c",
            "pressure": "hpa",
            "speed": "kmph",
            "precip": "mm",
        },
        "stations": [
            {
                "id": "ICURITIB24",
                "parameters": [
                    "temp",
                    "wind_speed",
                    "wind_gust",
                    "wind_bearing",
                    "pressure",
                    "humidity",
                    "precip_rate",
                    "precip_total",
                    "uv_index",
                    "radiation",
                ],
            },
            {
                "id": "ICURITIB28",
                "parameters": [
                    "temp",
                    "wind_speed",
                    "wind_gust",
                    "wind_bearing",
                    "pressure",
                    "humidity",
                    "precip_rate",
                    "precip_total",
                    "uv_index",
                    "radiation",
                ],
            },
            {
                "id": "IPRCURIT2",
                "parameters": [
                    "temp",
                    "wind_speed",
                    "wind_gust",
                    "wind_bearing",
                    "pressure",
                    "humidity",
                    "precip_rate",
                    "precip_total",
                ],
            },
        ],
    }

    for k, v in process(config).items():
        print(f"{k}\t{v}")
