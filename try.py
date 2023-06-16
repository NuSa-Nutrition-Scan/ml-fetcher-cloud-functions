import json
import os
from typing import Dict, List

import functions_framework
from cloudevents.http import CloudEvent
from google.cloud import firestore
from google.events.cloud import firestore as firestoredata
from gradio_client import Client

food_recommendation_api = "https://hakim571-food-recommendation.hf.space/"

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


r, t = get_predictions("UNT001", 20, 80, 180, 1800, "M", 3)

for e in r:
    e["img"] = "https://sdsds"

print(r)