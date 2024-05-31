import json
import random


def load_questions(filename):
    """从文件中加载题目数据"""
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['questions']

def get_questions_to_quiz(questions, incorrect_ids=None):
    """根据错题ID列表获取需要答题的题目集"""
    if incorrect_ids:
        return [q for q in questions if q['id'] in incorrect_ids]
    return questions

def quiz(questions):
    if not questions:
        print("没有找到需要复习的错题。")
        return
    
    random.shuffle(questions)  # 打乱题目顺序
    incorrect_answers = []  # 用于记录错误题目的ID
    total_questions = len(questions)
    
    try:
        for index, question in enumerate(questions):
            print(f"问题 {index + 1}/{total_questions}: {question['question']}")
            original_options = question['options']
            items = list(original_options.items())
            random.shuffle(items)  # 打乱选项内容的顺序

            # 重新将选项按 A, B, C, D 的顺序组织
            sorted_options = {chr(65 + i): item[1] for i, item in enumerate(items)}
            correct_answer_letter = chr(65 + items.index((question['answer'], original_options[question['answer']])))
            
            # 打印选项
            for letter in sorted('ABCD'[:len(sorted_options)]):
                print(f"{letter}: {sorted_options[letter]}")
            
            while True:
                user_answer = input("请输入你的答案（例如A、B、C、D等）: ").strip().upper()
                if user_answer in sorted_options:
                    break
                else:
                    print("无效输入，请输入正确的选项字母。")
            
            # 比对答案
            if user_answer == correct_answer_letter:
                print("正确！\n")
            else:
                print(f"错误。正确答案是 {correct_answer_letter}。\n")
                incorrect_answers.append(question['id'])
    
    except KeyboardInterrupt:
        print("\n测试被用户中断。")

    finally:
        # 输出错误题目的ID列表
        if incorrect_answers:
            print("错误题目ID列表:", incorrect_answers)
        else:
            print("恭喜你，全部答对了！")

if __name__ == "__main__":
    questions = load_questions("FEA.json")  # 假设 JSON 文件名为 FEA.json
    # 假设这是错题ID列表，如果有的话
    incorrect_ids = []
    #incorrect_ids = [2, 10]  # 可以为空或者从外部读取
    questions_to_quiz = get_questions_to_quiz(questions, incorrect_ids)
    quiz(questions_to_quiz)