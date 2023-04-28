import requests
import config
from datetime import datetime

GENDER = "male"
WEIGHT = 88
HEIGHT = 185
AGE = 40

USERNAME = config.USER
PROJECT_NAME = config.PROJECT
SHEETY_NAME = config.SHEETY


def write_to_sheety(result: dict) -> None:
    sheet_endpoint = f'https://api.sheety.co/{USERNAME}/{PROJECT_NAME}/{SHEETY_NAME}'

    today_date = datetime.now().strftime("%d/%m/%Y")
    now_time = datetime.now().strftime("%X")

    headers = {
        'Authorization': f'Basic {config.Authorization}',
    }

    # [exercises.get("name"), exercises.get('duration_min'), exercises.get("nf_calories")]
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

        sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=headers)

        print(sheet_response.text)


def get_calories(user_response: str) -> dict:
    nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

    nutritionix_headers = {
        'x-app-id': config.APP_ID,
        'x-app-key': config.API_KEY,
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
    # print(response.json())
    exercises = response.json()
    return exercises


def main():
    exercise_and_calories = get_calories(user_response=input("What do yuo do today!\n"))
    print(exercise_and_calories)
    write_to_sheety(exercise_and_calories)


if __name__ == '__main__':
    main()
