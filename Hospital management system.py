import json
import os

class Patient:
    def __init__(self, patient_id, name, age, ailment):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.ailment = ailment

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "ailment": self.ailment
        }

    @staticmethod
    def from_dict(data):
        return Patient(data["patient_id"], data["name"], data["age"], data["ailment"])

class Hospital:
    DATA_FILE = "patients.txt"

    def __init__(self):
        self.patients = []
        self.load_patients()

    def load_patients(self):
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "r") as f:
                for line in f:
                    data = json.loads(line.strip())
                    self.patients.append(Patient.from_dict(data))

    def save_patients(self):
        with open(self.DATA_FILE, "w") as f:
            for patient in self.patients:
                f.write(json.dumps(patient.to_dict()) + "\n")

    def add_patient(self, name, age, ailment):
        patient_id = self._generate_patient_id()
        patient = Patient(patient_id, name, age, ailment)
        self.patients.append(patient)
        self.save_patients()
        print(f"Patient {name} added with ID {patient_id}.")

    def _generate_patient_id(self):
        if not self.patients:
            return 1
        return max(p.patient_id for p in self.patients) + 1

    def list_patients(self):
        for p in self.patients:
            print(f"ID: {p.patient_id}, Name: {p.name}, Age: {p.age}, Ailment: {p.ailment}")

    def search_patient_by_id(self, patient_id):
        for p in self.patients:
            if p.patient_id == patient_id:
                print(f"ID: {p.patient_id}, Name: {p.name}, Age: {p.age}, Ailment: {p.ailment}")
                return p
        print("Patient not found.")
        return None

    def delete_patient(self, patient_id):
        for i, p in enumerate(self.patients):
            if p.patient_id == patient_id:
                del self.patients[i]
                self.save_patients()
                print(f"Patient ID {patient_id} deleted.")
                return
        print("Patient not found.")

    def update_patient(self, patient_id, name=None, age=None, ailment=None):
        patient = self.search_patient_by_id(patient_id)
        if patient:
            if name:
                patient.name = name
            if age:
                patient.age = age
            if ailment:
                patient.ailment = ailment
            self.save_patients()
            print(f"Patient ID {patient_id} updated.")

# Example usage
if __name__ == "__main__":
    hospital = Hospital()
    hospital.add_patient("John Doe", 30, "Flu")
    hospital.add_patient("Jane Smith", 25, "Fracture")
    hospital.list_patients()
    hospital.search_patient_by_id(1)
    hospital.update_patient(1, age=31)
    hospital.delete_patient(2)
    while True:
        print("\nHospital Management System")
        print("1. Add Patient")
        print("2. List Patients")
        print("3. Search Patient by ID")
        print("4. Update Patient")
        print("5. Delete Patient")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter patient name: ")
            age = int(input("Enter patient age: "))
            ailment = input("Enter patient ailment: ")
            hospital.add_patient(name, age, ailment)
        elif choice == "2":
            hospital.list_patients()
        elif choice == "3":
            pid = int(input("Enter patient ID to search: "))
            hospital.search_patient_by_id(pid)
        elif choice == "4":
            pid = int(input("Enter patient ID to update: "))
            name = input("Enter new name (leave blank to keep unchanged): ")
            age_input = input("Enter new age (leave blank to keep unchanged): ")
            ailment = input("Enter new ailment (leave blank to keep unchanged): ")
            age = int(age_input) if age_input else None
            hospital.update_patient(pid, name=name if name else None, age=age, ailment=ailment if ailment else None)
        elif choice == "5":
            pid = int(input("Enter patient ID to delete: "))
            hospital.delete_patient(pid)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")