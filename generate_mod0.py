import os
from datetime import datetime, timedelta

# Path targets the source folder inside your project root directory
base_dir = "source/Mod-0"

week_configs = {
    "week01": {
        "start_date": datetime(2026, 8, 26),
        "days_count": 7
    },
    "week02": {
        "start_date": datetime(2026, 9, 2),
        "days_count": 7
    }
}

# Mapping days of the week to single letters (R for Thursday, U for Sunday)
day_letters = {
    "Wednesday": "W",
    "Thursday": "R",
    "Friday": "F",
    "Saturday": "S",
    "Sunday": "U",
    "Monday": "M",
    "Tuesday": "T"
}

# Fixed Template: Uses paragraphs as the root element instead of fragment
xml_template = """<?xml version="1.0" encoding="UTF-8" ?>
<paragraphs xml:id="day-{file_stub}" xmlns:xi="http://w3.org">
  <title></title>

  <paragraphs xml:id="scratchpad-{file_stub}">
    <title>Instructor Notes</title>
    <p>
    </p>
  </paragraphs>

  <handout xml:id="handout-{file_stub}">
    <title>{display_date}</title>
    <p>
    </p>

    <biographical xml:id="footer-{file_stub}">
      <p>
        The present materials are/were associated with a differential equations course instructed by Dwight Anderson Williams II.
      </p>
    </biographical>
  </handout>

</paragraphs>"""

for week_name, config in week_configs.items():
    week_folder_path = os.path.join(base_dir, week_name)
    os.makedirs(week_folder_path, exist_ok=True)

    print(f"\\n=========================================")
    print(f"Creating files in: {week_folder_path}")
    print(f"=========================================")

    current_date = config["start_date"]

    for i in range(config["days_count"]):
        day_full_name = current_date.strftime("%A")
        day_letter = day_letters[day_full_name]

        file_stub = f"{current_date.strftime('%Y%m%d')}-{day_letter}"
        display_date = current_date.strftime("%A, %d %B %Y")

        file_path = os.path.join(week_folder_path, f"{file_stub}.xml")
        filled_content = xml_template.format(file_stub=file_stub, display_date=display_date)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(filled_content)

        print(f" -> Created {file_stub}.xml")
        current_date += timedelta(days=1)

print("\\nExecution complete! Check your updated chronological files in Atom.")
