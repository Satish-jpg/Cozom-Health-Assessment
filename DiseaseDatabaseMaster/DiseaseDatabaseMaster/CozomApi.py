# -*- coding: utf-8 -*-
import json
import requests
import urllib.parse

class CozomAPI(object):
    def __init__(self, protocol='http', host="symptoms.cozom.com", service="cozom/SymptomCheckerAPI.svc"):
        self.protocol = protocol
        self.host = host
        self.service = service

    def symptoms(self, bodypartid, age=20, gender="M"):
        url = self.make_endpoint('symptoms')
        payload = CozomAPI.make_request_body({"bodypartid": bodypartid}, age, gender)
        return CozomAPI.make_request(url, payload)

    def conditions(self, symptoms, age=20, gender="M", maxconditions=200):
        url = self.make_endpoint('conditions')
        payload = CozomAPI.make_request_body({"maxconditions": maxconditions, "bodyparts": symptoms}, age, gender)
        return CozomAPI.make_request(url, payload)

    def make_endpoint(self, endpoint):
        self.base = urllib.parse.urljoin(f"{self.protocol}://{self.host}/", self.service)
        return f"{self.base}/{endpoint}"

    @staticmethod
    def make_symptom(bodypartid, symptoms):
        return {"id": bodypartid, "symptoms": [{"id": symptomid, "qclss": []} for symptomid in symptoms]}

    @staticmethod
    def make_request_body(data, age, gender):
        body = {"locale": "in", "user": {"age": age, "gender": gender}}
        body.update(data)
        return {"request": body}

    @staticmethod
    def make_request(url, payload):
        response = requests.post(url, json=payload)
        response.encoding = "utf-8-sig"
        return response
