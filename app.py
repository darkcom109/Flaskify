from flask import render_template, redirect, url_for, flash, request
import os
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from web_forms import SignUpForm, LoginForm, UpdateForm, PostForm, SearchForm
from models import Posts, Users, db, app
from valid_url import is_valid

csrf = CSRFProtect(app)
# Secret key - NEEDS TO BE CHANGED FOR SECURITY REASONS
secret = os.getenv("FORM_SECRET_KEY")
app.config['SECRET_KEY'] = secret

# Initialise LoginManager
login_manager = LoginManager(app)

login_manager.login_view = "login"
login_manager.login_message_category = "info"

# <--- INDEX PAGE --->
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

# <--- SIGNUP PAGE --->
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

# <--- LOGIN PAGE --->
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

# <--- LOAD USER --->
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# <--- LOGOUT VIEW --->
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "success")
    return redirect(url_for("login"))

# <--- COMMUNITY PAGE --->
@app.route('/posts')
@login_required
def posts():
    # Grab all posts from DB
    posts = Posts.query.order_by(Posts.date_posted.desc()).all()
    return render_template("posts.html", posts=posts)

# <--- VIEW POST PAGE --->
@app.route('/posts/<int:id>')
@login_required
def post(id):
    post = Posts.query.get_or_404(id)
    post.profile_picture = (post.profile_picture)[0:7]
    return render_template("post.html", post=post)

# <--- ADD POST PAGE --->
@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():

        number_of_posts = Posts.query.filter_by(user_id=current_user.id).count()
        print(number_of_posts)

        if number_of_posts >= 10:
            flash("You cannot have more than 10 posts due to spam policies", "danger")
            return redirect(url_for('dashboard'))

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

# <--- EDIT POSTS PAGE --->
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

# <--- DELETE POSTS PAGE --->
@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post = Posts.query.get_or_404(id)
    if current_user.id != post.user_id:
        flash("You cannot access this page", "danger")
        return redirect(url_for('dashboard'))
    try:
        db.session.delete(post)
        db.session.commit()
        flash("Blog post was Deleted", "success")
        return redirect(url_for('profile'))
    except:
        flash("There was a Problem Deleting the post", "danger")
        return redirect(url_for('profile'))

# <--- USER DASHBOARD PAGE --->
@app.route('/dashboard')
@login_required
def dashboard():
    progress = current_user.progress or []
    return render_template("dashboard.html", current_user=current_user, user_progress=set(progress))

# <--- USER LESSONS PAGE --->
@app.route('/dashboard/<string:lesson>')
def lesson(lesson):
    # To avoid template injection for security reasons
    if is_valid(lesson):
        return render_template(f"/lessons/{lesson}.html")
    else:
        return render_template("errors/404.html")

# <--- SAVE PROGRESS --->
@app.route("/save_progress", methods=['POST'])
@login_required
def save_progress():
    if not request.is_json:
        return {"success": False, "error": "JSON required"}, 400
    data = request.json
    current_user.progress = data.get("completed_lessons", [])
    db.session.commit()
    return {"success": True}

@app.route('/profile')
@login_required
def profile():
    posts = (Posts.query
             .filter_by(user_id = current_user.id)
             .order_by(Posts.date_posted.desc())
             .all())
    return render_template("profile.html", current_user=current_user, posts=posts)

# Update database record
@app.route('/update_profile/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if current_user.id != id:
        flash("You cannot access this page", "danger")
        return redirect(url_for('dashboard'))
    form = UpdateForm()
    name_to_update = Users.query.get_or_404(id)

    if form.validate_on_submit():
        name_to_update.name = form.name.data.strip()
        name_to_update.email = form.email.data.strip()
        name_to_update.bio = form.bio.data.strip()
        name_to_update.aspiring_job = form.aspiring_job.data.strip()
        try:
            db.session.commit()
            flash("User updated successfully!", "success")
            return redirect(url_for("profile"))
        except:
            flash("Error, try again!", "danger")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update)

@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/search', methods=["POST", "GET"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        search_term = f"%{form.searched.data.strip()}%"   # build the pattern safely
        posts = posts.filter(Posts.content.like(search_term))
        posts = posts.order_by(Posts.title).all()
        return render_template(
            "search.html", 
            form=form, 
            searched=form.searched.data, 
            posts=posts
        )

    return redirect(url_for("posts"))

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

# <-- MUST CHANGE BEFORE PRODUCTION -->
if __name__ == "__main__":
    app.run(debug=True)
