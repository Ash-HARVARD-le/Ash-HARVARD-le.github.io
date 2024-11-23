from flask import Flask, render_template

# Create the Flask app instance
app = Flask(__name__)

# Route to render the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
  
@app.route('/about')
def about():
    return render_template('about.html', title='About Us')
