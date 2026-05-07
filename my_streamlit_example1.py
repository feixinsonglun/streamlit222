import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
print(f".env 文件路径: {dotenv_path}")
load_dotenv(dotenv_path)

os.environ["LANGCHAIN_TRACING_V2"] = os.environ.get("LANGSMITH_TRACING", "true")
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGSMITH_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGSMITH_PROJECT", "default")

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

print("=== LangSmith 配置检查 ===")
print(f"LANGSMITH_TRACING: {os.environ.get('LANGSMITH_TRACING')}")
print(f"LANGSMITH_API_KEY: {os.environ.get('LANGSMITH_API_KEY')}")
print(f"LANGSMITH_PROJECT: {os.environ.get('LANGSMITH_PROJECT')}")
print(f"Deepseek_API_KEY: {os.environ.get('Deepseek_API_KEY')}")
print("=========================")

st.title('🦜🔗 中文小故事生成器')

def get_api_key():
    return os.environ.get("Deepseek_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""

prompt = ChatPromptTemplate.from_template("请编写一篇关于{topic}的中文小故事，不超过100字")

model = ChatOpenAI(
    base_url="https://api.deepseek.com/v1",
    api_key=get_api_key(),
    model="deepseek-chat",
    temperature=0.8
)

chain = prompt | model

with st.form('my_form'):
    text = st.text_area('输入主题关键词:', '小白兔')
    submitted = st.form_submit_button('提交')
    if submitted:
        st.info(chain.invoke({"topic": text}))