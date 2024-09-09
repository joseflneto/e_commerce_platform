document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, password})
    });

    const result = await response.json();
    alert(result.message || result.error);
});

document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, password})
    });

    const result = await response.json();
    alert(result.message || result.error);
});

document.getElementById('placeOrderButton')?.addEventListener('click', async () => {
    const username = prompt('Enter your username to place the order');
    const response = await fetch('/place_order', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username})
    });

    const result = await response.json();
    alert(result.order_id ? `Order placed with ID: ${result.order_id}` : result.error);
});

// Manipulador para adicionar novos produtos
document.getElementById('addProductForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const productName = document.getElementById('productName').value;
    const productPrice = document.getElementById('productPrice').value;

    const response = await fetch('/add_product', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name: productName, price: productPrice})
    });

    const result = await response.json();
    alert(result.message || result.error);
});

document.getElementById('removeProductForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const productId = document.getElementById('productId').value;

    const response = await fetch('/remove_product', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({product_id: productId})
    });

    const result = await response.json();
    alert(result.message || result.error);
});
