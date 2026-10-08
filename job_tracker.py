from load_applications import (
    load_applications,
    save_applications,
    add_application,
    search_applications,
    update_application_status,
    find_upcoming_deadlines,
    calculate_application_summary
    
)
from datetime import date 


applications = load_applications("applications.csv")

save_applications("test_applications.csv", applications)

print("Saved successfully!")


new_application = {
    "id": 9,
    "company": "NVIDIA",
    "position": "Software Engineer Intern",
    "application_date": date(2026, 10, 8),
    "deadline": date(2026, 10, 25),
    "status": "Applied"
}

add_application(applications, new_application)

print(len(applications))
print(f"New application: {new_application['status']} at {new_application['company']}")
search_results = search_applications(applications, "Google")
print(search_results)

updated = update_application_status(applications, 1, "Interview")

print(updated)
print(applications[0])
print(len(applications))

upcoming = find_upcoming_deadlines(applications, date(2026, 10, 8))
print(upcoming)

summary = calculate_application_summary(applications, date(2026, 10, 8))
print(summary)
