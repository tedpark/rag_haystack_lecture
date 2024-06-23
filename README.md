# rag_haystack_lecture

## streamlit

streamlit run streamlit.py

## fastapi webserver

cd web_server

uvicorn main:app --reload --port=8000

## qna

http://127.0.0.1:8000/qna

{
"context": "나의 생일은 2월이야",
"question": "내가 태어난 월은?"
}

## question

http://127.0.0.1:8000/question

{
"question":"서울의 수도는?"
}
