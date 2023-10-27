from src.regions.models import Country, City
from src.regions.schemas import RegionsRead, CityRead

from typing import List


def get_all_regions_from_db() -> List[RegionsRead]:
    query_countries = Country.select().order_by(Country.name)

    all_regions = []

    for country in query_countries:
        query_cities = (
            City.select().where(City.country_id == country.id).order_by(City.name)
        )

        cities = []

        for city in query_cities:
            cities.append(
                CityRead(
                    id=city.id,
                    name=city.name,
                    latitude=city.latitude,
                    longitude=city.longitude,
                )
            )

        region = RegionsRead(id=country.id, name=country.name, cities=cities)

        all_regions.append(region)

    return all_regions
