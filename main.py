import json
import os
from typing import Dict, List

import functions_framework
from cloudevents.http import CloudEvent
from google.cloud import firestore
from google.events.cloud import firestore as firestoredata
from gradio_client import Client

food_recommendation_api = os.getenv("FOOD_RECOMMENDATION_API")


def get_predictions(
    uid: str,
    age: int,
    weight: int,
    height: int,
    cal_need: int,
    gender: str,
    amount_of_eat: int,
) -> tuple:
    client = Client(food_recommendation_api)
    result = client.predict(
        uid, age, weight, height, cal_need, gender, amount_of_eat, fn_index=0
    )

    top15_path, recom_path = result

    top15_result: List[Dict[str, str]] = []
    recom_result: List[Dict[str, str]] = []

    with open(top15_path, "r") as f1:
        top15 = json.load(f1)
        for data in top15["data"]:
            top15_result.append(
                {
                    "id": data[1],
                    "name": data[2],
                }
            )

    f1.close()

    with open(recom_path, "r") as f2:
        recom = json.load(f2)
        headers = recom["headers"]

        for i in range(20):
            t: Dict[str, str] = {}
            for j in range(len(headers)):
                t[headers[j]] = recom["data"][i][j]

            recom_result.append(t)

        print(recom_result)

    f2.close()

    os.remove(top15_path)
    os.remove(recom_path)

    return (top15_result, recom_result)


@functions_framework.cloud_event
def update_food_recommendation(event: CloudEvent) -> None:
    client = firestore.Client()

    payload = firestoredata.DocumentEventData()
    payload._pb.ParseFromString(event.data)

    user_id = payload.value.name.split("/")[-1]

    ml_id = payload.value.fields["ml_id"].string_value
    age = payload.value.fields["age"].integer_value
    weight = payload.value.fields["weight"].integer_value
    calories_target = payload.value.fields["calories_target"].integer_value
    height = payload.value.fields["height"].integer_value
    sex = payload.value.fields["sex"].string_value

    top15_2, recom_2 = get_predictions(
        ml_id, age, weight, height, calories_target, sex, 2
    )
    top15_3, recom_3 = get_predictions(
        ml_id, age, weight, height, calories_target, sex, 3
    )
    top15_4, recom_4 = get_predictions(
        ml_id, age, weight, height, calories_target, sex, 4
    )

    ref = client.collection("food_recommendation").document(user_id)
    ref.set(
        {
            "2x": {
                "top15": top15_2,
                "recom": recom_2,
            },
            "3x": {
                "top15": top15_3,
                "recom": recom_3,
            },
            "4x": {
                "top15": top15_4,
                "recom": recom_4,
            },
        }
    )
