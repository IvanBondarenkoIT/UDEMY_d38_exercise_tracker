import os
import requests
from datetime import datetime

GENDER = "male"
WEIGHT = 88
HEIGHT = 185
AGE = 40


USERNAME = os.environ.get("USER")
PROJECT_NAME = os.environ.get("PROJECT")
SHEETY_NAME = os.environ.get("SHEETY")

SHEET_PASSWORD = os.environ.get("Authorization")
APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")


def write_to_sheety(result: dict) -> None:
    sheet_endpoint = f'https://api.sheety.co/{USERNAME}/{PROJECT_NAME}/{SHEETY_NAME}'

    today_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")

    bearer_headers = {
        'Authorization': f'Bearer {SHEET_PASSWORD}',
    }

    for exercise in result["exercises"]:
        sheet_inputs = {
            "workout": {
                "date": today_date,
                "time": now_time,
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            }
        }

        sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=bearer_headers)

        print(sheet_response.text)


def get_calories(user_response: str) -> dict:
    nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

    nutritionix_headers = {
        'x-app-id': APP_ID,
        'x-app-key': API_KEY,
    }

    nutritionix_config = {
        "query": user_response,
        "gender": GENDER,
        "weight_kg": WEIGHT,
        "height_cm": HEIGHT,
        "age": AGE
    }

    response = requests.post(url=nutritionix_endpoint,
                             json=nutritionix_config,
                             headers=nutritionix_headers)

    exercises = response.json()
    return exercises


def main(user_response):
    exercise_and_calories = get_calories(user_response=user_response)
    print(exercise_and_calories)
    write_to_sheety(exercise_and_calories)


if __name__ == '__main__':
    user_answer = input("What do yuo do today!\n")
    # user_answer = "Run 15 km swim 5 km"
    main(user_answer)
