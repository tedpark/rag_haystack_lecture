# pip install farm-haystack==1.17.2

from haystack.document_stores import FAISSDocumentStore
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever
from haystack.nodes import FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from pydantic import BaseModel

reader = FARMReader(model_name_or_path="deepset/xlm-roberta-large-squad2")


class Question(BaseModel):
    question: str


def question(question: Question):
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
    response = pipeline.run(query=question.question)
    answer_object = response["answers"][0]

    print("-----------------")
    print(answer_object.answer)
    print("-----------------")

    return {
        "answer": answer_object.answer,
        "score": answer_object.score + 0.2,
        "context": answer_object.context,
    }


class Qna(BaseModel):
    context: str
    question: str


def qna(qna: Qna):
    document_store = InMemoryDocumentStore(use_bm25=True)

    # token = jwt.decode(request.headers["authorization"].replace("Bearer ", ""), options={"verify_signature": False})
    # data = await request.app.state.database.content.find({"userId": token["profileId"]}).to_list(length=1000)
    # dict_list = [{"content": item["content"]} for item in data if item["content"]]

    document_store.write_documents([{"content": qna.context}])

    document_store.write_documents([{"content": ""}])

    retriever = BM25Retriever(document_store=document_store)
    pipeline = ExtractiveQAPipeline(reader, retriever)
    response = pipeline.run(query=qna.question)
    answer_object = response["answers"][0]

    print("-----------------")
    print(answer_object.answer)
    print("-----------------")

    return {
        "answer": answer_object.answer,
        "score": answer_object.score + 0.2,
        "context": answer_object.context,
    }


# qna(Qna(context="프랑스의 수도는 파리야", question="프랑스의 수도는 어디야?"))
qna(Qna(context="승환님은 올리브영이라는 회사에 다녀", question="승환님 회사는 어디야?"))
