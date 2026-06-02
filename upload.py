import pandas as pd

from code import add_entry
from study import (
    ENGINEERING_SUBJECTS,
    CODING_LANGUAGES
)


# ==================================
# CSV UPLOAD
# ==================================
def upload_file(user, file, category="study"):

    """
    CSV FORMAT

    topic,problems,languages

    Example:

    Data Structures,20,"Python,Java"
    DBMS,15,"SQL"
    Operating Systems,10,"C,C++"
    """

    try:

        df = pd.read_csv(file)

        # -------------------------
        # REQUIRED COLUMNS
        # -------------------------
        required = ["topic", "problems"]

        for col in required:

            if col not in df.columns:
                return f"❌ Missing column: {col}"

        success_count = 0

        # -------------------------
        # PROCESS ROWS
        # -------------------------
        for _, row in df.iterrows():

            topic = str(row["topic"]).strip()

            try:
                problems = int(row["problems"])
            except:
                continue

            # -------------------------
            # LANGUAGES
            # -------------------------
            languages = []

            if "languages" in df.columns:

                if pd.notna(row["languages"]):

                    languages = [
                        lang.strip()
                        for lang in str(
                            row["languages"]
                        ).split(",")
                        if lang.strip()
                    ]

            # -------------------------
            # VALIDATE SUBJECT
            # -------------------------
            if category == "study":

                if topic not in ENGINEERING_SUBJECTS:
                    continue

            # -------------------------
            # VALIDATE LANGUAGES
            # -------------------------
            valid_languages = []

            for lang in languages:

                if lang in CODING_LANGUAGES:
                    valid_languages.append(lang)

            # -------------------------
            # SAVE ENTRY
            # -------------------------
            add_entry(
                user=user,
                category=category,
                topic=topic,
                problems=problems,
                languages=valid_languages
            )

            success_count += 1

        return (
            f"✅ Upload Successful\n\n"
            f"Imported {success_count} entries."
        )

    except Exception as e:

        return f"❌ Upload Error: {str(e)}"
