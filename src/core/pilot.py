class Pilot:
    name = ""
    department = ""
    major = ""
    school = ""

    def __init__(self, name, department="", major="", school=""):
        self.name = name
        self.department = department
        self.major = major
        self.school = school

    def __str__(self):
        return self.name + \
               (" " + self.department if self.department else "") + \
               (" " + self.major if self.major else "") + \
               (" " + self.school if self.school else "")
