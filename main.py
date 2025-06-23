import fitz, argparse, json, re

# Extracts text from each page of the PDF and joins them into one string
def extract_text(pdf_path):
    return " ".join(page.get_text() for page in fitz.open(pdf_path))

# Cleans the extracted text: removes special characters, collapses spaces, and lowercases everything
def clean(text):
    return re.sub(r'\s+', ' ', re.sub(r'[^A-Za-z0-9\s]', ' ', text)).lower()

# Matches each skill against the cleaned text and counts occurrences
def match_skills(text, skills):
    txt = clean(text)
    return {
        skill: len(re.findall(fr'\b{re.escape(skill.lower())}\b', txt))
        for skill in skills
    }

# Main execution starts here
if __name__ == "__main__":
    # Parse command-line argument for the resume PDF path
    parser = argparse.ArgumentParser(description="Ram's Resume Analyzer")
    parser.add_argument("pdf", help="Path to your resume (.pdf)")
    args = parser.parse_args()

    # Load the list of skills from a JSON file
    with open("skills.json") as f:
        skills = json.load(f)

    # Extract and analyze the resume text
    results = match_skills(extract_text(args.pdf), skills)

    # Find which skills are missing (mentioned zero times)
    missing = [skill for skill, count in results.items() if count == 0]

    # Print summary of all skill counts
    print("\nSkill Summary:")
    for skill, count in results.items():
        print(f"  {skill:<18}: {count}")

    # Print suggestions for missing skills
    if missing:
        print("\nSuggestions (Missing Skills):")
        for skill in missing:
            print(f"  - {skill}")
    else:
        print("\nAll key skills were found in the resume.")
