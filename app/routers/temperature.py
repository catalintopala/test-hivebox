"""
Temperature endpoint module.
"""

import asyncio
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Literal

import aiohttp
from fastapi import APIRouter

sensebox_ids = [
    "652fe96f4a79360007bdeb16",
    "67212e5549d0900007b4061b",
    "629f9c0a87a60b001cdbcb8d",
    "660c4eef93fed60007512dc8",
    "6721358f49d0900007c04651",
    "65413ac9439231000734deb1",
    "67212e0449d0900007b37968",
    "672137c949d0900007c3fd52",
    "67212ddd49d0900007b3371f",
    "60a7d0bdddf854001b31622f",
    "65d4f21f578b6f00080f361a",
    "63616b12b950ed001bc6a968",
    "6541392443923100073233ee",
    "6615731cd03a3e00083f0cef",
    "6721605f49d090000707fe2e",
    "636166bc7b650f001be8ed9c",
    "65d4f2a4578b6f0008103452",
]

router = APIRouter()


@router.get("/temperature")
async def get_average_temperature():
    """
    Return average temperature based on all senseBox data.
    """
    total_boxes = 0
    total_temperatures = 0
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    sensebox_data = await fetch_sensebox_data(sensebox_ids)

    for response in sensebox_data:
        sensors = response.get("sensors", [])
        for sensor in sensors:
            if sensor["unit"] == "°C":
                last_measurement = sensor.get("lastMeasurement", {})
                measurement_time = last_measurement.get("createdAt")
                value = last_measurement.get("value")

                if measurement_time and value:
                    measurement_time = datetime.strptime(
                        measurement_time,
                        "%Y-%m-%dT%H:%M:%S.%fZ",
                    ).replace(tzinfo=timezone.utc)
                    if measurement_time >= one_hour_ago:
                        total_boxes += 1
                        total_temperatures += float(value)

    if total_boxes == 0:
        return {"error": "There is no data newer than 1 hour"}

    average_temperature = total_temperatures / total_boxes
    return {
        "average_temperature": average_temperature,
        "status": determine_status(average_temperature),
    }


async def fetch_sensebox_data(sensebox_ids: list[str]) -> list[dict]:
    """
    Asynchronously fetches data for a list of senseBox IDs from the OpenSenseMap API.

    This function sends concurrent GET request to the OpenSenseMap API to fetch data for each senseBox ID in the provided list. It gathers the results and returns them as a list of JSON responses, one for each valid senseBox.

    Args:
        sensebox_ids (list[str]): A list of senseBox IDs for which data retrieval is requested.

    Returns:
        list[dict]: A list of dictionaries containing the JSON response data for each senseBox, or an empty list if no data is retrieved.

    Notes:
        - If a request fails (i.e., status code is not 200), an error message is printed, and the corresponding data is excluded from the response.
        - The timeout for each API call is set to 100 seconds.
    """
    request_timeout = aiohttp.ClientTimeout(total=100)
    json_responses = []

    try:
        async with aiohttp.ClientSession(timeout=request_timeout) as session:
            session_list = []
            for sensebox_id in sensebox_ids:
                api_url = f"https://api.opensensemap.org/boxes/{sensebox_id}"
                session_list.append(session.get(api_url))

            responses = await asyncio.gather(*session_list)
            for response in responses:
                if response.status == 200:
                    json_responses.append(response.json())

            json_responses = await asyncio.gather(*json_responses)
    except aiohttp.ClientError as err:
        print(f"Client error: {err}")
        return {"status": 500, "error": "Failed to fetch SenseBox"}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"status": 500, "error": "Failed to fetch SenseBox"}

    return json_responses


def determine_status(
    average_temperature: float,
) -> Literal["Too Cold", "Good", "Too Hot"]:
    """
    Generates a temperature status message based on the average temperature.

    Args:
        average_temperature (float): The average temperature value to assess.

    Returns:
        str:
            A message indicating the temperature status:
            - "Too Cold" if the temperature is below 10
            - "Good" if the temperature is between 10 and 36 (inclusive)
            - "Too Hot" if the temperature exceeds 37

    """
    if average_temperature < 10:
        return "Too Cold"
    if average_temperature <= 36:
        return "Good"
    return "Too Hot"
