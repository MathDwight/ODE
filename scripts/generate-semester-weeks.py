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
    "Projects": "Core Course Projects Phase"
}

# Determine the structural module progression verb state
def get_module_action_verb(week, mod):
    mod_weeks = [w for w, m in week_to_mod.items() if m == mod]
    if week == mod_weeks[0]:
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

# Standardized template with unhyphenated xml:id configurations
week_template = """<?xml version="1.0" encoding="UTF-8"?>
<section xml:id="week{week_str}" xmlns:xi="http://w3.org">
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

# Initial chronological base mapping pass
start_date = datetime(2026, 8, 26)
week_starts = {w: start_date + timedelta(days=(w-1)*7) for w in range(1, 16)}

mod_starts = {}
for w in range(1, 16):
    m = week_to_mod[w]
    if m not in mod_starts:
        mod_starts[m] = week_starts[w]

# Initialize static deadlines for Mod-0
week_deadlines = {
    1: ["Mod-0 Quiz: Aug 31 (if day-one enrolled)"],
    2: [
        "Mod-0 Quiz (if not day-one enrolled): Sep 07, 11:59PM EDT",
        "Reading Quiz 1: Sep 08, 11:59PM EDT"
    ]
}

# Dynamically compute Reading Quizzes 2-5 based on Mod start times
for x in range(2, 6):
    target_mod = f"Mod-{x}"
    due_date = mod_starts[target_mod] - timedelta(days=1)

    # Locate matching parent week container for current deadline date
    for w in range(1, 16):
        if week_starts[w] <= due_date <= (week_starts[w] + timedelta(days=6)):
            if w not in week_deadlines:
                week_deadlines[w] = []
            formatted_deadline = f"Reading Quiz {x}: {due_date.strftime('%b %d')}, 11:59PM EDT"
            week_deadlines[w].append(formatted_deadline)

# Main parent generation writing routine loop
current_week_start = start_date

for week_num in range(1, 16):
    mod_name = week_to_mod[week_num]
    week_str = f"{week_num:02d}"

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

        if (day_full_name in STANDARD_CLASS_DAYS) and (date_iso not in NO_CLASS_DATES):
            class_meetings.append(f"        <li>{running_date.strftime('%b %d')}</li>")

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

    # Process automated deadlines list
    if week_num in week_deadlines:
        due_entries = [f"        <li>{deadline}</li>" for deadline in week_deadlines[week_num]]
        due_dates_block = "\n".join(due_entries)
    else:
        due_dates_block = "        <li>Review current module guidelines for project tracking updates.</li>"

    filled_week = week_template.format(
        week_str=week_str,
        week_num=week_num,
        date_range_str=date_range_str,
        action_verb=action_verb,
        mod_title_text=mod_title_text,
        class_meetings_block=class_meetings_block,
        due_dates_block=due_dates_block,
        include_tags_block=include_tags_block,
        commented_handouts_block=commented_handouts_block
    )

    parent_file_path = os.path.join(source_base, mod_name, f"week{week_str}.ptx")
    with open(parent_file_path, "w", encoding="utf-8") as f:
        f.write(filled_week)

    print(f"Generated clean parent section: {parent_file_path}")
    current_week_start += timedelta(days=7)

print("\nUnhyphenated parent week configuration complete!")
