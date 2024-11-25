 
import os
import json
from .models import BodyPart, Symptom, Condition
from .helpers import getBodyPart, add_part, find_by_id

# Reads a given database of json files to retrieve an OOP database
def readDatabase(folder):
    symptomPath = os.path.sep.join((folder, 'symptoms'))
    conditionPaths = [
        os.path.sep.join((folder, 'conditions_part1')),
        os.path.sep.join((folder, 'conditions_part2'))
    ]

    partsPath = os.path.sep.join((folder, 'body_parts.json'))
    parts = []

    # Open the parts file
    with open(partsPath) as partsFile:
        partsObject = json.load(partsFile)
        for k, v in partsObject.items():
            add_part(parts, BodyPart(id=int(k), name=v))

    for symptomFilePath in os.listdir(symptomPath):
        part = getBodyPart(symptomFilePath)
        part = find_by_id(parts, int(part['id']))
        with open(os.path.sep.join((symptomPath, symptomFilePath))) as symptomFile:
            symptomsObject = json.load(symptomFile)
            for symptom in symptomsObject['data']['symptoms']:
                part.add_symptom(Symptom(id=symptom['id'], name=symptom['nm']))

    for conditionPath in conditionPaths:
        if os.path.exists(conditionPath):
            print(f"Accessing folder: {conditionPath}")
            for conditionsFilePath in os.listdir(conditionPath):
                if conditionsFilePath.endswith('.json'):
                    with open(os.path.sep.join((conditionPath, conditionsFilePath))) as conditionFile:
                        conditions = json.load(conditionFile)
                        if len(conditions['data']['conditions']) <= 0:
                            continue
                        symptoms = find_by_id(parts, int(conditions['meta']['bodypart']['id'])).symptoms()
                        symptom = find_by_id(symptoms, int(conditions['meta']['symptom'][0]['id']))
                        for condition in conditions['data']['conditions']:
                            if condition is not None:
                                symptom.add_condition(Condition(
                                    id=condition['id'],
                                    name=condition['name'],
                                    about=condition['curl']
                                ))
        else:
            print(f"Error: Folder not found at {conditionPath}")

    return parts
