import jwt
import torch
from fastapi import APIRouter, Request
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from pydantic import BaseModel

reader = FARMReader(model_name_or_path="deepset/xlm-roberta-large-squad2")

document_store = InMemoryDocumentStore(use_bm25=True)

document_store.write_documents(
    [
        {"content": "프랑스의 수도는 파리야"},
        {"content": "독일의 수도는 베를린이야"},
        {"content": "한국의 수도는 서울이야"},
        {"content": "미국의 수도는 워싱턴이야"},
        {"content": "일본의 수도는 도쿄야"},
    ]
)

retriever = BM25Retriever(document_store=document_store)

pipeline = ExtractiveQAPipeline(reader, retriever)

query = "Which city is the capital of France?"
# query = "이수는 여자야?"
# query = "구글 비밀 번호는?"

response = pipeline.run(query=query)
answer_object = response["answers"][0]

print("-----------------")
print(answer_object.answer)
print("-----------------")