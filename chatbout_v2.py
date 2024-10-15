# import jwt
# import torch
# from fastapi import APIRouter, Request
# from haystack.document_stores.in_memory import InMemoryDocumentStore
#
#
# from haystack import Document, Pipeline
# from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
# from haystack.components.readers import ExtractiveReader
#
# document_store = InMemoryDocumentStore()
#
# document_store.write_documents(
#     [
#         {"content": "프랑스의 수도는 파리야"},
#         {"content": "독일의 수도는 베를린이야"},
#         {"content": "한국의 수도는 서울이야"},
#         {"content": "미국의 수도는 워싱턴이야"},
#         {"content": "일본의 수도는 도쿄야"},
#     ]
# )
#
#
#
# retriever = InMemoryBM25Retriever(document_store)
# reader = ExtractiveReader(model="deepset/roberta-base-squad2")
# extractive_qa_pipeline = Pipeline()
# extractive_qa_pipeline.add_component("retriever", retriever)
# extractive_qa_pipeline.add_component("reader", reader)
# extractive_qa_pipeline.connect("retriever", "reader")
#
# query = "Which city is the capital of France?"
# result = extractive_qa_pipeline.run(data={
# 	"retriever": {"query": query, "top_k": 3},
# 	"reader": {"query": query, "top_k": 2}
# })
#
#



from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack import Document, Pipeline
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.readers import ExtractiveReader

document_store = InMemoryDocumentStore()
document_store.write_documents([
    Document(content="Paris is the capital of France."),
    Document(content="Berlin is the capital of Germany."),
    Document(content="Rome is the capital of Italy."),
    Document(content="Madrid is the capital of Spain."),
])

retriever = InMemoryBM25Retriever(document_store)
reader = ExtractiveReader(model="deepset/roberta-base-squad2")
extractive_qa_pipeline = Pipeline()
extractive_qa_pipeline.add_component("retriever", retriever)
extractive_qa_pipeline.add_component("reader", reader)
extractive_qa_pipeline.connect("retriever", "reader")

query = "What is the capital of France?"
result = extractive_qa_pipeline.run(data={
	"retriever": {"query": query, "top_k": 3},
	"reader": {"query": query, "top_k": 1}
})

# print(result)

# 가장 높은 점수의 답변만 추출
top_answer = result['reader']['answers'][0].data

print(top_answer)
