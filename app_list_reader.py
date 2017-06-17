import csv


def read(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quoting=3)
        return [r[0] for r in reader]


def cleanup_app_name(app_list):
    return [' '.join(r.split()[:3]) for r in app_list]
