from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CN230'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'  # Database file will be created in the project folder
db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, default=0.0)
    num_ratings = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='recipe', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)


@app.route('/')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        title = request.form['title']
        image_url = request.form['image_url']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        new_recipe = Recipe(title=title, image_url=image_url, ingredients=ingredients, instructions=instructions)
        db.session.add(new_recipe)
        db.session.commit()

        flash('Recipe submitted successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('submit_recipe.html')

@app.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.method == 'POST':
        rating = float(request.form['rating'])

        recipe.rating = (recipe.rating * recipe.num_ratings + rating) // (recipe.num_ratings + 1)
        recipe.num_ratings += 1

        db.session.commit()

        flash('Thank you for rating the recipe!', 'success')

    return render_template('view_recipe.html', recipe=recipe)

@app.route('/rate_recipe/<int:recipe_id>', methods=['POST'])
def rate_recipe(recipe_id):
    # Implement rating a recipe logic here
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.method == 'POST':
        rating = float(request.form['rating'])

        recipe.rating = (recipe.rating * recipe.num_ratings + rating) / (recipe.num_ratings + 1)
        recipe.rating = round(recipe.rating,2)
        recipe.num_ratings += 1

        db.session.commit()
    return render_template('view_recipe.html',recipe=recipe)

@app.route('/comment/<int:recipe_id>', methods=['POST'])
def comment(recipe_id):
    if request.method == 'POST':
        content = request.form['content']

        new_comment = Comment(content=content, recipe_id=recipe_id)
        db.session.add(new_comment)
        db.session.commit()

        flash('Comment added successfully!', 'success')

    return redirect(url_for('view_recipe', recipe_id=recipe_id))



login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)