# aipiping_L3_Shivam

This is a scalable FastAPI application that provides travel recommendations for a given country and season using the OpenAI API. The application also uses background processing and MongoDB for storing and retrieving recommendations.

## Features
- FastAPI for building the API.
- MongoDB for storing recommendations.
- OpenAI API for generating recommendations.
- Background processing with FastAPI's background tasks.
- Docker Compose for containerizing the application.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- OpenAI API Key

### Setup

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    pip install -r 'requirements.txt'
    ```

2. Create a `.env` file in the project root with your OpenAI API key:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

3. Build and run the application using Docker Compose:

    ```sh
    docker-compose up --build
    ```

4. The application should now be running at `http://localhost:8000`.

### Usage

#### Create Recommendations

To create a recommendation, send a `POST` request to `/recommendations/` with the country and season.

Example:

```sh
curl -X POST "http://localhost:8000/recommendations/" -H "Content-Type: application/json" -d '{"country": "Canada", "season": "winter"}'

```
### Response:

{
  "uid": "unique-id"
}

Retrieve Recommendations
To retrieve a recommendation, send a GET request to /recommendations/{uid} with the UID from the previous step.

Example:


curl -X GET "http://localhost:8000/recommendations/{uid}"

Response:


{
  "uid": "unique-id",
  "country": "Canada",
  "season": "winter",
  "status": "completed",
  "recommendations": [
    "Go skiing in Whistler.",
    "Experience the Northern Lights in Yukon.",
    "Visit the Quebec Winter Carnival."
  ]
}




