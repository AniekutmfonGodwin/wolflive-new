import json
from storage.models import GuessWhat





def import_data(file_path=None):
    data = []
    with open("gwdb.json",mode="r") as f:
        data = json.load(f)
    db_data = []
    for d in data:

        db_data.append(GuessWhat(
            **{
            "image_code":d.get("image_code"),
            "image_url":d.get("image_url"),
            "answer":d.get("answer"),
            "guess":d.get("guess"),
            "category":d.get("category")
        }
        ))
    GuessWhat.objects.bulk_create(db_data)
        