import argparse
import csv
import random

DEFAULT_PAPERS = [
    'Pandey, Punya Syon, Hai Son Le, Devansh Bhardwaj, Rada Mihalcea, and Zhijing Jin. 2025. "SocialHarmBench: Revealing LLM Vulnerabilities to Socially Harmful Requests." https://doi.org/10.48550/arXiv.2510.04891',
    'Peng, Shengyun, Pin-Yu Chen, Jianfeng Chi, Seongmin Lee, and Duen Horng Chau. 2025. "Shape It Up! Restoring LLM Safety during Finetuning." arXiv [Cs.LG]. arXiv. http://arxiv.org/abs/2505.17196',
    'Maini, Pratyush, Sachin Goyal, Dylan Sam, Alex Robey, Yash Savani, Yiding Jiang, Andy Zou, Zacharcy C. Lipton, and J. Zico Kolter. 2025. "Safety Pretraining: Toward the next Generation of Safe AI." arXiv [Cs.LG]. arXiv. http://arxiv.org/abs/2504.16980',
    'Mou, Yutao, Yuxiao Luo, Shikun Zhang, and Wei Ye. 2025. "SaRO: Enhancing LLM Safety through Reasoning-Based Alignment." arXiv [Cs.CL]. arXiv. http://arxiv.org/abs/2504.09420',
    'Lee, Andrew, Xiaoyan Bai, Itamar Pres, Martin Wattenberg, Jonathan K. Kummerfeld, and Rada Mihalcea. 2024. "A Mechanistic Understanding of Alignment Algorithms: A Case Study on DPO and Toxicity." arXiv [cs.CL]. arXiv. http://arxiv.org/abs/2401.01967',
    'Jing-Jing Li, Joel Mire, Eve Fleisig, Valentina Pyatkin, Anne Collins, Maarten Sap & Sydney Levine (2026) PluriHarms: Benchmarking the Full Spectrum of Human Judgments on AI Harm. ICLR. https://arxiv.org/abs/2601.08951'
]

ROLES = [
    "Within-Week Connector",
    "Evaluation and Validity Auditor",
    "Citation Trail Archaeologist",
    "Next-Step Study Designer",
    "Methodology Challenger"
]

def format_name(name):
    """Convert 'Last, First' to 'First Last'"""
    parts = name.split(", ")
    if len(parts) == 2:
        return f"{parts[1]} {parts[0]}"
    return name

def main():
    parser = argparse.ArgumentParser(description="Assign discussion roles to students for papers")
    parser.add_argument(
        "--papers", "-p",
        action="append",
        help="Paper citation (can be specified multiple times). If not provided, uses default paper list."
    )
    parser.add_argument(
        "--students-file", "-f",
        default="2026-02-13T1251_Grades-11430.csv",
        help="Path to the CSV file containing student grades (default: 2026-02-13T1251_Grades-11430.csv)"
    )
    parser.add_argument(
        "--exclude", "-e",
        action="append",
        help="Student to exclude (can be specified multiple times). 'Student, Test' is always excluded by default."
    )
    parser.add_argument(
        "--seed", "-s",
        type=int,
        default=20260213,
        help="Random seed for reproducibility (default: 20260213)"
    )
    args = parser.parse_args()
    
    random.seed(args.seed)

    # Use default papers if none provided
    paper_list = args.papers if args.papers else DEFAULT_PAPERS

    # Build exclusion list (always include "Student, Test")
    excluded_students = ["Student, Test"]
    if args.exclude:
        excluded_students.extend(args.exclude)

    # Read students from CSV
    students = []
    with open(args.students_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] and row[0] not in excluded_students:
                name = row[0].strip()
                if "," in name and not name.startswith("Student") and name != "Points Possible":
                    students.append(name)

    # Shuffle students for random assignment
    random.shuffle(students)

    num_papers = len(paper_list)
    num_students = len(students)
    base_students_per_paper = num_students // num_papers
    extra_students = num_students % num_papers

    # Assign students to papers
    assignments = {}
    student_idx = 0

    for paper_idx, paper in enumerate(paper_list):
        students_for_this_paper = base_students_per_paper + (1 if paper_idx < extra_students else 0)

        assignments[paper] = []
        for role_idx in range(students_for_this_paper):
            if student_idx < num_students and role_idx < len(ROLES):
                assignments[paper].append({
                    "student": students[student_idx],
                    "role": ROLES[role_idx]
                })
                student_idx += 1

    # Print assignments
    for paper_idx, (paper, assigned) in enumerate(assignments.items(), 1):
        print(f"- Group {paper_idx} (Size: {len(assigned)}): {paper}")
        for assignment in assigned:
            print(f"  - {format_name(assignment['student'])}: {assignment['role']}")
        print()

if __name__ == "__main__":
    main()
