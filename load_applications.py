import csv
from datetime import datetime

# This file contains the reusable functions.

def load_applications(filename):
    """Load job applications from a CSV file."""
    applications = []

    with open(filename, "rt") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            application = {
                "id": int(row["id"]),
                "company": row["company"],
                "position": row["position"],
                "application_date": datetime.strptime(
                    row["application_date"], "%Y-%m-%d"
                ).date(),
                "deadline": datetime.strptime(
                    row["deadline"], "%Y-%m-%d"
                ).date(),
                "status": row["status"]
            }

            applications.append(application)

    return applications

def save_applications(filename, applications):
    """Save job applications to a CSV file."""
    with open(filename, "wt") as csv_file:

        fieldnames = [
            "id",
            "company",
            "position",
            "application_date",
            "deadline",
            "status"
         ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for application in applications:
            row = application.copy()
            row["application_date"] = row["application_date"].strftime("%Y-%m-%d")
            row["deadline"] = row["deadline"].strftime("%Y-%m-%d")

            writer.writerow(row) # Use a copy(row)so the original application data is not modified.

def add_application(applications, application):
    """Add a job application to the list."""
    applications.append(application)

def search_applications(applications, search_term):
    """Search applications by company or position."""

    results = []

    for application in applications:
        if search_term in application["company"] or search_term in application["position"]:
            results.append(application)

    return results

def update_application_status(applications, application_id, new_status):
    """Update the status of a job application."""

    for application in applications:
        if application["id"] == application_id:
            application["status"] = new_status
            return True
        
    return False

def find_upcoming_deadlines(applications, current_date):
    """Find applications with upcoming deadlines."""
    results = []

    for application in applications:
        if application["deadline"] >= current_date:
            results.append(application)

    return results 

def calculate_application_summary(applications, current_date):
    """Calculate a summary of job applications."""

    total = len(applications)

    active_count = 0

    for application in applications:
        if application["status"] in ["Applied", "Interview"]:
            active_count += 1

    upcoming = find_upcoming_deadlines(applications, current_date)
    upcoming_count = len(upcoming)

    summary = {
        "total": total,
        "active": active_count,
        "upcoming": upcoming_count
    }
    

    return summary






    