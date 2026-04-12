from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)