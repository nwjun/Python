import datetime
import requests
import time

url = "https://docs.google.com/forms/d/e/1FAIpQLSd0epowgODvaow9rNMHR5LfLrvK4pdbwrKKFuSzJGsiRHW08Q/formResponse"
#change viewform in url->formResponse

ic_no = ""
matriks_no = ""

def get_values():
    values_list = []
    a = input("Class code 1:")
    b = input("Class code 2:")
    deltatime = 0
    # no. of date ahead/behind of current date

    subjects_time = {
        "Tuesday": ["KULIAH", "TUTORIAL", "PRAKTIKAL"],
        "Wednesday": ["KULIAH"],
        "Friday": ["TUTORIAL"],
    }

    while True:
        now = datetime.date.today() + datetime.timedelta(days=deltatime)
        day_name = now.strftime("%A")
        # change current date to English word
        date = str(now).split("-")

        if day_name in subjects_time.keys():
            # add into list only if that day has class

            for i in subjects_time[day_name]:
                """keys are the value of 'name' element of the """

                values = {
                    # class code 1
                    "entry.1373291832": a,
                    # class code 2
                    "entry.472846005": b,
                    # ic
                    "entry.274958804": ic_no,
                    # matriks no
                    "entry.1997049463": matriks_no,
                    # subject
                    "entry.1051960764": "COMPUTER SCIENCE 1 SC015",
                    # Mod
                    "entry.1480241652": i,
                    # place
                    "entry.1965094254": "GL",
                    # year
                    "entry.286813345_year": date[0],
                    "entry.286813345_month": date[1],
                    "entry.286813345_day": date[2][0:2],
                }

                values_list.append(values)

        # last class in a week
        if day_name == "Friday":
            break
        else:
            deltatime += 1

    return values_list


def send_attendance(url, data):
    # send data to google form

    for d in data:
        try:
            requests.post(url, data=d)
            print("Form submitted.")
            time.sleep(5)
        except:
            print("Error Occured!")


final_data = get_values()
# print(len(final_data),final_data)
send_attendance(url, final_data)
