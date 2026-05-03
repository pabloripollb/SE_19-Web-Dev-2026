from flask import Flask, render_template, request, redirect, session
from mongoengine import connect, Document, StringField, DateTimeField
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

connect(host=os.environ.get('MONGODB_URI'))

class Blog(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    date = DateTimeField(default=datetime.datetime.utcnow)

products_data = {
    1: {"name": "Magic mirror", "desc": "You can see yourself in it", "price": "Gazillion dollars"},
    2: {"name": "Super H2O", "desc": "The ultimate hydration solution", "price": "Billion dollars"},
    3: {"name": "Breathable Air", "desc": "Clean, fresh air for your home", "price": "Million dollars"}
}

@app.route('/')
def home():
    return render_template('index.html', products=products_data)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = products_data.get(product_id)
    if product:
        return render_template('product.html', product=product)
    else:
        return render_template('404.html'), 404

@app.route('/blog')
def blog():
    posts = Blog.objects()
    return render_template('blog.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == os.environ.get('ADMIN_PASSWORD'):
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            return "<h1>Wrong password!</h1><br><a href='/login'>Try again</a>"
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('admin_logged_in'):
        return redirect('/login')

    if request.method == 'POST':
        form_title = request.form.get('title')
        form_content = request.form.get('content')
        new_post = Blog(title=form_title, content=form_content)
        new_post.save()
        return redirect('/admin')
        
    posts = Blog.objects()
    return render_template('admin.html', posts=posts)

@app.route('/admin/delete/<post_id>')
def delete_post(post_id):
    if not session.get('admin_logged_in'):
        return redirect('/login')
        
    post = Blog.objects(id=post_id).first()
    if post:
        post.delete()
        
    return redirect('/admin')

@app.route('/admin/edit/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if not session.get('admin_logged_in'):
        return redirect('/login')
        
    post = Blog.objects(id=post_id).first()
    if not post:
        return render_template('404.html'), 404
        
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.save()
        return redirect('/admin')
        
    return render_template('edit.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)