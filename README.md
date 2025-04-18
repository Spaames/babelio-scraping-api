# Book Scraping API

An open-source Flask API that retrieves book information from the [Babelio](https://www.babelio.com) website. This API is used to power a personal book library management application ([Panthota]()).

## Features

- ***Babelio scraping***: Retrieves detailed book information based on the book title / author or ISBN.
- ***Data Return***: Returns data like title, author, cover image, summary.
- ***Frontend Communication***: This API is used by a Next.js application to display the results and store books in a MongoDB database.

## Installation

### Prerequisites

- **Python** version 3.13 or above
- **Poetry** to install dependencies

### Installation and Running Steps


```
git clone https://github.com/Spaames/babelio-scraping-api.git
cd babelio-scraping-api
poetry update
python3.13 app.py
```

By default, the app serves on localhost and on basic flask port (5000).
Edit the app.py to change this.

### Docker
You can use the dockerfile to build docker image or you can get it here : [babelio-scraping-api](https://hub.docker.com/layers/remidupuy/babelio-scraping-api/latest/images/sha256:10fd35d3e1b1a3b3f3aa9913cf9bd21a888f7695249cae38cc63284eb46a2339?uuid=cfc78975-47c1-43a8-bcb7-dbee6874def2%0A)

## Endpoints

- **/search** : GET -- params : query=<anything> --> return the result of the search field as a list of book (title, author, cover and book_url)
- **/book** : GET -- params : query=<book_url> --> return data for a specific book url, 

