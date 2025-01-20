import csv
import random
import os
import json

# Define discussion roles in priority order
MUST_HAVE_ROLES = [
    "Reviewer",
    "Community archaeologist"
]
GOOD_TO_HAVE_ROLES = [
    "Forensic archaeologist",
    "Academic researcher",
    "Visitor from the past"
]
ALL_ROLES = MUST_HAVE_ROLES + GOOD_TO_HAVE_ROLES

# Directory to store role assignments
ASSIGNMENTS_DIR = "discussion_groups/discussion_assignments"
os.makedirs(ASSIGNMENTS_DIR, exist_ok=True)

def load_previous_assignments(discussion_number):
    """Load past assignments from JSON file."""
    file_path = os.path.join(ASSIGNMENTS_DIR, f"assignments_discussion_{discussion_number}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

def save_assignments(assignments, discussion_number):
    """Save updated assignments to a discussion-specific JSON file."""
    file_path = os.path.join(ASSIGNMENTS_DIR, f"assignments_discussion_{discussion_number}.json")
    with open(file_path, "w") as f:
        json.dump(assignments, f, indent=4)

def read_students(csv_file):
    """Read student names from a CSV file."""
    students = []
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f, delimiter=",")
        for row in reader:
            students.append(row["Student Name"])
    return students

def distribute_students(students, num_groups):
    """Distribute students into the requested number of groups as evenly as possible."""
    num_students = len(students)
    base_size = num_students // num_groups
    remainder = num_students % num_groups
    
    groups = []
    index = 0
    for i in range(num_groups):
        group_size = base_size + (1 if i < remainder else 0)
        groups.append(students[index:index + group_size])
        index += group_size
    
    return groups

def optimize_swaps(groups, assignments, previous_assignments):
    """Try to swap students between groups to reduce role repetition."""
    for i, group in enumerate(groups):
        for j, student in enumerate(group):
            past_roles = set(previous_assignments.get(student, []))
            current_role = assignments[student]
            if current_role in past_roles:
                # Try to find a swap candidate in another group
                for k, other_group in enumerate(groups):
                    if i == k:
                        continue  # Don't swap within the same group
                    for l, other_student in enumerate(other_group):
                        other_past_roles = set(previous_assignments.get(other_student, []))
                        other_role = assignments[other_student]
                        # Swap if it improves role variety
                        if other_role not in past_roles and current_role not in other_past_roles:
                            assignments[student], assignments[other_student] = assignments[other_student], assignments[student]
                            groups[i][j], groups[k][l] = groups[k][l], groups[i][j]  # Swap students in groups
                            break
    return assignments

def assign_roles(groups, previous_assignments):
    """Assign roles while ensuring students get different roles across discussions."""
    assignments = {}
    
    for group in groups:
        num_students = len(group)
        
        # Determine available roles based on group size
        if num_students <= len(ALL_ROLES):
            available_roles = MUST_HAVE_ROLES + GOOD_TO_HAVE_ROLES[:num_students - len(MUST_HAVE_ROLES)]
        else:
            repeats_needed = num_students - len(ALL_ROLES)
            available_roles = ALL_ROLES + MUST_HAVE_ROLES[:repeats_needed]
        
        random.shuffle(group)  # Shuffle students within the group
        
        assigned_roles = {}
        for student in group:
            past_roles = set(previous_assignments.get(student, []))
            possible_roles = [role for role in available_roles if role not in past_roles]
            
            if possible_roles:
                role = random.choice(possible_roles)
            else:
                role = random.choice(available_roles)  # Allow repeats if necessary
            
            assignments[student] = role
            assigned_roles[student] = role
            available_roles.remove(role)
    
    return optimize_swaps(groups, assignments, previous_assignments)

def main(csv_file, discussion_number, num_groups):
    random.seed(discussion_number)  # Set seed for reproducibility
    students = read_students(csv_file)
    random.shuffle(students)  # Shuffle students globally before grouping
    previous_assignments = load_previous_assignments(discussion_number)
    
    groups = distribute_students(students, num_groups)
    assignments = assign_roles(groups, previous_assignments)
    
    # Update assignment history
    for student, role in assignments.items():
        if student not in previous_assignments:
            previous_assignments[student] = []
        previous_assignments[student].append(role)
    
    save_assignments(previous_assignments, discussion_number)
    
    # Print results
    print(f"Discussion {discussion_number} Groups and Assignments:")
    for i, group in enumerate(groups, 1):
        print(f"\nGroup {i} (Size: {len(group)}):")
        sorted_group = sorted(group, key=lambda x: ALL_ROLES.index(assignments[x]))  # Sort by role priority
        for student in sorted_group:
            print(f"  {student}: {assignments[student]}")

if __name__ == "__main__":
    csv_file = "discussion_groups/data/roster 1-20-2025.csv"  # Update 
    discussion_number = 1 # Enter discussion number
    num_groups = 5 # Enter number of groups/papers selected
    main(csv_file, discussion_number, num_groups)
