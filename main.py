# Import create_app from 'website' to start the Flask application
from website import create_app

# Create an instance of the Flask application
# Sets up the app with all required routes and databases
app = create_app()

# Check if the script is being run directly and start the local server
if __name__ == '__main__':
    # Debug moment
    app.run(debug=True)
