from app import create_app

# Initialize the Flask application using the factory pattern
app = create_app()

if __name__ == "__main__":
    # Run the application in debug mode (auto-reloads when you save code changes)
    app.run(debug=True)
