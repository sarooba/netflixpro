from flask import Flask, flash, render_template, request, redirect, url_for, session
import json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Dummy User
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Load movies from JSON file
def load_movies():
    with open("movies.json", "r") as file:
        return json.load(file)

# Home Route
@app.route("/")
def home():
    movies = load_movies()
    return render_template("home.html", movies=movies)

# Movie Detail Page
@app.route("/movie/<int:movie_id>")
def movie(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m["id"] == movie_id), None)
    if movie:
        return render_template("movie.html", movie=movie)
    return "Movie Not Found", 404

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Basic validation
        if not username or not password:
            flash('Please fill in all fields')
            return redirect(url_for('login'))
            
        if username == "admin" and password == "password":
            user = User(id=1)
            login_user(user)
            next_page = request.args.get('next')
            return redirect("dashboard") if next_page else redirect(url_for('home'))
        else:
            flash('Invalid credentials')
            
    return render_template("login.html")
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic validation
        if not all([email, username, password, confirm_password]):
            flash('Please fill in all fields')
            return redirect(url_for('register'))
            
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))
            
        if len(password) < 6 or len(password) > 60:
            flash('Password must be 6-60 characters')
            return redirect(url_for('register'))
            
        # In a real app, you would save the user to a database here
        # For now, we'll just log them in
        user = User(id=1)  # Replace with actual user creation
        login_user(user)
        flash('Registration successful!')
        return redirect(url_for('dashboard'))
        
    return render_template('register.html')
@app.route('/search')
def search():
    query = request.args.get('q', '')
    movies = [m for m in load_movies() if query.lower() in m['title'].lower()]
    return render_template('home.html', movies=movies)
# Add this route to your app.py
@app.route('/dashboard')
@login_required
def dashboard():
    print("DEBUG: Dashboard route accessed")
    # Sample data - in a real app you'd get this from your database
    continue_watching = [
        {"id": 1, "title": "Stranger Things", "poster": "https://image.tmdb.org/t/p/w500/xYZ9QP5nFa1G3JLC9f3R3EmN4Gz.jpg", "progress": 65},
        {"id": 2, "title": "The Witcher", "poster": "https://image.tmdb.org/t/p/w500/8WUVHemHFH2ZIP6NWkwlHWsyrEL.jpg", "progress": 30},
        {"id": 3, "title": "Money Heist", "poster": "https://image.tmdb.org/t/p/w500/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg", "progress": 80}
    ]
    
    hottest_movies = [
        {"id": 4, "title": "Dune", "poster": "https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg", "year": "2021"},
        {"id": 5, "title": "No Time to Die", "poster": "https://image.tmdb.org/t/p/w500/iUgygt3fscRoKWCV1d0C7FbM9TP.jpg", "year": "2021"},
        {"id": 6, "title": "The Batman", "poster": "https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg", "year": "2022"}
    ]
    
    recommended = [
        {"id": 7, "title": "Squid Game", "poster": "https://image.tmdb.org/t/p/w500/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg", "year": "2021"},
        {"id": 8, "title": "The Queen's Gambit", "poster": "https://image.tmdb.org/t/p/w500/zU0htwkhNvBQdVSIKB9s6hgVeFK.jpg", "year": "2020"},
        {"id": 9, "title": "Breaking Bad", "poster": "https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg", "year": "2008"}
    ]
    
    watchlist = [
        {"id": 10, "title": "The Mandalorian", "poster": "https://image.tmdb.org/t/p/w500/sWgBv7LV2PRoQgkxwlibdGXKz1S.jpg", "year": "2019"},
        {"id": 11, "title": "Loki", "poster": "https://image.tmdb.org/t/p/w500/kEl2t3OhXc3Zb9FBh1AuYzRTgZp.jpg", "year": "2021"}
    ]
    
    return render_template('dashboard.html', 
                         continue_watching=continue_watching,
                         hottest_movies=hottest_movies,
                         recommended=recommended,
                         watchlist=watchlist)


# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
