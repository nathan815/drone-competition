class Pilot:
    name = ""
    department = ""
    major = ""

    def __init__(self, name, department="", major=""):
        self.name = name
        self.department = department
        self.major = major

    def __str__(self):
        return "Name: " + self.name + \
               ("\nDepartment: " + self.department if self.department else "") + \
               ("\nMajor: " + self.major if self.major else "")
