# Discussion Group Role Assignment

## Overview
This script assigns students to discussion groups and distributes roles fairly, ensuring that students receive different roles over time unless all options are exhausted. Groups are dynamically sized to accommodate varying student counts.

## Setup Instructions
1. **Download Class Roster**
   - Follow the steps here: [Download a Student Roster in Canvas](https://teacherscollege.screenstepslive.com/a/1286286-download-a-student-roster-in-canvas)
   - Save the CSV file in the `discussion_groups/data/` folder.

2. **Run the Script**
   - Open `assign_groups.py` and update the following variables:
     - `discussion_number`: The discussion session number.
     - `num_groups`: The number of discussion groups i.e., the number of papers being discussed.
   - Execute the script:
     ```sh
     python assign_groups.py
     ```

## How It Works
1. **Reads Student Roster**: Extracts student names from the CSV file.
2. **Forms Groups**: Distributes students evenly across the specified number of groups.
3. **Assigns Roles**:
   - Prioritizes must-have roles (`Reviewer`, `Community archaeologist`).
   - Assigns other roles (`Forensic archaeologist`, `Academic researcher`, `Visitor from the past`) as needed.
   - Ensures students receive new roles whenever possible.
   - Dynamically adjusts group sizes if student count doesn’t divide evenly.
4. **Optimizes Assignments**:
   - Minimizes role repetition by swapping students between groups if needed.
5. **Saves Assignments**: Stores assignments in `discussion_groups/discussion_assignments/` for reference in future discussions.

## Notes
- The script dynamically adjusts roles if the number of students is not a perfect multiple of role count.
- If fewer students are available than required roles, some roles are dropped.
- If more students are available, must-have roles are assigned first before repeating others.



