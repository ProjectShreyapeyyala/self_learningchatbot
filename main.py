import json
from difflib import get_close_matches

# read from the file
def load_knowledgebase(file_path:str)->dict:
    with open(file_path,'r') as file:
        data:dict=json.load(file)
    return data

#write to the file
def save_knowledgebase(file_path:str,data:dict):
    with open(file_path,'w') as file:
        json.dump(data,file,indent=2)

def find_best_match(user_questions:str ,questions: list[str])->str | None:
    matches: list=get_close_matches(user_questions,questions,n=1,cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question:str,Knowledge:dict)->str |None:
    for q in Knowledge["questions"]:
        if q["questions"]==question:
            return q["answers"]


def chat_bot():
    knowledge: dict=load_knowledgebase("Knowledge.json")
    while True:
        user_input:str=input("you:")
        if user_input.lower()=="quit":
            break
        best_match: str | None=find_best_match(user_input,[q['questions']for q in knowledge["questions"]])
        if best_match:
            answer:str =get_answer_for_question(best_match,knowledge)
            print(f'bot:{answer}')
        else:
            print("Bot : I donot know the answer .Can you teach me?")
            new_answer:str =input("type the answer or 'skip' to skip:")
            if new_answer.lower()!='skip':
                knowledge['questions'].append({'questions':user_input,'answers':new_answer})
                save_knowledgebase('Knowledge.json',knowledge)
                print("Bot: Thank you!!, I learned a new response !")
if __name__=="__main__":
    chat_bot()
