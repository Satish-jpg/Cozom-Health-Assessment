# cozom_api.py - Custom implementation for COZOM's Symptoms Checker API
import json
import os

class COZOMAPI(object):
    def __init__(self, data_folder='data'):
        """
        Initialize the COZOM API to interact with local data.
        Args:
            data_folder (str): The folder where data JSON files are stored.
        """
        self.data_folder = data_folder

    def symptoms(self, bodypartid, age=20, gender="M"):
        """
        Retrieve symptoms based on the body part ID from local JSON data.
        Args:
            bodypartid (int): ID of the body part.
        Returns:
            list: List of symptoms for the given body part.
        """
        symptoms_file_path = os.path.join(self.data_folder, "symptoms", f"{bodypartid}.json")
        try:
            with open(symptoms_file_path, 'r') as file:
                symptoms_data = json.load(file)
                return symptoms_data.get("symptoms", [])
        except FileNotFoundError:
            print(f"No symptoms found for body part ID {bodypartid}.")
            return []

    def conditions(self, symptoms, age=20, gender="M", maxconditions=200):
        """
        Retrieve possible conditions based on the given symptoms from local JSON data.
        Args:
            symptoms (list): List of symptom IDs.
            maxconditions (int): Maximum number of conditions to retrieve.
        Returns:
            list: List of possible conditions based on the given symptoms.
        """
        conditions = []
        try:
            for symptom_id in symptoms:
                condition_file_path = os.path.join(self.data_folder, "conditions", f"{symptom_id}.json")
                with open(condition_file_path, 'r') as file:
                    condition_data = json.load(file)
                    conditions.extend(condition_data.get("conditions", []))

            # Limit the number of conditions based on maxconditions
            return conditions[:maxconditions]
        except FileNotFoundError:
            print(f"No conditions found for given symptoms.")
            return []

    def make_symptom(self, bodypartid, symptoms):
        """
        Create a dictionary structure to represent symptoms linked to a body part.
        Args:
            bodypartid (int): The ID of the body part.
            symptoms (list): List of symptom IDs.
        Returns:
            dict: A dictionary representation of symptoms for the given body part.
        """
        return {"id": bodypartid, "symptoms": [{"id": symptom_id, "qclss": []} for symptom_id in symptoms]}

# Example usage
if __name__ == "__main__":
    api = COZOMAPI()
    # Example to retrieve symptoms for a body part
    body_part_id = 1
    symptoms = api.symptoms(body_part_id)
    print(f"Symptoms for body part {body_part_id}: {symptoms}")

    # Example to retrieve possible conditions for symptoms
    symptoms_list = [101, 102]  # Example symptom IDs
    conditions = api.conditions(symptoms_list)
    print(f"Possible conditions for given symptoms: {conditions}")
