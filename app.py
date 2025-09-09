from flask import render_template, redirect, url_for, flash, request
import os
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from web_forms import SignUpForm, LoginForm, UpdateForm, PostForm, SearchForm
from models import Posts, Users, db, app, ckeditor

# Secret key
app.config['SECRET_KEY'] = os.getenv("FORM_SECRET_KEY", "dev-secret")

# Initialise LoginManager
login_manager = LoginManager(app)

login_manager.login_view = "login"
login_manager.login_message_category = "info"

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/search', methods=["POST", "GET"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        post.searched = form.searched.data
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template("search.html", form=form, searched=post.searched, posts=posts)
    
    return redirect(url_for("posts"))

@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post = Posts.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        flash("Blog post was Deleted", "success")
        return redirect(url_for('profile'))
    except:
        flash("There was a Problem Deleting the post", "danger")
        return redirect(url_for('profile'))

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
    post.profile_picture = (post.profile_picture)[0:7]
    return render_template("post.html", post=post)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    if current_user.id != post.user_id:
        flash("You cannot access this page", "danger")
        return redirect(url_for('dashboard'))
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.content = form.content.data.strip()
        # Update db
        db.session.add(post)
        db.session.commit()
        flash("Post has been Updated Successfully", "success")
        return redirect(url_for('post', id=post.id))
    
    form.title.data = post.title
    form.content.data = post.content

    return render_template("edit_post.html", form=form)

# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(title=form.title.data.strip(),
                     content=form.content.data.strip(),
                     author=current_user.name,
                     user_id=current_user.id,
                     profile_picture=current_user.profile_picture)
        # Clear form
        form.title.data = ''
        form.content.data = ''
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
             .filter_by(user_id = current_user.id)
             .order_by(Posts.date_posted.desc())
             .all())
    return render_template("profile.html", current_user=current_user, posts=posts)

# Update database record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if current_user.id != id:
        flash("You cannot access this page", "danger")
        return redirect(url_for('dashboard'))
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

from flask import render_template

# 400 – Bad Request
@app.errorhandler(400)
def bad_request(e):
    return render_template("errors/400.html"), 400

# 401 – Unauthorized
@app.errorhandler(401)
def unauthorized(e):
    return render_template("errors/401.html"), 401

# 403 – Forbidden
@app.errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403

# 404 – Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404

# 405 – Method Not Allowed
@app.errorhandler(405)
def method_not_allowed(e):
    return render_template("errors/405.html"), 405

# 429 – Too Many Requests
@app.errorhandler(429)
def too_many_requests(e):
    return render_template("errors/429.html"), 429

# 500 – Internal Server Error
@app.errorhandler(500)
def internal_error(e):
    return render_template("errors/500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)
