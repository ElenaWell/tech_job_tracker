
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

from load_applications import (
    load_applications,
    save_applications,
    calculate_application_summary,
)


def main():
    filename = "applications.csv"
    applications = load_applications(filename)

    root = tk.Tk()
    root.title("Tech Job Application Tracker")
    root.geometry("900x600")
    root.minsize(800, 500)
    root.configure(bg="#071A35")

    # THEME batman cutie oh yeah
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background="#102747",
        foreground="white",
        fieldbackground="#102747",
        rowheight=30,
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        background="#17365D",
        foreground="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
    )
    style.map(
        "Treeview",
        background=[("selected", "#087E8B")],
        foreground=[("selected", "white")],
    )

    style.configure(
        "TCombobox",
        fieldbackground="#FFFFFF",
        background="#FFFFFF",
        foreground="#071A35",
    )

    # HELPERS 
    def refresh_dashboard():
        summary = calculate_application_summary(applications, date.today())

        summary_labels["total"].config(text=str(summary["total"]))
        summary_labels["active"].config(text=str(summary["active"]))
        summary_labels["upcoming"].config(text=str(summary["upcoming"]))

    def display_applications(records):
        for item in application_table.get_children():
            application_table.delete(item)

        for application in records:
            application_table.insert(
                "",
                "end",
                iid=str(application["id"]),
                values=(
                    application["company"],
                    application["position"],
                    application["deadline"].strftime("%Y-%m-%d"),
                    application["status"],
                ),
            )

    def reset_search():
        search_entry.delete(0, tk.END)
        search_entry.insert(0, "Search company or position...")
        display_applications(applications)

    def show_all_applications():
        reset_search()
        refresh_dashboard()

    def search_records(event=None):
        term = search_entry.get().strip()

        if term == "Search company or position...":
            term = ""

        if not term:
            display_applications(applications)
            return

        results = [
            application
            for application in applications
            if term.casefold() in application["company"].casefold()
            or term.casefold() in application["position"].casefold()
        ]
        display_applications(results)

    def selected_application():
        selection = application_table.selection()

        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Please select an application first.",
                parent=root,
            )
            return None

        selected_id = int(selection[0])

        for application in applications:
            if application["id"] == selected_id:
                return application

        messagebox.showerror(
            "Application Not Found",
            "The selected application could not be found.",
            parent=root,
        )
        return None

    def persist_applications(updated_applications):
        try:
            save_applications(filename, updated_applications)
            return True
        except (OSError, ValueError, TypeError) as error:
            messagebox.showerror(
                "Save Failed",
                f"Your changes could not be saved.\n\n{error}",
                parent=root,
            )
            return False

    # DASHBOARD 
    header = tk.Frame(root, bg="#071A35")
    header.pack(fill="x", padx=24, pady=(20, 12))

    tk.Label(
        header,
        text="TECH JOB TRACKER",
        font=("Segoe UI", 20, "bold"),
        fg="white",
        bg="#071A35",
    ).pack(anchor="w")

    tk.Label(
        header,
        text="Keep your applications organized. Stay ready for your next opportunity.",
        font=("Segoe UI", 10),
        fg="#B7C9E2",
        bg="#071A35",
    ).pack(anchor="w", pady=(4, 0))

    dashboard = tk.Frame(root, bg="#071A35")
    dashboard.pack(fill="x", padx=24, pady=8)

    summary_labels = {}

    summary_cards = [
        ("total", "TOTAL APPLICATIONS"),
        ("active", "ACTIVE APPLICATIONS"),
        ("upcoming", "UPCOMING DEADLINES"),
    ]

    for key, title in summary_cards:
        card = tk.Frame(dashboard, bg="#102747", padx=16, pady=12)
        card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            fg="#B7C9E2",
            bg="#102747",
        ).pack(anchor="w")

        number = tk.Label(
            card,
            text="0",
            font=("Segoe UI", 22, "bold"),
            fg="#FF6B35",
            bg="#102747",
        )
        number.pack(anchor="w", pady=(4, 0))
        summary_labels[key] = number

    # SEARCH AND ADD 
    toolbar = tk.Frame(root, bg="#071A35")
    toolbar.pack(fill="x", padx=24, pady=(12, 8))

    search_entry = tk.Entry(
        toolbar,
        font=("Segoe UI", 10),
        bg="#FFFFFF",
        fg="#071A35",
        relief="flat",
    )
    search_entry.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 8))
    search_entry.insert(0, "Search company or position...")

    def on_search_focus_in(event):
        if search_entry.get() == "Search company or position...":
            search_entry.delete(0, tk.END)

    def on_search_focus_out(event):
        if not search_entry.get().strip():
            search_entry.insert(0, "Search company or position...")

    search_entry.bind("<FocusIn>", on_search_focus_in)
    search_entry.bind("<FocusOut>", on_search_focus_out)
    search_entry.bind("<Return>", search_records)

    tk.Button(
        toolbar,
        text="SEARCH",
        command=search_records,
        bg="#087E8B",
        fg="white",
        activebackground="#0A98A5",
        activeforeground="white",
        relief="flat",
        font=("Segoe UI", 9, "bold"),
        padx=16,
        pady=8,
        cursor="hand2",
    ).pack(side="left", padx=(0, 8))

    # APPLICATION TABLE 
    table_frame = tk.Frame(root, bg="#071A35")
    table_frame.pack(fill="both", expand=True, padx=24, pady=(4, 20))

    columns = ("company", "position", "deadline", "status")

    application_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        selectmode="browse",
    )

    application_table.heading("company", text="COMPANY")
    application_table.heading("position", text="POSITION")
    application_table.heading("deadline", text="DEADLINE")
    application_table.heading("status", text="STATUS")

    application_table.column("company", width=160, anchor="w")
    application_table.column("position", width=240, anchor="w")
    application_table.column("deadline", width=130, anchor="center")
    application_table.column("status", width=120, anchor="center")

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=application_table.yview,
    )
    application_table.configure(yscrollcommand=scrollbar.set)

    application_table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    #  ADD APPLICATION 
    def open_add_application_window():
        form = tk.Toplevel(root)
        form.title("Add Application")
        form.geometry("480x510")
        form.resizable(False, False)
        form.configure(bg="#071A35")
        form.transient(root)
        form.grab_set()

        tk.Label(
            form,
            text="ADD APPLICATION",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#071A35",
        ).pack(pady=(20, 16))

        fields_frame = tk.Frame(form, bg="#071A35")
        fields_frame.pack(fill="x", padx=28)

        entries = {}

        def add_field(label_text, key, placeholder=""):
            tk.Label(
                fields_frame,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                fg="#B7C9E2",
                bg="#071A35",
            ).pack(anchor="w", pady=(8, 4))

            entry = tk.Entry(
                fields_frame,
                font=("Segoe UI", 10),
                relief="flat",
            )
            entry.pack(fill="x", ipady=7)

            if placeholder:
                entry.insert(0, placeholder)

            entries[key] = entry

        add_field("Company", "company")
        add_field("Position", "position")
        add_field("Application Date (YYYY-MM-DD)", "application_date")
        entries["application_date"].insert(0, date.today().isoformat())
        add_field("Deadline (YYYY-MM-DD)", "deadline")

        tk.Label(
            fields_frame,
            text="Status",
            font=("Segoe UI", 10, "bold"),
            fg="#B7C9E2",
            bg="#071A35",
        ).pack(anchor="w", pady=(8, 4))

        status_box = ttk.Combobox(
            fields_frame,
            values=["Applied", "Interview", "Offer", "Rejected", "Withdrawn"],
            state="readonly",
            font=("Segoe UI", 10),
        )
        status_box.pack(fill="x", ipady=3)
        status_box.set("Applied")

        def save_new_application():
            company = entries["company"].get().strip()
            position = entries["position"].get().strip()
            application_date_text = entries["application_date"].get().strip()
            deadline_text = entries["deadline"].get().strip()
            status = status_box.get().strip()

            if not all([
                company,
                position,
                application_date_text,
                deadline_text,
                status,
            ]):
                messagebox.showwarning(
                    "Missing Information",
                    "Please complete all fields.",
                    parent=form,
                )
                return

            try:
                application_date = datetime.strptime(
                    application_date_text, "%Y-%m-%d"
                ).date()
                deadline = datetime.strptime(deadline_text, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "Enter dates in YYYY-MM-DD format.",
                    parent=form,
                )
                return

            if deadline < application_date:
                messagebox.showerror(
                    "Invalid Deadline",
                    "The deadline cannot be before the application date.",
                    parent=form,
                )
                return

            next_id = max(
                (application["id"] for application in applications),
                default=0,
            ) + 1

            new_application = {
                "id": next_id,
                "company": company,
                "position": position,
                "application_date": application_date,
                "deadline": deadline,
                "status": status,
            }

            updated_applications = applications + [new_application]

            if not persist_applications(updated_applications):
                return

            applications.append(new_application)
            show_all_applications()
            form.destroy()

            messagebox.showinfo(
                "Success",
                "Application added successfully!",
                parent=root,
            )

        tk.Button(
            form,
            text="SAVE APPLICATION",
            command=save_new_application,
            bg="#FF6B35",
            fg="white",
            activebackground="#E85B27",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=16,
            pady=10,
            cursor="hand2",
        ).pack(pady=20)

    tk.Button(
        toolbar,
        text="+ ADD APPLICATION",
        command=open_add_application_window,
        bg="#FF6B35",
        fg="white",
        activebackground="#E85B27",
        activeforeground="white",
        relief="flat",
        font=("Segoe UI", 9, "bold"),
        padx=14,
        pady=8,
        cursor="hand2",
    ).pack(side="left")

    #  EDIT APPLICATION
    def open_edit_application_window():
        application = selected_application()
        if application is None:
            return

        form = tk.Toplevel(root)
        form.title("Edit Application")
        form.geometry("480x510")
        form.resizable(False, False)
        form.configure(bg="#071A35")
        form.transient(root)
        form.grab_set()

        tk.Label(
            form,
            text="EDIT APPLICATION",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#071A35",
        ).pack(pady=(20, 16))

        fields_frame = tk.Frame(form, bg="#071A35")
        fields_frame.pack(fill="x", padx=28)

        entries = {}

        def add_edit_field(label_text, key, value):
            tk.Label(
                fields_frame,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                fg="#B7C9E2",
                bg="#071A35",
            ).pack(anchor="w", pady=(8, 4))

            entry = tk.Entry(
                fields_frame,
                font=("Segoe UI", 10),
                relief="flat",
            )
            entry.pack(fill="x", ipady=7)
            entry.insert(0, value)
            entries[key] = entry

        add_edit_field("Company", "company", application["company"])
        add_edit_field("Position", "position", application["position"])
        add_edit_field(
            "Application Date (YYYY-MM-DD)",
            "application_date",
            application["application_date"].isoformat(),
        )
        add_edit_field(
            "Deadline (YYYY-MM-DD)",
            "deadline",
            application["deadline"].isoformat(),
        )

        tk.Label(
            fields_frame,
            text="Status",
            font=("Segoe UI", 10, "bold"),
            fg="#B7C9E2",
            bg="#071A35",
        ).pack(anchor="w", pady=(8, 4))

        status_box = ttk.Combobox(
            fields_frame,
            values=["Applied", "Interview", "Offer", "Rejected", "Withdrawn"],
            state="readonly",
            font=("Segoe UI", 10),
        )
        status_box.pack(fill="x", ipady=3)
        status_box.set(application["status"])

        def save_edited_application():
            company = entries["company"].get().strip()
            position = entries["position"].get().strip()
            application_date_text = entries["application_date"].get().strip()
            deadline_text = entries["deadline"].get().strip()
            status = status_box.get().strip()

            if not all([
                company,
                position,
                application_date_text,
                deadline_text,
                status,
            ]):
                messagebox.showwarning(
                    "Missing Information",
                    "Please complete all fields.",
                    parent=form,
                )
                return

            try:
                application_date = datetime.strptime(
                    application_date_text, "%Y-%m-%d"
                ).date()
                deadline = datetime.strptime(deadline_text, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "Enter dates in YYYY-MM-DD format.",
                    parent=form,
                )
                return

            if deadline < application_date:
                messagebox.showerror(
                    "Invalid Deadline",
                    "The deadline cannot be before the application date.",
                    parent=form,
                )
                return

            updated_record = {
                "id": application["id"],
                "company": company,
                "position": position,
                "application_date": application_date,
                "deadline": deadline,
                "status": status,
            }

            updated_applications = [
                updated_record if item["id"] == application["id"] else item
                for item in applications
            ]

            if not persist_applications(updated_applications):
                return

            application.update(updated_record)
            show_all_applications()
            form.destroy()

            messagebox.showinfo(
                "Success",
                "Application updated successfully!",
                parent=root,
            )

        tk.Button(
            form,
            text="SAVE CHANGES",
            command=save_edited_application,
            bg="#FF6B35",
            fg="white",
            activebackground="#E85B27",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=16,
            pady=10,
            cursor="hand2",
        ).pack(pady=20)

    # COPY COMPANY NAME 
    def copy_company_name():
        application = selected_application()
        if application is None:
            return

        try:
            root.clipboard_clear()
            root.clipboard_append(application["company"])
            root.update()
        except tk.TclError as error:
            messagebox.showerror(
                "Copy Failed",
                f"Could not copy the company name.\n\n{error}",
                parent=root,
            )
            return

        messagebox.showinfo(
            "Copied",
            f"Copied '{application['company']}' to the clipboard.",
            parent=root,
        )

    #  DELETE APPLICATION 
    def delete_application():
        application = selected_application()
        if application is None:
            return

        confirmed = messagebox.askyesno(
            "Confirm Deletion",
            (
                "Are you sure you want to delete this application?\n\n"
                f"Company: {application['company']}\n"
                f"Position: {application['position']}\n\n"
                "This action cannot be undone."
            ),
            parent=root,
        )

        if not confirmed:
            return

        updated_applications = [
            item
            for item in applications
            if item["id"] != application["id"]
        ]

        if not persist_applications(updated_applications):
            return

        applications[:] = updated_applications
        show_all_applications()

        messagebox.showinfo(
            "Deleted",
            "Application deleted successfully.",
            parent=root,
        )

    # RIGHT-CLICK CONTEXT MENU 
    context_menu = tk.Menu(
        root,
        tearoff=0,
        bg="#102747",
        fg="white",
        activebackground="#087E8B",
        activeforeground="white",
        font=("Segoe UI", 10),
    )

    context_menu.add_command(
        label="Edit Application",
        command=open_edit_application_window,
    )
    context_menu.add_command(
        label="Copy Company Name",
        command=copy_company_name,
    )
    context_menu.add_separator()
    context_menu.add_command(
        label="Delete Application",
        command=delete_application,
    )

    def show_context_menu(event):
        row_id = application_table.identify_row(event.y)

        # Don't show the menu when the user right-clicks empty space.
        if not row_id:
            return

        application_table.selection_set(row_id)
        application_table.focus(row_id)

        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    application_table.bind("<Button-3>", show_context_menu)

    #  START 
    display_applications(applications)
    refresh_dashboard()

    root.mainloop()


if __name__ == "__main__":
    main()
