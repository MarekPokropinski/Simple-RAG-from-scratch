# Simple RAG from scratch

This repository is a toy project with simple Retrieval-Augmented Generation system. 
System was build with pre-trained LLM's from LM Studio. For embeddings `nomic-ai/nomic-embed-text-v1.5-GGUF` model was used and for response generation: `Meta-Llama-3.1-8B-Instruct-GGUF`.

In notebook `langchain rag` similar application is implemented but using Langchain.

It is important to note that this is just simple solution for a model to have access to recent/private data. This model is still prone to hallucination and can respond with false and misleading statements.

## How to use

### Dependencies

First install used python packages:

```bash
pip install -r requirements.txt
```

### Models:

You can either use OpenAI models or self hosted. For self hosted download [LM Studio](https://lmstudio.ai/). 
In LM Studio download models for embeddings and for response generation (in ths repo `nomic-ai/nomic-embed-text-v1.5-GGUF` and `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF` were used). After downloading start local server in `Local Server` tab.

In `config.json` set url api key and model names for your models. If using LM Studio set url to http://localhost:1234/v1/ or your local IP if running LM Studio on windows and RAG in WSL and api key to `lm-studio`.

### Data
First download your target dataset to a directory. Each article should be in separate file and have its title as filename. As example dataset in this repo I used MediaWiki articles. [Vampire Survivors Wiki](https://vampire-survivors.fandom.com/wiki/Vampire_Survivors_Wiki) to be exact. When using this dataset be aware of licences of articles: https://www.fandom.com/licensing. 

To download data use `download_mediawiki.py` script. You can change url in script to download different wiki.

```bash
python download_mediawiki.py
```

To create vector database use `setup_data.py`.

```bash
python setup_data.py
```

It will remove previous database if it existed and create `rag.db` file. You need to have embedding model already running to generate vectors for database.

### Running

Example of running RAG is in `example.ipynb` notebook.

## Examples
```
Q: How do I unlock lightning ring in vampire survivors
A: To unlock Lightning Ring in Vampire Survivors, you need to defeat 5,000 enemies. It is also the starting weapon of Porta Ladonna.
```
```
Q: What is the damage of Hellfire?
A: According to the Vampire Survivors wiki, the base damage of Hellfire is 100 (+10). This means that the actual damage dealt by Hellfire will be its base damage plus any additional damage bonuses it may receive from other effects or upgrades.
```
```
Q: What is the evolution of Lightning ring and how do i get it?
A: The evolution of Lightning Ring is Thunder Loop. You can evolve Lightning Ring into Thunder Loop with Duplicator.
```
