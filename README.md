# Music_Search_Engine

**This project is about building a basic search engine and use it for music services.**

The search engine implements the following functions:
- Web Crawler to discover and download web documents.
- Indexer to produce inverted index database.
- Query Handler for accepting user queries from the web interface, produce shorted results and serve them back to the user.
- Web interface, the user friendly tool for communication between the user and the
search engine

## Screenshots
Web interface

![screenshot](https://github.com/Charalampidis87/Music_Search_Engine/blob/main/Assets/search_results.png)

Suggestion function (Did you mean?)

![screenshot](https://github.com/Charalampidis87/Music_Search_Engine/blob/main/Assets/suggestions.png)

Operational infrastructure of the engine.

![infrastructure](https://github.com/Charalampidis87/Music_Search_Engine/blob/main/Assets/infrastructure.png)

## Pre-requirements
To **run** this project, you will need:
- [Python](https://www.python.org/downloads/) (Version 3 used for this project)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/installation/) (for web interface. To install `pip install flask`)

## How to run it
Before running, set the `start_url` parameter in crawler file `Crawler.py`. The `start_url` provides the crawler the starting point for crawling and downloading web documents, and also limits the crawler to download web documents only if those are below the `start_url` (match prefix).

To run the search engine, start the `main.py` file. From terminal run `python .\main.py`.

The Music_Search_Engine will start crawling from the `start_url` and create inverted index database. After finishing this process, the web interface will launch and the engine can accept and answer search queries. If the inverted index already exists (`inverted_index.json` file), the crawling process will not execute.

___
> You can find full documentation [here](https://github.com/Charalampidis87/Music_Search_Engine/blob/main/Assets/Project_Documentation.pdf)