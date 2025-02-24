import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json, os, random
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#import matplotlib.pyplot as plt
question_file_path="Questions/ALL.json"

redo=[]
#redo=['PracticeExamination_17', '2023_Q6', 'Week7_5', '2023_Q5', 'Week7_4', 'Week4_3', '2023_Q18', 'Week11_8', '2023_Q20', 'Week11_4', 'Week7_6', '2023_Q16', '2023_Q8', 'PracticeExamination_16', 'PracticeExamination_7', '2023_Q15', 'Week2_5', 'PracticeExamination_20', 'PracticeExamination_10', '2023_Q10', 'Week11_1', 'Week11_5', 'PracticeExamination_4', 'PracticeExamination_12', '2023_Q9', 'Week4_4', 'PracticeExamination_19']
#redo=['2023_Q18', 'Week4_3', '2023_Q8', '2023_Q9', 'PracticeExamination_4', 'PracticeExamination_10']
#redo=['Week11_5', '2023_Q12', 'Week7_6', '2023_Q8', 'PracticeExamination_12', 'Week2_4', '2022_Q15', '2023_Q9']
#redo+=['2023_Q8', 'Week4_3', 'PracticeExamination_10', 'PracticeExamination_20', 'PracticeExamination_4', '2023_Q16', 'PracticeExamination_19', '2023_Q9', '2023_Q18']
#redo=['2022_Q14', 'Week11_3', '2022_Q3', 'Week2_2', '2022_Q16', '2023_Q17', '2023_Q6', 'PracticeExamination_20', 'PracticeExamination_16', '2022_Q13', 'PracticeExamination_1', 'PracticeExamination_19', '2022_Q18', '2022_Q18', '2022_Q4', 'Week9_1', 'Week4_3', 'Week7_5', 'PracticeExamination_14', '2023_Q10', '2022_Q8']





def rearrange_dict_keys(input_dict):
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N"]
    reordered_dict = {}
    values = list(input_dict.values())

    target_len=len(input_dict)
    i=0
    while i<target_len:
        reordered_dict[alphabet[i]]=values[i]
        i+=1
    return reordered_dict

def get_key_from_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None


def question_filter(questions, question_ids=[]):
    filtered_questions = []
    for question in questions:
        if question.get('id') in question_ids:
            filtered_questions.append(question)
    return filtered_questions

def question_filter_with_keywords(questions, keywords=[]):
    filtered_questions = []
    for question in questions:
        for i in keywords:
            if i in question.get('id'):
                filtered_questions.append(question)
    return filtered_questions

class QuizApp:
    def __init__(self, master):
        self.master = master
        master.title("Quiz App")
        button_frame = tk.Frame(master)

        button_frame.pack(side=tk.TOP, fill=tk.X)
        master.attributes('-fullscreen', True)
        self.quit_button = tk.Button(button_frame, text="Quit", command=self.quit)
        self.quit_button.pack(side=tk.LEFT)

        

        self.next_button = tk.Button(button_frame, text="Next", command=self.next_question)
        self.next_button.pack(side=tk.RIGHT)

        self.back_button = tk.Button(button_frame, text="Back", command=self.previous_question)
        self.back_button.pack(side=tk.RIGHT)
        
        self.labels = []  # Initialize labels list
        self.checkbox_vars = []  # Initialize checkbox_vars list

        
        self.questions = self.load_questions(question_file_path)
        # 题目过滤器
        #self.questions = question_filter(self.questions, question_ids=["Week1_1"])
        #self.questions = question_filter_with_keywords(self.questions, keywords=["3"])
        if len(redo)>0:
            self.questions = question_filter_with_keywords(self.questions, keywords=redo)
        #print(self.questions)
        self.json_dir = os.path.dirname(os.path.abspath(question_file_path))
        self.incorrect_ids = []
        self.questions_to_quiz = self.get_questions_to_quiz(self.questions, self.incorrect_ids)

        self.current_question_index = 0
        self.total_questions = len(self.questions_to_quiz)

        self.question_label = tk.Label(master, wraplength=400)
        self.question_label.pack()

        
        self.dropdowns = []
        self.checkboxes = []  # Initialize checkboxes list

        self.radio_var = tk.StringVar()
        self.radio_buttons = []
        for i in range(4):
            radio_button = tk.Radiobutton(master, text="", variable=self.radio_var, value="", command=self.select_answer)
            radio_button.pack(anchor="w")
            self.radio_buttons.append(radio_button)
        self.load_question()


    def previous_question(self):
        """Move to the previous question."""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.load_question()  # Added method to load previous question

    def load_questions(self, filename, randomQuestions=True, randomChoices=True):
        """Load questions from a file and shuffle them."""
        with open(filename, 'r') as file:
            data = json.load(file)
        questions = data['questions']
        if randomQuestions:
            random.shuffle(questions)  # 打乱问题顺序
        if randomChoices:
            for question in questions:
                if 'options' in question:
                    if len(question['answer'])==1:
                        original_options = list(question['options'].keys())
                        original_answer_value=question['options'][question['answer']]
                        options= original_options

                        random.shuffle(options)
                        question['options'] = {key: question['options'][key] for key in options}
                        question['options'] =rearrange_dict_keys(question['options'])
                        question['answer']=get_key_from_value(question['options'],original_answer_value)
                    elif len(question['answer'])>1:
                        original_options = list(question['options'].keys())
                        original_answer_options=question['answer']
                        answer_values=[]
                        for original_answer in original_answer_options:
                            answer_values.append(question['options'][original_answer])
                        options= original_options

                        random.shuffle(options)
                        question['options'] = {key: question['options'][key] for key in options}
                        question['options'] =rearrange_dict_keys(question['options'])
                        new_answer=""
                        for i in answer_values:
                            #print(i)
                            new_answer+=get_key_from_value(question['options'],i)
                        new_answer=sorted(new_answer)
                        question['answer']=new_answer
                    else:pass
                elif 'groups' in question:
                    groups = list(question['groups'].keys())
                    random.shuffle(groups)
                    question['groups'] = {key: question['groups'][key] for key in groups}
        #print(questions)
        return questions
    def get_questions_to_quiz(self, questions, incorrect_ids=None):
        """Get questions for the quiz based on incorrect IDs."""
        if incorrect_ids:
            return [q for q in questions if q['id'] in incorrect_ids]
        return questions

    def load_question(self):
        try:
            # Clear existing radio buttons
            for radio_button in self.radio_buttons:
                radio_button.pack_forget()
            self.radio_buttons.clear()
            self.radio_var.set("")
            self.question_label.pack_forget()

            # Clear existing dropdowns
            for dropdown in self.dropdowns:
                dropdown.destroy()
            self.dropdowns.clear()

            # Clear existing labels
            for label in self.labels:
                label.destroy()
            self.labels.clear()

            # Clear existing checkboxes
            for checkbox in self.checkboxes:
                checkbox.destroy()
            self.checkboxes.clear()

            # Clear existing checkbox variables
            del self.checkbox_vars[:]
        except Exception:
            pass

        if self.current_question_index < self.total_questions:
            question = self.questions_to_quiz[self.current_question_index]
            self.question_label.config(text=f"Question {self.current_question_index + 1}/{self.total_questions}: {question['question']}")
            self.question_label.pack()

            # Load image if provided
            image_path = question.get('image')
            if image_path:
                image_path = os.path.join(self.json_dir, image_path)
                self.load_image(image_path)
            else:
                self.load_image("")

            # Load options based on question type
            if 'options' in question:
                options = list(question['options'].values())
                for i, option in enumerate(options):
                    var = tk.BooleanVar()
                    checkbox = tk.Checkbutton(self.master, text=f"{chr(65+i)}. {option}", variable=var)
                    checkbox.pack(anchor="w")
                    self.checkbox_vars.append(var)
                    self.checkboxes.append(checkbox)  # Add checkbox to checkboxes list
                '''
                if len(question["answer"]) > 1:
                    # Multi-choice question
                    options = list(question['options'].values())
                    for i, option in enumerate(options):
                        var = tk.BooleanVar()
                        checkbox = tk.Checkbutton(self.master, text=f"{chr(65+i)}. {option}", variable=var)
                        checkbox.pack(anchor="w")
                        self.checkbox_vars.append(var)
                        self.checkboxes.append(checkbox)  # Add checkbox to checkboxes list
                else:
                    # Single-choice question
                    options = list(question['options'].values())
                    for i, option in enumerate(options):
                        radio_button = tk.Radiobutton(self.master, text=f"{chr(65+i)}. {option}", variable=self.radio_var, value=chr(65+i), command=self.select_answer)
                        radio_button.pack(anchor="w")
                        self.radio_buttons.append(radio_button)
                '''
            elif 'groups' in question:
                # Matching question
                self.load_matching_question(question['groups'])
        else:
            messagebox.showinfo("Quiz Finished", "Congratulations! You have finished the quiz.")
            messagebox.showinfo("错题列表", f"错题列表：{self.incorrect_ids}")
            self.master.quit()
            print(f"错题列表：{self.incorrect_ids}")

    def load_matching_question(self, groups):
        try:
            """Load a matching question."""
            # Clear existing radio buttons and labels
            for radio_button in self.radio_buttons:
                radio_button.pack_forget()
            self.radio_var.set("")
            self.question_label.pack_forget()

            # Clear existing dropdowns
            for dropdown in self.dropdowns:
                dropdown.destroy()
            self.dropdowns.clear()

            # Clear existing labels
            for label in self.labels:
                label.destroy()
            self.labels.clear()
        except Exception: pass

        # Load labels and dropdowns for each statement
        for g in groups.items():
            label = tk.Label(self.master, text=g[0])
            label.pack(anchor="w")
            self.labels.append(label)  # Add the label to the list
            dropdown = ttk.Combobox(self.master, values=list(groups.values()), state="readonly")
            dropdown.pack(anchor="w")
            self.dropdowns.append(dropdown)




    def load_image(self, image_path):
        try:
            if image_path=="":
                self.image_label.pack_forget()
            else:
                try:
                    self.image_label.pack_forget()
                except Exception:
                    pass
                self.image_label = tk.Label(self.master)
                self.image_label.pack()
                """Load and display the image."""
                image = Image.open(image_path)
                image = image.resize((300, 300))
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo)
                self.image_label.image = photo

        except Exception as ex:
            print(ex);pass

    def select_answer(self):
        """Handle answer selection."""
        pass
    def next_question(self):
        """Move to the next question."""
        selected_answer = self.radio_var.get()
        question = self.questions_to_quiz[self.current_question_index]
        
        if 'options' in question:
            selected_answers = [option for option, var in zip(question['options'].keys(), self.checkbox_vars) if var.get()]
            if len(selected_answers)<1:
                messagebox.showerror("Error", "Please select at least one answer."); return
            correct_answers = question['answer']
            #print(selected_answers)
            if set(selected_answers) == set(correct_answers):
                messagebox.showinfo("Result", "Correct!")
            else:
                messagebox.showinfo("Result", f"Incorrect. \n QuestionID: {question["id"]}\nCorrect answers: {', '.join(correct_answers)}")
                self.incorrect_ids.append(question['id'])
            self.current_question_index += 1
            self.load_question() 
            '''
            if len(question["answer"])>1:
                selected_answers = [option for option, var in zip(question['options'].keys(), self.checkbox_vars) if var.get()]
                if len(selected_answers)<1:
                    messagebox.showerror("Error", "Please select at least one answer."); return
                correct_answers = question['answer']
                #print(selected_answers)
                if set(selected_answers) == set(correct_answers):
                    messagebox.showinfo("Result", "Correct!")
                else:
                    messagebox.showinfo("Result", f"Incorrect. Correct answers: {', '.join(correct_answers)}")
                    self.incorrect_ids.append(question['id'])
                self.current_question_index += 1
                self.load_question() 
            else:
                if selected_answer:
                    correct_answer = question['answer']
                    if selected_answer == correct_answer:
                        messagebox.showinfo("Result", "Correct!")
                    else:
                        messagebox.showinfo("Result", f"Incorrect. Correct answer: {correct_answer}")
                        self.incorrect_ids.append(question['id'])
                    self.current_question_index += 1
                    self.load_question()
                else:
                    messagebox.showerror("Error", "Please select an answer.")
            '''
        elif 'groups' in question:
            # Matching question
            user_answers = [dropdown.get() for dropdown in self.dropdowns]
            for i in user_answers:
                if i=="":
                    messagebox.showerror("Error", "Please complete all choices.")
                    return
            
            #print(user_answers)
            correct_answers = list(question['groups'].values())
            #print(correct_answers)
            if user_answers == correct_answers:
                messagebox.showinfo("Result", "Correct!")
            else:
                messagebox.showinfo("Result", f"Incorrect. Correct answers: {correct_answers}",icon='error')
                self.incorrect_ids.append(question['id'])
            self.current_question_index += 1
            self.load_question()
        else:
            self.current_question_index += 1
            self.load_question()
        print(f"错题列表：{self.incorrect_ids}")
    def quit(self):
        """Quit the application with confirmation."""
        confirm = messagebox.askyesno("Confirm Exit", "Are you sure you want to quit?\n",icon='warning')
        if confirm:
            messagebox.showinfo("错题列表", f"列表同时也会在控制台输出\n{self.incorrect_ids}",icon='info')
            self.master.quit()
            print(f"错题列表：\n{self.incorrect_ids}")

root = tk.Tk()
root.iconbitmap('favicon.ico')
app = QuizApp(root)
root.mainloop()
