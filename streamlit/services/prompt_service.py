# streamlit/services/prompt_service.py

from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv 

load_dotenv()

# 프롬프트 가져오는 함수
def make_prompt(prompt_name):
    with open(f"./prompts/{prompt_name}.txt", "r") as f:
        template = f.read()
    
    prompt = PromptTemplate.from_template(template)

    return prompt

def make_chain(model, prompt_name, output_parser):
    prompt = make_prompt(prompt_name)

    chain = prompt | model | output_parser 

    return chain 


# 모델 로드
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# 요약
summary_chain = make_chain(
    model=model,
    prompt_name="summary_prompt",
    output_parser=StrOutputParser()
)
todo_chain = make_chain(
    model=model,
    prompt_name="todo_prompt",
    output_parser=CommaSeparatedListOutputParser()
)
schedule_chain = make_chain(
    model=model,
    prompt_name="schedule_prompt",
    output_parser=JsonOutputParser()
)

