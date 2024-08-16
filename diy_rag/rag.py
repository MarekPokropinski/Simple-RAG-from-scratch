import logging

from openai import OpenAI

from diy_rag.vector_db import MilvusDatabaseClient


logger = logging.getLogger(__name__)


class RAG:
    def __init__(self, *, url, api_key, embeddings_model, chat_model) -> None:
        self.ai_client = OpenAI(base_url=url, api_key=api_key)
        self.embeddings_model = embeddings_model
        self.chat_model = chat_model
        self.vector_db = MilvusDatabaseClient()

    def completion(self, text):
        system_message, user_message = self._prepare_system_message(text)
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        if user_message:
            messages.append({"role": "user", "content": user_message})
        completion = self.ai_client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0.7,
        )

        return completion.choices[0].message

    def _prepare_system_message(self, text, max_num_documents=10, distance_theshold=0.5):
        embed = self.get_embedding(text)
        [documents] = self.vector_db.search([embed], limit=max_num_documents)
        documents = filter(lambda doc: doc["distance"] > distance_theshold, documents)
        documents = map(lambda x: x["entity"]["text"], documents)
        documents = list(documents)
        # Reverse order of documents to have most relevant at the end. Having most relevant documents close to the question allows for more relevant answer.
        documents_text = "\n".join(reversed(documents))

        # system_text = "You are an expert assistant. Based on provided documents and wiki articles fulfill the user's requests to the best of your ability. " \
        # "If the information is missing from the documents respond: \"Result not found.\". Your response should be short and to the point. Only extract information from provided articles and don't add anything else. Here is the list of documents in MediaWiki format:\n" + documents_text

        # system_text = "You are an assistant for question-anwering tasks. Use the following pieces of retrieved context to answer the question. If you don't know, just say you don't know. Use three sentences maximum and keep the answer concise."
        # user_text = f"Question: {text}\nContext: {documents_text}"

        system_text = ""
        user_text = (
            "You are an assistant for question-anwering tasks. Use the following pieces of retrieved context to answer the question. If you don't know, just say you don't know. Use three sentences maximum and keep the answer concise.\n"
            + f"Answer the question based only on the following context:\n{documents_text}\n\n Question: {text}"
        )

        return system_text, user_text

    def get_embedding(self, text):
        return self.get_embeddings([text])[0]

    def get_embeddings(self, texts):
        # texts = [text.replace("\n", " ") for text in texts]
        data = self.ai_client.embeddings.create(input=texts, model=self.embeddings_model).data
        embeddings = [d.embedding for d in data]
        return embeddings
