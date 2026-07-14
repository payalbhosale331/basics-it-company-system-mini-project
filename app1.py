from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)

DATABASE = "business.db"


# Create Database
def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        price REAL,
        quantity INTEGER
    )
    """)

    conn.commit()
    conn.close()


create_database()


# HTML + CSS + JavaScript together
HTML = """

<!DOCTYPE html>
<html>
<head>

<title>Business Management System</title>

<style>

body{
    font-family: Arial;
    background:#f2f5f8;
    margin:0;
}

header{
    background:#1e88e5;
    color:white;
    padding:20px;
    text-align:center;
}


.container{
    width:90%;
    margin:auto;
}


.card{
    background:white;
    padding:20px;
    margin:20px;
    border-radius:10px;
    box-shadow:0 0 10px gray;
}


input,button{
    padding:10px;
    margin:5px;
}


button{
    background:#1e88e5;
    color:white;
    border:none;
    cursor:pointer;
}


button:hover{
    background:#1565c0;
}


table{
    width:100%;
    border-collapse:collapse;
}


th{
    background:#1e88e5;
    color:white;
}


td,th{
    padding:10px;
    border:1px solid #ddd;
}


.delete{
    background:red;
}


</style>

</head>


<body>


<header>
<h1>Business Management System</h1>
<p>Product Management Software</p>
</header>


<div class="container">


<div class="card">

<h2>Add Product</h2>


<input id="name" placeholder="Product Name">

<input id="category" placeholder="Category">

<input id="price" placeholder="Price">

<input id="quantity" placeholder="Quantity">


<button onclick="addProduct()">
Add Product
</button>


</div>



<div class="card">

<h2>Search Product</h2>

<input id="search"
placeholder="Search product"
onkeyup="loadProducts()">


</div>




<div class="card">


<h2>Products</h2>


<h3 id="total"></h3>


<table>


<thead>

<tr>

<th>ID</th>
<th>Name</th>
<th>Category</th>
<th>Price</th>
<th>Quantity</th>
<th>Action</th>

</tr>

</thead>


<tbody id="data">

</tbody>


</table>


</div>


</div>



<script>


function loadProducts(){


fetch('/products')

.then(res=>res.json())

.then(data=>{


let search=document.getElementById("search").value.toLowerCase();


let html="";

let total=0;


data.forEach(p=>{


if(p.name.toLowerCase().includes(search)){


total += p.price*p.quantity;


html+=`

<tr>

<td>${p.id}</td>

<td>${p.name}</td>

<td>${p.category}</td>

<td>${p.price}</td>

<td>${p.quantity}</td>


<td>

<button class="delete"
onclick="deleteProduct(${p.id})">
Delete
</button>

</td>


</tr>

`;

}

});


document.getElementById("data").innerHTML=html;


document.getElementById("total").innerHTML=
"Total Stock Value : ₹"+total;


});


}





function addProduct(){


let product={

name:name.value,

category:category.value,

price:price.value,

quantity:quantity.value

};


fetch('/add',
{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify(product)

})

.then(()=>{

alert("Product Added");

loadProducts();

});


}





function deleteProduct(id){


fetch('/delete/'+id)

.then(()=>{

alert("Deleted");

loadProducts();

});


}



loadProducts();


</script>


</body>
</html>

"""



@app.route("/")
def home():

    return render_template_string(HTML)



@app.route("/products")
def products():

    conn=sqlite3.connect(DATABASE)

    cursor=conn.cursor()

    cursor.execute("SELECT * FROM products")

    data=cursor.fetchall()

    conn.close()


    result=[]


    for p in data:

        result.append({

            "id":p[0],
            "name":p[1],
            "category":p[2],
            "price":p[3],
            "quantity":p[4]

        })


    return jsonify(result)





@app.route("/add",methods=["POST"])
def add():


    data=request.json


    conn=sqlite3.connect(DATABASE)

    cursor=conn.cursor()


    cursor.execute("""

    INSERT INTO products
    (name,category,price,quantity)

    VALUES(?,?,?,?)

    """,

    (
    data["name"],
    data["category"],
    data["price"],
    data["quantity"]
    ))


    conn.commit()

    conn.close()


    return "success"





@app.route("/delete/<int:id>")
def delete(id):


    conn=sqlite3.connect(DATABASE)

    cursor=conn.cursor()


    cursor.execute(
    "DELETE FROM products WHERE id=?",
    (id,)
    )


    conn.commit()

    conn.close()


    return "deleted"





if __name__=="__main__":

    app.run(debug=True)