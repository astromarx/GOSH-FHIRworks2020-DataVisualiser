from fhir_parser.fhir import FHIR
import matplotlib.pyplot as plotter

"""
Eduardo Battistini, SN 17001483
March 23, 2020

GOSH FHIR Task Submission

This project makes use of the fhir_parser library (available under Apache License 2.0). 

"""


class DataVisualiser:
    """Analyse and visualize medical demographics based on patient database"""
    endpoint = None

    def __init__(self):
        self.endpoint = FHIR()
        self.weights = []
        self.bmis = []
        self.heart_rates = []
        self.respiratory_rates = []
        self.sample_size = 600

    def go(self):
        self.retrieve_data()
        self.plot()

    def retrieve_data(self):
        """ Retrieves data from FHIR API """
        patients = self.endpoint.get_all_patients()
        patients = patients[:self.sample_size]

        i = 0
        for patient in patients:
            print(i)
            i = i + 1
            observations = self.endpoint.get_patient_observations(patient.get_uuid())
            self.collect_relevant_metrics(patient.birthdate(), patient.get_gender(), observations)

    def collect_relevant_metrics(self, birthdate, gender, observations):
        """ Collects desired metrics from patient observation data """
        for observation in observations:
            if observation.get_type() != 'vital-signs':
                pass
            else:
                metric = observation.components[0].get_display()
                value = observation.components[0].get_value()
                age = get_age(birthdate, observation.get_date())

                if metric == 'Body Weight':
                    self.weights.append([age, value, gender])
                if metric == 'Body Mass Index':
                    self.bmis.append([age, value, gender])
                if metric == 'Heart rate':
                    self.heart_rates.append([age, value, gender])
                if metric == 'Respiratory rate':
                    self.respiratory_rates.append([age, value, gender])

    def plot(self):
        """ Plots analysed results using matplotlib library"""
        plotter.figure(figsize=(300, 150))

        ax = plotter.subplot(221)
        x1, y1 = analyze_data(self.weights, 'male')
        x2, y2 = analyze_data(self.weights, 'female')
        ax.plot(x1, y1, label='Male')
        ax.plot(x2, y2, label='Female')
        ax.set(xlabel='age (yrs)', ylabel='Weight (kg)',
               title='Average Weight per Age (Sample Size: ' + str(self.sample_size) + ')')
        ax.legend(loc='upper left')
        ax.grid()

        ax = plotter.subplot(222)
        x1, y1 = analyze_data(self.bmis, 'male')
        x2, y2 = analyze_data(self.bmis, 'female')
        ax.plot(x1, y1, label='Male')
        ax.plot(x2, y2, label='Female')
        ax.set(xlabel='age (yrs)', ylabel='Weight (kg)',
               title='Average BMI per Age (Sample Size: ' + str(self.sample_size) + ')')
        ax.legend(loc='upper left')
        ax.grid()

        ax = plotter.subplot(223)
        x1, y1 = analyze_data(self.heart_rates, 'male')
        x2, y2 = analyze_data(self.heart_rates, 'female')
        ax.plot(x1, y1, label='Male')
        ax.plot(x2, y2, label='Female')
        ax.set(xlabel='age (yrs)', ylabel='Weight (kg)',
               title='Average Heart Rate per Age (Sample Size: ' + str(self.sample_size) + ')')
        ax.legend(loc='upper left')
        ax.grid()

        ax = plotter.subplot(224)
        x1, y1 = analyze_data(self.respiratory_rates, 'male')
        x2, y2 = analyze_data(self.respiratory_rates, 'female')
        ax.plot(x1, y1, label='Male')
        ax.plot(x2, y2, label='Female')
        ax.set(xlabel='age (yrs)', ylabel='Weight (kg)',
               title='Average Respiratory Rate per Age (Sample Size: ' + str(self.sample_size) + ')')
        ax.legend(loc='upper left')
        ax.grid()

        plotter.show()


COUNT = 0
SUM = 1

AGE = 0
VALUE = 1
GENDER = 2


def get_age(birthdate, observation_date):
    """ calculates de age of patients at time of observation"""

    o_year = int(observation_date[0:4])
    o_month = int(observation_date[5:7])
    o_day = int(observation_date[8:10])

    b_year = int(birthdate[0:4])
    b_month = int(birthdate[5:7])
    b_day = int(birthdate[8:10])

    return o_year - b_year - ((o_month, o_day) < (b_month, b_day))


def analyze_data(dataset, gender):
    """ computes averages from datasets """
    sample_ages = []
    sums_per_age = []

    for i in range(110):
        sums_per_age.append([0, 0])

    for entries in dataset:
        if entries[GENDER] != gender:
            pass
        else:
            if entries[AGE] not in sample_ages:
                sample_ages.append(entries[AGE])

            sums_per_age[entries[AGE]][COUNT] = sums_per_age[entries[AGE]][COUNT] + 1
            sums_per_age[entries[AGE]][SUM] = sums_per_age[entries[AGE]][SUM] + entries[VALUE]

    average_vals = []

    for entry in sums_per_age:
        if entry[COUNT] == 0:
            pass
        else:
            average_vals.append(entry[SUM] / entry[COUNT])

    sample_ages.sort()

    return sample_ages, average_vals
