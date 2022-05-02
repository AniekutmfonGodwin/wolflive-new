import json
from game.models import GuessWhat





def export(file_path=None):
    data = []
    for gw in GuessWhat.objects.all():
        gw:GuessWhat
        data.append({
            "image_code":gw.image_code,
            "image_url":gw.image_url,
            "answer":gw.answer,
            "guess":gw.guess,
            "category":gw.category
        })
    with open("gwdb.json",mode="w") as f:
        json.dump(data,f)
