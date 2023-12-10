import pandas as pd
import os

# Step 1: Input file name
input_file = input("Enter the file name in folder Data:")

# Step 2: Read file from input
while True:
    try:
        with open(f"./data/{input_file}") as f:
            print(f"Successfully opened {input_file}")
            print("---------")
            input_lines = f.readlines()
            break
    except Exception as e:
        print(f"An error occurred: {e}")
        input_file = input("Re-enter the file name: ")

# Step 3: Get student answers
answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
answer_list = answer_key.split(",")
student_answers = []
invalid_lines = 0

for line in input_lines:
    line = line.strip()
    parts = line.split(",")

    if len(parts) != 26:
        print(f"Invalid answer data: {line}")
        invalid_lines += 1
        continue

    student_code = parts[0]
    student_answers_list = parts[1:]

    if not student_code.startswith("N") or not student_code[1:].isdigit() or len(student_code) != 9:
        print(f"Invalid student_code: {student_code}")
        invalid_lines += 1
    else:
        student_answers.append({
            "student_code": student_code,
            "answer_count": len(student_answers_list),
            "answer_list": student_answers_list,
        })

print("Total valid lines of data:", len(student_answers))
print("Total invalid lines of data:", invalid_lines)

# Step 4: Compute scores
student_scores = []
answers_statistic = []

for student in student_answers:
    student_code = student['student_code']
    score = 0

    if student['answer_count'] == 25:
        for index, answer in enumerate(student['answer_list']):
            if answer == answer_list[index]:
                score += 4
                answers_statistic.append({"question": index + 1, "correct": 1})
            elif answer == "":
                answers_statistic.append({"question": index + 1, "skip": 1})
            else:
                score -= 1
                answers_statistic.append({"question": index + 1, "fail": 1})

    student_scores.append({"student_code": student_code, "score": score})

# Step 5: Save file
output_dir = "Output"

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

with open(f"./{output_dir}/{input_file[:-4]}_grades.txt", "w") as f:
    for record in student_scores:
        f.write(f"{record['student_code']}, {record['score']}\n")

# Step 6: Calculate statistics
student_answers_df = pd.DataFrame(student_scores)
answers_statistic_df = pd.DataFrame(answers_statistic)

metric_1 = len(student_answers_df[student_answers_df['score'] > 80])
static_table = student_answers_df.describe()

print("**** REPORT ****")
print("Đếm số lượng học sinh đạt điểm cao (>80):", metric_1)
print("Mean (average) score:", static_table.loc['mean']['score'])
print("Highest score:", static_table.loc['max']['score'])
print("Lowest score:", static_table.loc['min']['score'])
print("Range of scores:", static_table.loc['max']['score'] - static_table.loc['min']['score'])
print("Median score:", static_table.loc['50%']['score'])

df = answers_statistic_df.groupby(['question']).agg({
    "correct": "sum",
    "fail": "sum",
    "skip": "sum",
}).reset_index()

df['skip_rate'] = df['skip'] / (df['correct'] + df['fail'] + df['skip'])
df['fail_rate'] = df['fail'] / (df['correct'] + df['fail'] + df['skip'])

most_skipped_questions = df.sort_values(by='skip', ascending=False)['skip'].max()
most_incorrect_questions = df.sort_values(by='fail', ascending=False)['fail'].max()

df_skip = df[df['skip'] == most_skipped_questions]
df_fail = df[df['fail'] == most_incorrect_questions]

print("Question that most people skip:")
print(df_skip[['question', 'skip', 'skip_rate']])

print("Question that most people answer incorrectly:")
print(df_fail[['question', 'fail', 'fail_rate']])
