import os
from datetime import datetime, timedelta

# Root directory path for all module source files
source_base = "source"

# Map semester week indices directly to their syllabus folders
week_to_mod = {
    1: "Mod-0", 2: "Mod-0",
    3: "Mod-1", 4: "Mod-1",
    5: "Mod-2", 6: "Mod-2", 7: "Mod-2",
    8: "Mod-3", 9: "Mod-3",
    10: "Mod-4", 11: "Mod-4",
    12: "Mod-5", 13: "Mod-5",
    14: "Projects", 15: "Projects"
}

# Explicit definition of the exact Mod labels matching your syllabus parameters
mod_titles = {
    "Mod-0": "Mod-0: Logistics and Foundations",
    "Mod-1": "Mod-1: Recognizing ODEs and Their Solutions",
    "Mod-2": "Mod-2: Numerical Methods",
    "Mod-3": "Mod-3: First-Order ODEs and Analytic Methods",
    "Mod-4": "Mod-4: Second-Order ODEs and Analytic Methods",
    "Mod-5": "Mod-5: Systems and Symmetries",
    "Projects": "Core Projects"
}

# Determine the structural module progression verb state
def get_module_action_verb(week, mod):
    mod_weeks = [w for w, m in week_to_mod.items() if m == mod]
    if week == mod_weeks:
        return "opens"
    elif week == mod_weeks[-1]:
        return "closes"
    else:
        return "continues"

day_letters = {
    "Wednesday": "W", "Thursday": "R", "Friday": "F", "Saturday": "S",
    "Sunday": "U", "Monday": "M", "Tuesday": "T"
}

STANDARD_CLASS_DAYS = ["Wednesday", "Friday", "Monday"]

# Calendar dates when face-to-face lecture sessions are canceled
NO_CLASS_DATES = [
    "20260907", "20261007", "20261106", "20261123", "20261125", "20261127"
]

# XML layout template optimized for face-to-face active class days
class_day_template = """<?xml version="1.0" encoding="UTF-8" ?>
<subsection xml:id="day-{file_stub}" web-toc="none" xmlns:xi="{xi_url}">
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
    <p>Fall 2026 MATH 340 Intro to Differential Equations</p>
    <p>Instructor: Dwight Anderson Williams II, PhD</p>
    <p>Student: /></p>
    <p>Date of Work:  /></p>
    <p>&#xa0;</p>
  </handout>

</subsection>"""

# XML layout template optimized for independent study and preparation days
no_class_template = """<?xml version="1.0" encoding="UTF-8" ?>
<subsection xml:id="day-{file_stub}" web-toc="none" xmlns:xi="{xi_url}">
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
    <p>Fall 2026 MATH 340 Intro to Differential Equations</p>
    <p>Instructor: Dwight Anderson Williams II, PhD</p>
    <p>Student: <fillin characters="30" /></p>
    <p>Date of Work: <fillin characters="20" /></p>
    <p>&#xa0;</p>
  </handout>

</subsection>"""


week_template = """<?xml version="1.0" encoding="UTF-8"?>
<section xml:id="week{week_str}" xmlns:xi="{xi_url}">
  <title>Week {week_num}</title>

  <introduction>
    <p>
      Week {week_num} ({date_range_str}) {action_verb} {mod_title_text}.
    </p>
    <p>
      Class meeting dates:
      <ul>
{class_meetings_block}
      </ul>
    </p>
    <p>
      Next due dates:
      <ul>
{due_dates_block}
      </ul>
    </p>
  </introduction>

  <!-- Chronological daily includes for Week {week_num} -->
{include_tags_block}

<!--
{commented_handouts_block}
-->
</section>"""

# Un-truncated target namespace string constant
XINCLUDE_URI = "http://www.w3.org/2001/XInclude"

# Chronological calendar setup pass
start_date = datetime(2026, 8, 26)
week_starts = {w: start_date + timedelta(days=(w-1)*7) for w in range(1, 16)}

mod_starts = {}
for w in range(1, 16):
    m = week_to_mod[w]
    if m not in mod_starts:
        mod_starts[m] = week_starts[w]

# Explicit chronologically ordered milestone registry with automatic EST calculation adjustments
all_semester_deadlines = [
    {"week_threshold": 1, "text": "Mod-0 Quiz: Aug 31 (if day-one enrolled)"},
    {"week_threshold": 2, "text": "Mod-0 Quiz (if not day-one enrolled): Sep 07, 11:59PM EDT"},
    {"week_threshold": 2, "text": "Reading Quiz 1: Sep 08, 11:59PM EDT"},
    {"week_threshold": 14, "text": "Core Projects: Dec 01, 11:59PM EST"},
    {"week_threshold": 15, "text": "Final Feedback: Dec 08, 11:59PM EST"}
]

# Compute Reading Quizzes 2-5
for x in range(2, 6):
    target_mod = f"Mod-{x}"
    due_date = mod_starts[target_mod] - timedelta(days=1)

    target_week = 15
    for w in range(1, 16):
        if week_starts[w] <= due_date <= (week_starts[w] + timedelta(days=6)):
            target_week = w
            break

    # Apply standard winter boundary check rule for zone labeling string adjustments
    tz = "EST" if due_date >= datetime(2026, 11, 1) else "EDT"
    formatted_text = f"Reading Quiz {x}: {due_date.strftime('%b %d')}, 11:59PM {tz}"
    all_semester_deadlines.append({"week_threshold": target_week, "text": formatted_text})

# Main processing generation pipeline loop
current_week_start = start_date

for week_num in range(1, 16):
    mod_name = week_to_mod[week_num]
    week_str = f"{week_num:02d}"

    week_folder_path = os.path.join(source_base, mod_name, f"week{week_str}")
    os.makedirs(week_folder_path, exist_ok=True)

    week_end_date = current_week_start + timedelta(days=6)
    date_range_str = f"{current_week_start.strftime('%b %d')}<ndash/>{week_end_date.strftime('%b %d')}"

    action_verb = get_module_action_verb(week_num, mod_name)
    mod_title_text = mod_titles[mod_name]

    class_meetings = []
    include_tags = []
    commented_handouts = []
    running_date = current_week_start

    for d in range(7):
        day_full_name = running_date.strftime("%A")
        day_letter = day_letters[day_full_name]
        date_iso = running_date.strftime('%Y%m%d')
        file_stub = f"{date_iso}-{day_letter}"
        display_date = running_date.strftime("%A, %d %B %Y")

        if (day_full_name in STANDARD_CLASS_DAYS) and (date_iso not in NO_CLASS_DATES):
            class_meetings.append(f"        <li>{running_date.strftime('%b %d')}</li>")
            day_filled = class_day_template.format(file_stub=file_stub, display_date=display_date, xi_url=XINCLUDE_URI)
        else:
            day_filled = no_class_template.format(file_stub=file_stub, display_date=display_date, xi_url=XINCLUDE_URI)

        day_file_path = os.path.join(week_folder_path, f"{file_stub}.xml")
        with open(day_file_path, "w", encoding="utf-8") as f:
            f.write(day_filled)

        include_tags.append(f'  <xi:include href="week{week_str}/{file_stub}.xml" />')

        commented_handouts.append(
            f"  <handout>\n"
            f"    <title>{running_date.strftime('%A, %d %B %Y')}</title>\n"
            f"    <p>\n"
            f"    </p>\n"
            f"  </handout>"
        )
        running_date += timedelta(days=1)

    class_meetings_block = "\n".join(class_meetings) if class_meetings else "        <li>No lecture meetings.</li>"
    include_tags_block = "\n".join(include_tags)
    commented_handouts_block = "\n\n".join(commented_handouts)

    active_dues = []
    for item in all_semester_deadlines:
        if item["week_threshold"] == week_num:
            active_dues.append(f"        <li>{item['text']}</li>")

    if not active_dues:
        for item in all_semester_deadlines:
            if item["week_threshold"] > week_num:
                active_dues.append(f"        <li>{item['text']}</li>")
                break

    if not active_dues:
        active_dues.append("        <li>None scheduled.</li>")

    due_dates_block = "\n".join(active_dues)

    filled_week = week_template.format(
        week_str=week_str,
        week_num=week_num,
        date_range_str=date_range_str,
        action_verb=action_verb,
        mod_title_text=mod_title_text,
        class_meetings_block=class_meetings_block,
        due_dates_block=due_dates_block,
        include_tags_block=include_tags_block,
        commented_handouts_block=commented_handouts_block,
        xi_url=XINCLUDE_URI
    )

    parent_file_path = os.path.join(source_base, mod_name, f"week{week_str}.ptx")
    with open(parent_file_path, "w", encoding="utf-8") as f:
        f.write(filled_week)

    print(f"Generated clean parent week and sub-folder components for: week{week_str}")
    current_week_start += timedelta(days=7)

print("\nComplete course framework generation successful!")
