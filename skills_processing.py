import pandas as pd
import re

PATH_TO_TECHNICAL_SKILLS = "data/technical_skills_20.csv"
PATH_TO_OCCUPATIONS = "data/occupations_20.csv"

df_skills = pd.read_csv(PATH_TO_TECHNICAL_SKILLS)
df_occupations = pd.read_csv(PATH_TO_OCCUPATIONS)

""" Clean skill names so that they can be properly counted (removes anything in parentheses) """
def preprocess_skills(row):
    row["Skill Name"] = re.sub(r" \(.*\)", "", row["Skill Name"])
    return row

# Call preprocess_skills to clean data
df_skills = df_skills.apply(preprocess_skills, axis=1)

""" Utility function that searches for skills using keywords """
def search_skills(skill):
    filtered_search = df_skills[df_skills["Skill Name"].str.contains(re.escape(skill), case=False)]
    unique_skills = filtered_search["Skill Name"].unique()
    return unique_skills

""" Prints the top_n most popular skills from the same skill category """
def related_skills(skill, top_n=5):
    print("Skills related to %s" % skill)
    filtered_search = df_skills[df_skills["Skill Name"].str.fullmatch(re.escape(skill))]
    # Here, we assume each skill belongs to a single category
    category = filtered_search["Skill Category"].unique()[0]
    category_search = df_skills[df_skills["Skill Category"] == category]
    category_search = category_search[category_search["Skill Name"] != skill]
    print(category_search["Skill Name"].value_counts().head(top_n))

### Uncomment for Demo
# related_skills(search_skills("HTML")[0])

""" Utility function that searches for industries using keywords """
def search_industries(industry):
    filtered_search = df_occupations[df_occupations["Job Category"].str.contains(re.escape(industry), case=False)]
    unique_industries = filtered_search["Job Category"].unique()
    return unique_industries

""" Prints the top_n most popular skills related to an industry """
def industry_skills(industry, top_n=10):
    filtered_search = df_occupations[df_occupations["Job Category"].str.fullmatch(re.escape(industry))]
    if (filtered_search.size == 0):
        return False
    occupation_ids = set(filtered_search["Occupation_ID"])
    industry_search = df_skills[df_skills["Occupation_ID"].isin(occupation_ids)]
    print("Skills popular in %s" % industry)
    print(industry_search["Skill Name"].value_counts().head(top_n))
    return True

""" Utility function that searches for occupations using keywords """
def search_occupations(occupation):
    filtered_search = df_occupations[df_occupations["Occupation"].str.contains(re.escape(occupation), case=False)]
    unique_jobs = filtered_search["Occupation"].unique()
    return unique_jobs

""" Prints the top_n most popular skills related to an occupation's industry """
def occupation_skills(occupation, top_n=10):
    filtered_search = df_occupations[df_occupations["Occupation"].str.fullmatch(re.escape(occupation))]
    industry_skills(filtered_search["Job Category"].iloc[0], top_n=top_n)

""" Prints skills related to either an occupation or industry (searches both) """
def job_skills_aggregate(search_term, top_n=10):
    return (industry_skills(search_term, top_n=top_n)) or (occupation_skills(search_term, top_n=top_n))

## Uncomment for Demo
# industry_skills(search_industries("software test")[0])
# print(search_occupations("software"))
# job_skills_aggregate("Statistical Assistants")
# job_skills_aggregate('Software Quality Assurance Analysts and Testers')
# job_skills_aggregate("Software Developers")
# job_skills_aggregate("Software testing/technician")
# job_skills_aggregate("Design", top_n=20)
