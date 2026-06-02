from code import add_entry, get_category, delete_entry


# ==================================
# ENGINEERING SUBJECTS (60+)
# ==================================
ENGINEERING_SUBJECTS = [
    "Mathematics I",
    "Mathematics II",
    "Mathematics III",
    "Engineering Physics",
    "Engineering Chemistry",
    "Engineering Mechanics",
    "Environmental Science",
    "Engineering Graphics",
    "Basic Electrical Engineering",
    "Basic Electronics Engineering",

    "Programming in C",
    "Object Oriented Programming",
    "Python Programming",
    "Java Programming",
    "Data Structures",
    "Algorithms",
    "Discrete Mathematics",
    "Probability & Statistics",
    "Numerical Methods",
    "Optimization Techniques",

    "Digital Logic Design",
    "Computer Organization",
    "Computer Architecture",
    "Microprocessors",
    "Microcontrollers",
    "Embedded Systems",

    "Operating Systems",
    "Database Management Systems",
    "Software Engineering",
    "Theory of Computation",
    "Compiler Design",
    "Computer Networks",
    "Network Security",
    "Cyber Security",
    "Internet Technologies",

    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Data Science",
    "Big Data Analytics",
    "Data Mining",
    "Natural Language Processing",
    "Computer Vision",

    "Cloud Computing",
    "DevOps",
    "System Design",
    "Distributed Systems",
    "Parallel Computing",
    "High Performance Computing",

    "Web Development",
    "Frontend Development",
    "Backend Development",
    "Full Stack Development",
    "Mobile App Development",
    "UI/UX Design",

    "Blockchain",
    "Internet of Things",
    "AR/VR",
    "Quantum Computing",

    "Project Work",
    "Internship",
    "Technical Communication"
]


# ==================================
# CODING LANGUAGES / TECHNOLOGIES (40+)
# ==================================
CODING_LANGUAGES = [
    "Python",
    "C",
    "C++",
    "Java",
    "JavaScript",
    "TypeScript",
    "Go",
    "Rust",
    "Kotlin",
    "Swift",

    "PHP",
    "Ruby",
    "SQL",
    "R",
    "MATLAB",

    "Dart",
    "Scala",
    "Shell",
    "Assembly",
    "Perl",

    "Lua",
    "Julia",
    "Groovy",
    "Objective-C",
    "Fortran",

    "COBOL",
    "VB.NET",
    "C#",
    "F#",
    "Haskell",

    "HTML",
    "CSS",
    "React",
    "Angular",
    "Vue.js",

    "Node.js",
    "Flask",
    "Django",
    "Spring Boot",
    "FastAPI"
]


# ==================================
# ADD ENTRY
# ==================================
def log_entry(user, subject, problems, languages=None):

    if subject not in ENGINEERING_SUBJECTS:
        return False

    if languages is None:
        languages = []

    add_entry(
        user=user,
        category="study",
        topic=subject,
        problems=problems,
        languages=languages
    )

    return True


# ==================================
# FETCH ENTRIES
# ==================================
def fetch_entries(user):
    return get_category(user, "study")


# ==================================
# REMOVE ENTRY
# ==================================
def remove_entry(user, entry_id):
    delete_entry(user, "study", entry_id)


# ==================================
# SUBJECT ANALYTICS
# ==================================
def subject_stats(user):

    data = fetch_entries(user)

    stats = {}

    for item in data:

        subject = item["topic"]
        problems = item["problems"]

        stats[subject] = stats.get(subject, 0) + problems

    return stats


# ==================================
# LANGUAGE ANALYTICS
# ==================================
def language_stats(user):

    data = fetch_entries(user)

    stats = {}

    for item in data:

        for lang in item.get("languages", []):

            stats[lang] = stats.get(lang, 0) + item["problems"]

    return stats


# ==================================
# TOTAL STARS
# ==================================
def total_stars(user):

    data = fetch_entries(user)

    return sum(item.get("stars", 0) for item in data)


# ==================================
# TOTAL PROBLEMS
# ==================================
def total_problems(user):

    data = fetch_entries(user)

    return sum(item["problems"] for item in data)


# ==================================
# TOTAL ENTRIES
# ==================================
def total_entries(user):

    return len(fetch_entries(user))
