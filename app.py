from flask import render_template, redirect, url_for, flash, request
import os
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from web_forms import SignUpForm, LoginForm, UpdateForm, PostForm
from models import Posts, Users, db, app

# Secret key
app.config['SECRET_KEY'] = os.getenv("FORM_SECRET_KEY", "dev-secret")

# Initialise LoginManager
login_manager = LoginManager(app)

login_manager.login_view = "login"
login_manager.login_message_category = "info"

@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post = Posts.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        flash("Blog post was Deleted", "success")
        return redirect(url_for('posts'))
    except:
        flash("There was a Problem Deleting the post", "danger")
        return redirect(url_for('posts'))

@app.route('/posts')
@login_required
def posts():
    # Grab all posts from DB
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)

@app.route('/posts/<int:id>')
@login_required
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post.html", post=post)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        # Update db
        db.session.add(post)
        db.session.commit()
        flash("Post has been Updated Successfully", "success")
        return redirect(url_for('post', id=post.id))
    
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content

    return render_template("edit_post.html", form=form)

# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(title=form.title.data,
                     content=form.content.data,
                     author=form.author.data,
                     slug=form.slug.data,
                     user_id=current_user.id)
        # Clear form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''
        # Add post data to db
        db.session.add(post)
        db.session.commit()

        flash("Blog Post Submitted Successfully", "success")
        return redirect(url_for('posts'))
    
    return render_template("add_post.html", form=form)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "success")
    return redirect(url_for("login"))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", current_user=current_user)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        hashed_pw = generate_password_hash(
            form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )

        user = Users(
            name=form.name.data, 
            email=form.email.data, 
            password=hashed_pw
        )
        
        db.session.add(user)
        db.session.commit()
        flash("Your Account was Successfully Made", "success")
        return redirect(url_for("login"))
    
    return render_template("signup.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Login failed. Check your username or password", "danger")
        
    return render_template("login.html", form=form)

@app.route('/profile')
@login_required
def profile():
    posts = (Posts.query
             .filter_by(user_id = current_user.id)     # only YOUR posts
             .order_by(Posts.date_posted.desc())     # newest first, because we live in 2025
             .all())
    return render_template("profile.html", current_user=current_user, posts=posts)

# Update database record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UpdateForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.bio = request.form['bio']
        name_to_update.aspiring_job = request.form['aspiring_job']
        try:
            db.session.commit()
            flash("User updated successfully!", "success")
            return redirect(url_for("profile"))
        except:
            flash("Error, try again!", "danger")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update)

@app.route('/dashboard/lesson_zero')
@login_required
def lesson_zero():
    return render_template("/lessons/lesson_zero.html")

@app.route('/dashboard/lesson_one')
@login_required
def lesson_one():
    return render_template("/lessons/lesson_one.html")

@app.route('/dashboard/lesson_two')
@login_required
def lesson_two():
    return render_template("/lessons/lesson_two.html")

@app.route('/dashboard/lesson_three')
@login_required
def lesson_three():
    return render_template("/lessons/lesson_three.html")

@app.route('/dashboard/lesson_four')
@login_required
def lesson_four():
    return render_template("/lessons/lesson_four.html")

@app.route('/dashboard/lesson_five')
@login_required
def lesson_five():
    return render_template("/lessons/lesson_five.html")

@app.route('/dashboard/lesson_six')
@login_required
def lesson_six():
    return render_template("/lessons/lesson_six.html")

@app.route('/dashboard/project_one')
@login_required
def project_one():
    return render_template("/lessons/project_one.html")

if __name__ == "__main__":
    app.run(debug=True)
