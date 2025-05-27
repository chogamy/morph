import os
from pydantic import BaseModel
import subprocess

from fastapi import FastAPI
from konlpy.tag import Mecab

import nltk
from nltk.tokenize import word_tokenize
import pandas as pd

nltk.download("punkt_tab")

DIR = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.abspath(os.path.join(DIR, "..", ".."))

app = FastAPI()


tokenizer = Mecab(os.path.join(DIR, "mecab-ko-dic-2.1.1-20180720"))


class Text(BaseModel):
    text: str


# TODO: 영어 단어도
# noun으로 변경 고려중
@app.post("/app/morph/")
def morph(text: Text):
    print("==== 한국어 형태소 분석 ====")
    print(f"입력 문장: {text.text}")

    nouns = tokenizer.nouns(phrase=text.text)
    output = " ".join(nouns)

    print(f"출력 문장: {output}")

    return {"text": output}


@app.post("/app/eng_morph/")
def eng_morph(text: Text):
    print("==== 영어 형태소 분석 ====")
    print(f"입력 문장: {text.text}")

    result = word_tokenize(text=text.text)
    output = " ".join(result)

    print(f"출력 문장: {output}")

    return {"text": output}


tokenizer = Mecab(os.path.join(DIR, "mecab-ko-dic-2.1.1-20180720"))


@app.post("/app/add_morph/")
def add_morph(text: Text):

    try:
        global tokenizer

        word = text.text.split(" ")[0]
        user_dic = os.path.join(DIR, "mecab-ko-dic-2.1.1-20180720", "NNP.csv")
        all_user_word_list = []
        with open(user_dic, "r", encoding="utf-8") as f:
            for line in f:
                all_user_word_list.append(line.split(",")[0])

        if word not in all_user_word_list:
            subprocess.run(
                ["make", "clean"],
                cwd=f"{os.path.join(DIR, 'mecab-ko-dic-2.1.1-20180720')}",
            )

            with open(user_dic, "a", encoding="utf-8") as f:
                f.write(f"{word},1786,3545,2953,NNP,*,F,{word},*,*,*,*\n")

            subprocess.run(
                ["bash", "./tools/add-userdic.sh"],
                cwd=f"{os.path.join(DIR, 'mecab-ko-dic-2.1.1-20180720')}",
            )
            subprocess.run(
                ["make"], cwd=f"{os.path.join(DIR, 'mecab-ko-dic-2.1.1-20180720')}"
            )
            subprocess.run(
                ["make", "install"],
                cwd=f"{os.path.join(DIR, 'mecab-ko-dic-2.1.1-20180720')}",
            )

        tokenizer = Mecab(os.path.join(DIR, "mecab-ko-dic-2.1.1-20180720"))

        return {"message": "성공"}

    except Exception as e:
        return {"message": str(e)}


# 형태소 분석 결과 추가 고려중
# @app.post("/app/morph/")
# def morph(text: Text):
#     pass

# TODO
# @app.post("/app/add_word/")
# def add_word(text: Text):
#     pass

# TODO
# @app.post("/app/remove_word/")
# def remove_word(text: Text):
#     pass


if __name__ == "__main__":
    print("test")
