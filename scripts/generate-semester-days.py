import os
from datetime import datetime, timedelta

# Root directory path for all module files
source_base = "source"

# Map semester week indices directly to their syllabus folders up through Week 15
week_to_mod = {
    1: "Mod-0", 2: "Mod-0",
    3: "Mod-1", 4: "Mod-1",
    5: "Mod-2", 6: "Mod-2", 7: "Mod-2",
    8: "Mod-3", 9: "Mod-3", 10: "Mod-3",
    11: "Mod-4",
    12: "Mod-5", 13: "Mod-5",
    14: "Projects", 15: "Projects"
}

# Ordered column tracking keys reflecting the syllabus date matrix
day_letters = {
    "Wednesday": "W",
    "Thursday": "R",
    "Friday": "F",
    "Saturday": "S",
    "Sunday": "U",
    "Monday": "M",
    "Tuesday": "T"
}

# Define the standard scheduled physical class meeting loop days
STANDARD_CLASS_DAYS = ["Wednesday", "Friday", "Monday"]

# Hardcoded calendar dates when there is no face-to-face class session
NO_CLASS_DATES = [
    "20260907",  # Week 2 Monday: Labor Day (University Closed)
    "20261007",  # Week 7 Wednesday: Group Work Day
    "20261106",  # Week 11 Friday: Group Work Day
    "20261123",  # Week 13 Monday: Group Work Day
    "20261125",  # Week 14 Wednesday: Thanksgiving Recess (University Closed)
    "20261127"   # Week 14 Friday: Thanksgiving Recess (University Closed)
]

# XML layout template for active class days
class_day_template = """<?xml version="1.0" encoding="UTF-8" ?>
<subsection xml:id="day-{file_stub}" web-toc="none" xmlns:xi="http://www.w3.org/2001/XInclude">
  <title>{display_date}</title>

  <paragraphs xml:id="announcements-{file_stub}">
    <title>Announcements</title>
    <p>&#xa0;</p>
  </paragraphs>

  <paragraphs xml:id="notes-{file_stub}">
    <title>Class Notes</title>
    <p>&#xa0;</p>
  </paragraphs>

  <exploration xml:id="activity-{file_stub}">
    <title>In-Class Activity</title>
    <p>&#xa0;</p>
  </exploration>

  <handout xml:id="handout-{file_stub}">
    <title>Reflection and Review for Class Date: {display_date}</title>
    <p>
      Fall 2026 MATH 340 Intro to Differential Equations<br/>
      Instructor: Dwight Anderson Williams II, PhD<br/>
      Student: <fillin characters="30" /><br/>
      Date of Work: <fillin characters="20" />
    </p>
    <p>&#xa0;</p>
  </handout>

</subsection>"""

# XML layout template for independent study and preparation days
no_class_template = """<?xml version="1.0" encoding="UTF-8" ?>
<subsection xml:id="day-{file_stub}" web-toc="none" xmlns:xi="http://www.w3.org/2001/XInclude">
  <title>{display_date}</title>

  <paragraphs xml:id="announcements-{file_stub}">
    <title>Announcements</title>
    <p>&#xa0;</p>
  </paragraphs>

  <paragraphs xml:id="preparation-{file_stub}">
    <title>Pre-Class Preparation</title>
    <p>&#xa0;</p>
  </paragraphs>

  <handout xml:id="handout-{file_stub}">
    <title>Reflection and Review for Study Date: {display_date}</title>
    <p>
      Fall 2026 MATH 340 Intro to Differential Equations<br/>
      Instructor: Dwight Anderson Williams II, PhD<br/>
      Student: <fillin characters="30" /><br/>
      Date of Work: <fillin characters="20" />
    </p>
    <p>&#xa0;</p>
  </handout>

</subsection>"""

# Semester start anchor initialized to Week 1 Wednesday
current_week_start = datetime(2026, 8, 26)

# Iterate across Weeks 1 through 15
for week_num in range(1, 16):
    mod_name = week_to_mod[week_num]
    week_str = f"week{week_num:02d}"

    # Establish subfolder configuration path relative to module directory
    week_folder_path = os.path.join(source_base, mod_name, week_str)
    os.makedirs(week_folder_path, exist_ok=True)

    print(f"\n=========================================")
    print(f"Creating files in: {week_folder_path}")
    print(f"=========================================")

    include_tags = []
    running_date = current_week_start

    # Process 7 consecutive dates per week chunk
    for d in range(7):
        day_full_name = running_date.strftime("%A")
        day_letter = day_letters[day_full_name]

        date_iso = running_date.strftime('%Y%m%d')
        file_stub = f"{date_iso}-{day_letter}"
        display_date = running_date.strftime("%A, %d %B %Y")
        file_path = os.path.join(week_folder_path, f"{file_stub}.xml")

        # Determine if current date is a standard active class session
        if (day_full_name in STANDARD_CLASS_DAYS) and (date_iso not in NO_CLASS_DATES):
            filled_content = class_day_template.format(file_stub=file_stub, display_date=display_date)
            print(f" -> Created Active Class Day: {file_stub}.xml")
        else:
            filled_content = no_class_template.format(file_stub=file_stub, display_date=display_date)
            print(f" -> Created Independent / Holiday / Group Work Day: {file_stub}.xml")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(filled_content)

        include_tags.append(f'<xi:include href="{week_str}/{file_stub}.xml" />')
        running_date += timedelta(days=1)

   # Output the include tags for the target week master structure file
    print(f"\n--- Copy and paste these lines into your {source_base}/{mod_name}/{week_str}.ptx file ---")
    for tag in include_tags:
        print(tag)

    # Advance the calendar calculation to the next week block
    current_week_start += timedelta(days=7)

print("\nSemester tree generation execution complete!")
