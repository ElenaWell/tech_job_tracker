from datetime import date

from load_applications import (
    load_applications,
    save_applications,
    add_application,
    search_applications,
    update_application_status,
    find_upcoming_deadlines,
    calculate_application_summary,
)


def sample_application():
    return {
        "id": 1,
        "company": "Google",
        "position": "Software Engineer Intern",
        "application_date": date(2026, 10, 1),
        "deadline": date(2026, 10, 20),
        "status": "Applied",
    }


def test_add_application():
    applications = []
    google = sample_application()
    microsoft = {
        **sample_application(),
        "id": 2,
        "company": "Microsoft",
    }

    add_application(applications, google)
    add_application(applications, microsoft)

    assert len(applications) == 2
    assert applications[1]["company"] == "Microsoft"


def test_search_applications():
    applications = [
        sample_application(),
        {
            **sample_application(),
            "id": 2,
            "company": "Microsoft",
            "position": "Data Analyst",
        },
    ]

    google_results = search_applications(applications, "google")
    microsoft_results = search_applications(applications, "microsoft")

    assert len(google_results) == 1
    assert microsoft_results[0]["company"] == "Microsoft"


def test_update_application_status():
    applications = [
        sample_application(),
        {
            **sample_application(),
            "id": 2,
            "company": "Microsoft",
        },
    ]

    first_result = update_application_status(
        applications, 1, "Interview"
    )
    second_result = update_application_status(
        applications, 2, "Offer"
    )

    assert first_result is True
    assert second_result is True
    assert applications[1]["status"] == "Offer"


def test_update_missing_application():
    applications = [sample_application()]

    first_result = update_application_status(
        applications, 99, "Interview"
    )
    second_result = update_application_status(
        applications, 100, "Offer"
    )

    assert first_result is False
    assert second_result is False
    assert applications[0]["status"] == "Applied"


def test_find_upcoming_deadlines():
    applications = [
        sample_application(),
        {
            **sample_application(),
            "id": 2,
            "company": "Microsoft",
            "deadline": date(2026, 10, 30),
        },
        {
            **sample_application(),
            "id": 3,
            "company": "Amazon",
            "deadline": date(2026, 10, 5),
        },
    ]

    results = find_upcoming_deadlines(
        applications, date(2026, 10, 20)
    )
    later_results = find_upcoming_deadlines(
        applications, date(2026, 10, 21)
    )

    assert {app["company"] for app in results} == {
        "Google", "Microsoft"
    }
    assert {app["company"] for app in later_results} == {
        "Microsoft"
    }


def test_calculate_application_summary():
    applications = [
        sample_application(),
        {
            **sample_application(),
            "id": 2,
            "company": "Microsoft",
            "status": "Interview",
            "deadline": date(2026, 10, 30),
        },
        {
            **sample_application(),
            "id": 3,
            "company": "Amazon",
            "status": "Rejected",
            "deadline": date(2026, 10, 10),
        },
    ]

    summary = calculate_application_summary(
        applications, date(2026, 10, 20)
    )
    later_summary = calculate_application_summary(
        applications, date(2026, 10, 21)
    )

    assert summary["total"] == 3
    assert summary["active"] == 2
    assert later_summary["upcoming"] == 1


def test_save_and_load_applications(tmp_path):
    filename = tmp_path / "test_applications.csv"
    applications = [sample_application()]

    save_applications(str(filename), applications)
    loaded = load_applications(str(filename))

    assert len(loaded) == 1
    assert loaded[0]["company"] == "Google"
    assert loaded[0]["application_date"] == date(2026, 10, 1)
    assert loaded[0]["deadline"] == date(2026, 10, 20)
    assert loaded[0]["id"] == 1