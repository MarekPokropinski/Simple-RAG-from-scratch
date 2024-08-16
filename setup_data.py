from pathlib import Path

from diy_rag.config import load_config
from diy_rag.rag import RAG
from diy_rag.vector_db import MilvusDatabaseClient

data_path = Path("vs_data")

records = []


rag = RAG(**load_config())

for i, file_path in enumerate(data_path.glob("*")):
    with open(file_path, "r") as f:
        text = f.read()
        text = f"[title of article: {file_path.name}]\n{file_path.name}\n" + text
        records.append({"id": i, "vector": rag.get_embedding(text), "text": text})


vector_db = MilvusDatabaseClient()
vector_db.init_collection()
vector_db.add_data(records)
