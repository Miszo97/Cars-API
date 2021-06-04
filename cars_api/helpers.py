import json

import requests


def exists_in_nhtsa(make, model):
    """
    Checks if a car with a given car make and model exists in NHTSA database
    """
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{}?format=json".format(
        make
    )

    response = requests.get(url)
    cars = json.loads(response.text)["Results"]

    for car in cars:
        if (
            car["Make_Name"].lower() == make.lower()
            and car["Model_Name"].lower() == model.lower()
        ):
            return True

    return False
