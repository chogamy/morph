import os
from pydantic import BaseModel

from fastapi import FastAPI
from konlpy.tag import Mecab

DIR = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.abspath(os.path.join(DIR, "..", ".."))

app = FastAPI()


tokenizer = Mecab(os.path.join(DIR, "mecab-ko-dic-2.1.1-20180720"))


class Text(BaseModel):
    text: str


@app.post("/app/noun/")
def morph(text: Text):

    nouns = tokenizer.nouns(phrase=text.text)

    return {"text": " ".join(nouns)}


# TODO: 언어분기
# TODO: 형태소 분석 결과
# TODO: 사용자 단어 추가
