from typing import Optional
from trainer import Trainer
from fastapi import FastAPI, File, UploadFile
import numpy as np
import pandas as pd
import uvicorn
import tempfile

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/train_rules")
def train_rules(file: UploadFile = File(...)):
    trainer = Trainer()
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(file.file.read())
        _, df_rules = trainer.fit(fp.name)

    return {"df": df_rules}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=5000)
