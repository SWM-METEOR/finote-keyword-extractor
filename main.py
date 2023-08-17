from fastapi import FastAPI
from kiwipiepy import Kiwi
from krwordrank.sentence import summarize_with_sentences
from pydantic import BaseModel
import uvicorn

import body_request
import markdown_to_text


class Item(BaseModel):
    body_string: str


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/keyword")
async def keyword(bodyRequest: body_request.BodyRequest):
    result = markdown_to_text.markdown_to_text(bodyRequest)
    lines = result.strip().split('\n')
    kiwi = Kiwi()
    preprocessingResult = []
    for line in lines:
        newString = ""
        result = kiwi.analyze(line)
        for token, pos, _, _ in result[0][0]:
            if len(token) != 1 and pos.startswith('N') or pos.startswith('SL'):
                token += " "
                newString += token
        print(newString)
        preprocessingResult.append(newString)

    keywords, _ = summarize_with_sentences(
        preprocessingResult,
        penalty=None,
        stopwords=None,
        diversity=0.5,
        num_keywords=100,
        num_keysents=10,
        verbose=False
    )

    sorted_keywords = [
        {"keyword": word, "score": r}
        for word, r in sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10]
    ]

    return sorted_keywords
