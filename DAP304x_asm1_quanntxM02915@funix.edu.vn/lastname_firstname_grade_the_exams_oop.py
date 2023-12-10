import pandas as pd


class AssignmentOne:
    def __init__(self, input_file):
        self.answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
        self.answer_list = self.answer_key.strip().split(",")
        self.input_file = input_file
        self.student_answers = []
        self.student_scores = []

        # create object for computing the answers statistic
        self.answers_statistic = []

    def read_file_from_input(self):
        while True:
            if self.input_file:
                try:
                    f = open(f"DAP304x_asm1_quanntxM02915@funix.edu.vn/data/{self.input_file}")
                    print(f"Successfully opened {self.input_file}")
                    print("---------")

                    break  # Exit the loop after successful file processing
                except Exception as e:
                    print(f"An error occurred: {e}")
                    self.input_file = input("Re-enter the file name: ")
        return f

    def get_student_answers(self) -> None:
        _f = self.read_file_from_input()
        invalid_lines = 0
        for line in _f:
            line = line.rstrip("\n")

            line = list(line.strip().split(","))

            student_code = line[0]

            answer_count = len(line[1:])

            self.student_answers.append(
                {
                    "student_code": student_code,
                    "answer_count": answer_count,
                    "answer_list": line[1:]
                }
            )

            student_num = student_code[1:]
            # print error
            if (student_code[0:1] != "N") or (isinstance(student_num, int)) or (len(student_num) != 8):
                print("Invalid student_code: ", student_code, len(str(student_num)))
                print("---------")
                invalid_lines += 1
            elif answer_count != 25:
                print(f"Invalid answer for student {student_code}: {answer_count} values")
                print("---------")
                invalid_lines += 1
        print("Total valid lines of data: ", len(self.student_answers))
        print("Total invalid lines of data: ", invalid_lines)

    def compute_scores(self):
        # Loop though each student and get data
        for student in self.student_answers:
            student_code = student.get('student_code')
            score = 0
            if student.get('answer_count') == 25:
                for index, answer in enumerate(student.get('answer_list')): # or isdigit()
                    if answer == self.answer_list[index]:
                        score += 4
                        # if correct, insert 1 record for correct
                        self.answers_statistic.append({
                            "question": index + 1,
                            "correct": 1
                        })
                    elif answer == "":
                        self.answers_statistic.append({
                            "question": index + 1,
                            "skip": 1
                        })
                    elif answer != self.answer_list[index]:
                        score -= 1
                        self.answers_statistic.append({
                            "question": index + 1,
                            "fail": 1
                        })
            # get score data
            self.student_scores.append({
                "student_code": student_code,
                "score": score
            })

    def save_file(self):
        # Save the file
        import os
        output_dir = "../Output"

        # check if output exist
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        # get file name with name & _grades.txt
        with open(f"./{output_dir}/{input_file[:-4]}_grades.txt", "w") as f:
            for record in self.student_scores:
                # convert value to list
                values = [str(value) for value in record.values()]

                f.write(', '.join(values) + '\n')

    def statistic(self):
        student_answers_df = pd.json_normalize(self.student_scores)

        # Aggregate results data for answer
        answers_statistic_df = pd.json_normalize(self.answers_statistic)

        metric_1 = len(student_answers_df.loc[student_answers_df['score'] > 80])
        static_table = student_answers_df.describe()
        # print(static_table)

        print("**** REPORT ****")
        print("Đếm số lượng học sinh đạt điểm cao (>80):", metric_1)
        print("Mean (average) score:", static_table.loc['mean']['score'])
        print("Highest score:", static_table.loc['max']['score'])
        print("Lowest score:", static_table.loc['min']['score'])
        print("Range of scores:", static_table.loc['max']['score'] - static_table.loc['min']['score'])
        print("Median score:", static_table.loc['50%']['score'])
        print(answers_statistic_df)

        df = answers_statistic_df.groupby(['question']).agg({
            "correct": "sum",
            "fail": "sum",
            "skip": "sum",
        }).reset_index()

        # Tính tỷ lệ bỏ qua và trả lời sai cho từng câu hỏi
        df.loc[:, 'skip_rate'] = df['skip'] / (df['correct'] + df['fail'] + df['skip'])
        df.loc[:, 'fail_rate'] = df['fail'] / (df['correct'] + df['fail'] + df['skip'])

        # Số lần bỏ qua nhiều nhất
        most_skipped_questions = df.sort_values(by='skip', ascending=False)['skip'].max()

        # Số lần sai nhiều nhất
        most_incorrect_questions = df.sort_values(by='fail', ascending=False)['fail'].max()

        # Lấy danh sách các câu hỏi có tỷ lệ bỏ qua và trả lời sai cao nhất
        df_skip = df.loc[df['skip'] == most_skipped_questions]
        df_fail = df.loc[df['fail'] == most_incorrect_questions]

        print("Question that most people skip:")
        print(df_skip[['question', 'skip', 'skip_rate']])

        print("Question that most people answer incorrectly:")
        print(df_fail[['question', 'fail', 'fail_rate']])


if __name__ == "__main__":
    input_file = input("Enter the file name in folder Data:")
    assignmentFile = AssignmentOne(input_file=input_file)

    # handle file
    assignmentFile.read_file_from_input()
    assignmentFile.get_student_answers()
    assignmentFile.compute_scores()
    assignmentFile.save_file()

    # output
    assignmentFile.statistic()
