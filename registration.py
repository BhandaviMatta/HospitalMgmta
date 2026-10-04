import csv
import os
from tkinter import *
from tkinter import messagebox, ttk


def save_patient_data():
    # Retrieve form data
    first_name = entry_first_name.get().strip()
    last_name = entry_last_name.get().strip()
    dob = entry_dob.get().strip()
    gender = combo_gender.get()
    phone = entry_phone.get().strip()
    history = txt_history.get("1.0", END).strip()

    # Basic Validation
    if (
        not first_name
        or not last_name
        or not dob
        or gender == "Select"
        or not phone
    ):
        messagebox.showerror(
            "Validation Error", "All fields marked with (*) are required."
        )
        return

    # Checkbox evaluation
    consent_given = "Yes" if var_consent.get() == 1 else "No"

    # Save to a CSV File
    file_exists = os.path.isfile("patient_records.csv")

    try:
        with open("patient_records.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            # Write header if the file is new
            if not file_exists:
                writer.writerow(
                    [
                        "First Name",
                        "Last Name",
                        "DOB",
                        "Gender",
                        "Phone",
                        "Medical History",
                        "Consent",
                    ]
                )

            # Write patient details row
            writer.writerow(
                [first_name, last_name, dob, gender, phone, history, consent_given]
            )

        messagebox.showinfo(
            "Success", f"Patient {first_name} {last_name} registered successfully!"
        )
        clear_form()

    except Exception as e:
        messagebox.showerror("Error", f"Could not save data: {e}")


def clear_form():
    entry_first_name.delete(0, END)
    entry_last_name.delete(0, END)
    entry_dob.delete(0, END)
    combo_gender.set("Select")
    entry_phone.delete(0, END)
    txt_history.delete("1.0", END)
    var_consent.set(0)


# Initialize Root Window
root = Tk()
root.title("Clinic Portal - Patient Registration")
root.geometry("500x600")
root.configure(padx=20, pady=20)

# Window Title Header
lbl_title = Label(
    root, text="Patient Registration Form", font=("Arial", 16, "bold")
)
lbl_title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# --- Form Fields Layout ---

# First Name
Label(root, text="First Name *", font=("Arial", 10)).grid(
    row=1, column=0, sticky=W, pady=5
)
entry_first_name = Entry(root, width=30)
entry_first_name.grid(row=1, column=1, pady=5)

# Last Name
Label(root, text="Last Name *", font=("Arial", 10)).grid(
    row=2, column=0, sticky=W, pady=5
)
entry_last_name = Entry(root, width=30)
entry_last_name.grid(row=2, column=1, pady=5)

# Date of Birth
Label(root, text="Date of Birth (YYYY-MM-DD) *", font=("Arial", 10)).grid(
    row=3, column=0, sticky=W, pady=5
)
entry_dob = Entry(root, width=30)
entry_dob.grid(row=3, column=1, pady=5)

# Gender
Label(root, text="Gender *", font=("Arial", 10)).grid(
    row=4, column=0, sticky=W, pady=5
)
combo_gender = ttk.Combobox(
    root, values=["Male", "Female", "Other", "Prefer not to say"], width=27
)
combo_gender.set("Select")
combo_gender.grid(row=4, column=1, pady=5)

# Phone Number
Label(root, text="Phone Number *", font=("Arial", 10)).grid(
    row=5, column=0, sticky=W, pady=5
)
entry_phone = Entry(root, width=30)
entry_phone.grid(row=5, column=1, pady=5)

# Medical History
Label(root, text="Brief Medical History", font=("Arial", 10)).grid(
    row=6, column=0, sticky=W, pady=5
)
txt_history = Text(root, width=22, height=5, font=("Arial", 10))
txt_history.grid(row=6, column=1, pady=5)

# Consent Checkbox
var_consent = IntVar()
chk_consent = Checkbutton(
    root,
    text="Patient consents to data privacy terms",
    variable=var_consent,
    font=("Arial", 9),
)
chk_consent.grid(row=7, column=0, columnspan=2, pady=15, sticky=W)

# --- Action Buttons ---
btn_frame = Frame(root)
btn_frame.grid(row=8, column=0, columnspan=2, pady=10)

btn_submit = Button(
    btn_frame,
    text="Register Patient",
    command=save_patient_data,
    bg="#238636",
    fg="white",
    width=15,
)
btn_submit.pack(side=LEFT, padx=10)

btn_clear = Button(
    btn_frame, text="Clear Form", command=clear_form, bg="#da373c", fg="white", width=15
)
btn_clear.pack(side=LEFT, padx=10)

# Run application Loop
root.mainloop()