# Flask Project

This is a simple Flask application that processes text and handles requests. Below are the instructions to set up and run the application.

## Prerequisites

- Docker installed on your machine.
- Python 3.x (if running locally without Docker).

## Project Structure

```
flask-project
├── app.py              # Main application code
├── Dockerfile          # Dockerfile for building the image
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-project
   ```

2. Install dependencies (if running locally):
   ```
   pip install -r requirements.txt
   ```

## Running the Application

### Using Docker

1. Build the Docker image:
   ```
   docker build -t flask-project .
   ```

2. Run the Docker container:
   ```
   docker run -p 5000:5000 flask-project
   ```

3. Access the application at `http://localhost:5000`.

### Running Locally

If you prefer to run the application locally without Docker, execute the following command:
```
python app.py
```
Then, access the application at `http://localhost:5000`.

## License

This project is licensed under the MIT License.