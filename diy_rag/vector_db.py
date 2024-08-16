from pathlib import Path
from pymilvus import MilvusClient


class MilvusDatabaseClient:
    def __init__(self, dimension=768) -> None:
        self.client = MilvusClient(str(Path(__file__).parent.parent / "rag.db"))
        self.dimension = dimension

    def init_collection(self):
        if self.client.has_collection(collection_name="texts"):
            self.client.drop_collection(collection_name="texts")

        self.client.create_collection(
            collection_name="texts",
            dimension=self.dimension,
        )

    def add_data(self, data):
        res = self.client.insert(collection_name="texts", data=data)
        return res

    def search(self, data, limit=1):
        return self.client.search(collection_name="texts", data=data, limit=limit, output_fields=["text"])
