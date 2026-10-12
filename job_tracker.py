import tkinter as tk
from datetime import date
from tkinter import ttk

from load_applications import (
    load_applications,
    save_applications,
    add_application,
    search_applications,
    update_application_status,
    find_upcoming_deadlines,
    calculate_application_summary
)


def main():
    # Load existing application data
    applications = load_applications("applications.csv")

    # Calculate dashboard statistics
    current_date = date.today()

    summary = calculate_application_summary(
        applications,
        current_date
    )

    # Create the main application window
    root = tk.Tk()
    root.title("Tech Job Application Tracker")
    root.geometry("900x600")
    root.configure(bg="#071A35")

    # Create the main heading
    heading = tk.Label(
        root,
        text="TECH JOB APPLICATION TRACKER",
        font=("Arial", 20, "bold"),
        bg="#071A35",
        fg="#FFFFFF"
    )
    heading.pack(pady=25)

    # Create the summary dashboard
    dashboard = tk.Frame(
        root,
        bg="#071A35"
    )
    dashboard.pack(fill="x", padx=25, pady=15)

    # Define the summary card information
    cards = [
        ("TOTAL APPLICATIONS", summary["total"], "#1677FF"),
        ("ACTIVE APPLICATIONS", summary["active"], "#E32636"),
        ("UPCOMING DEADLINES", summary["upcoming"], "#F7C948")
    ]

    # Build the summary cards
    for title, value, accent in cards:
        card = tk.Frame(
            dashboard,
            bg="#102A50",
            padx=18,
            pady=18
        )
        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=6
        )

        label = tk.Label(
            card,
            text=title,
            bg="#102A50",
            fg="#AFC7E8",
            font=("Arial", 9, "bold")
        )
        label.pack(anchor="w")

        number = tk.Label(
            card,
            text=str(value),
            bg="#102A50",
            fg="#FFFFFF",
            font=("Arial", 26, "bold")
        )
        number.pack(anchor="w", pady=(8, 4))

        accent_bar = tk.Frame(
            card,
            bg=accent,
            height=4
        )
        accent_bar.pack(fill="x", pady=(6, 0))

    # Create the applications section
    applications_frame = tk.Frame(
        root,
        bg="#071A35"
    )
    applications_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=20
    )

    # Section heading
    applications_heading = tk.Label(
        applications_frame,
        text="YOUR APPLICATIONS",
        font=("Arial", 14, "bold"),
        bg="#071A35",
        fg="#FFFFFF"
    )
    applications_heading.pack(anchor="w", pady=(0, 12))

    # Create the search bar section
    search_frame = tk.Frame(
        applications_frame,
        bg="#071A35"
    )
    search_frame.pack(
        fill="x",
        pady=(0, 12)
    )

    # Create the search input
    search_entry = tk.Entry(
        search_frame,
        font=("Arial", 11),
        bg="#102A50",
        fg="#FFFFFF",
        insertbackground="#FFFFFF",
        relief="flat"
    )
    search_entry.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=8,
        padx=(0, 10)
    )

    # Add placeholder guidance
    placeholder = "Search company or position..."
    search_entry.insert(0, placeholder)

    # Create the search button
    search_button = tk.Button(
        search_frame,
        text="SEARCH",
        font=("Arial", 9, "bold"),
        bg="#252B35",
        fg="#FFFFFF",
        activebackground="#343B46",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        padx=18,
        pady=8
    )
    search_button.pack(side="right")

    # Configure the widget styles
    style = ttk.Style()
    style.theme_use("clam")

    # Premium dark scrollbar styling
    style.configure(
        "Vertical.TScrollbar",
        background="#252B35",
        troughcolor="#07090D",
        bordercolor="#07090D",
        arrowcolor="#FFFFFF",
        darkcolor="#252B35",
        lightcolor="#252B35",
        relief="flat",
        gripcount=0,
        width=12
    )

    style.map(
        "Vertical.TScrollbar",
        background=[
            ("pressed", "#414955"),
            ("active", "#343B46")
        ]
    )

    # Style the table rows
    style.configure(
        "Treeview",
        background="#102A50",
        foreground="#FFFFFF",
        fieldbackground="#102A50",
        rowheight=32,
        font=("Arial", 10)
    )

    # Style the table headings
    style.configure(
        "Treeview.Heading",
        background="#071A35",
        foreground="#AFC7E8",
        font=("Arial", 10, "bold"),
        relief="flat"
    )

    # Style the selected row
    style.map(
        "Treeview",
        background=[("selected", "#1677FF")],
        foreground=[("selected", "#FFFFFF")]
    )

    # Style the heading when hovered over
    style.map(
        "Treeview.Heading",
        background=[("active", "#102A50")]
    )

    # Define the table columns
    columns = (
        "company",
        "position",
        "deadline",
        "status"
    )

    # Create a frame to hold the table and scrollbar
    table_frame = tk.Frame(
        applications_frame,
        bg="#071A35"
    )
    table_frame.pack(
        fill="both",
        expand=True
    )

    # Create the application table
    application_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    # Create the vertical scrollbar
    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=application_table.yview
    )

    # Connect the table to the scrollbar
    application_table.configure(
        yscrollcommand=scrollbar.set
    )

    # Set column headings
    application_table.heading("company", text="COMPANY")
    application_table.heading("position", text="POSITION")
    application_table.heading("deadline", text="DEADLINE")
    application_table.heading("status", text="STATUS")

    # Configure column widths
    application_table.column("company", width=150)
    application_table.column("position", width=280)
    application_table.column("deadline", width=120)
    application_table.column("status", width=120)

    # Display applications in the table
    def display_applications(records):
        # Remove existing rows
        for item in application_table.get_children():
            application_table.delete(item)

        # Insert the selected records
        for application in records:
            application_table.insert(
                "",
                "end",
                values=(
                    application["company"],
                    application["position"],
                    application["deadline"].strftime("%Y-%m-%d"),
                    application["status"]
                )
            )

    # Display all applications when the program starts
    display_applications(applications)

    # Display the table and scrollbar side by side
    application_table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # Search applications by company or position
    def perform_search():
        search_term = search_entry.get().strip()

        # Show all applications if the search is empty
        if not search_term or search_term == placeholder:
            display_applications(applications)
            return

        # Search using the existing backend function
        results = search_applications(
            applications,
            search_term
        )

        # Display the matching records
        display_applications(results)

    # Connect the search button
    search_button.configure(command=perform_search)

    # Search when Enter is pressed
    search_entry.bind(
        "<Return>",
        lambda event: perform_search()
    )

    # Clear the placeholder when the user focuses the input
    def clear_placeholder(event):
        if search_entry.get() == placeholder:
            search_entry.delete(0, tk.END)

    search_entry.bind("<FocusIn>", clear_placeholder)

    # Restore the placeholder if the input is empty
    def restore_placeholder(event):
        if not search_entry.get().strip():
            search_entry.insert(0, placeholder)

    search_entry.bind("<FocusOut>", restore_placeholder)

    # Keep the window running and responsive
    root.mainloop()


if __name__ == "__main__":
    main()
