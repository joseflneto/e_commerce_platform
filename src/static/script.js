document.addEventListener('DOMContentLoaded', () => {
    // Helper function to display messages
    function displayMessage(message, isError = false) {
        const messageContainer = document.getElementById('messageContainer');
        if (messageContainer) {
            messageContainer.textContent = message;
            messageContainer.style.color = isError ? 'red' : 'green';
        }
    }

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
        if (response.ok) {
            displayMessage(result.message);
            window.location.href = '/';
        } else {
            displayMessage(result.error, true);
        }
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
        if (response.ok) {
            displayMessage(result.message);
            window.location.href = '/';
        } else {
            displayMessage(result.error, true);
        }
    });

    document.getElementById('placeOrderButton')?.addEventListener('click', async () => {
        const username = prompt('Enter your username to place the order');
        const response = await fetch('/place_order', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username})
        });

        const result = await response.json();
        if (response.ok) {
            displayMessage(`Order placed with ID: ${result.order_id}`);
        } else {
            displayMessage(result.error, true);
        }
    });

    document.getElementById('addProductForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const productName = document.getElementById('productName').value;
        const productPrice = document.getElementById('productPrice').value;
        const productDescription = document.getElementById('productDescription').value;

        const response = await fetch('/add_product', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name: productName, price: productPrice, description: productDescription})
        });

        const result = await response.json();
        if (response.ok) {
            displayMessage(result.message);
        } else {
            displayMessage(result.error, true);
        }
    });

    document.getElementById('editProductForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const productId = document.getElementById('editProductId').value;
        const productName = document.getElementById('editProductName').value;
        const productPrice = document.getElementById('editProductPrice').value;
        const productDescription = document.getElementById('editProductDescription').value;

        const response = await fetch('/edit_product', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({product_id: productId, name: productName, price: productPrice, description: productDescription})
        });

        const result = await response.json();
        if (response.ok) {
            displayMessage(result.message);
        } else {
            displayMessage(result.error, true);
        }
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
});

document.addEventListener('DOMContentLoaded', function () {
    const addProductButton = document.getElementById('showAddProductForm');
    const removeProductButton = document.getElementById('showRemoveProductForm');
    const editProductButton = document.getElementById('showEditProductForm');

    const addProductForm = document.getElementById('addProduct');
    const removeProductForm = document.getElementById('removeProduct');
    const editProductForm = document.getElementById('editProduct');

    function showForm(formId) {
        // Hide all forms
        addProductForm.classList.add('form-hidden');
        removeProductForm.classList.add('form-hidden');
        editProductForm.classList.add('form-hidden');

        // Show the selected form
        const form = document.getElementById(formId);
        if (form) {
            form.classList.remove('form-hidden');
        }
    }

    addProductButton.addEventListener('click', function () {
        showForm('addProduct');
    });

    removeProductButton.addEventListener('click', function () {
        showForm('removeProduct');
    });

    editProductButton.addEventListener('click', function () {
        showForm('editProduct');
    });

    // Show the default form (e.g., Add Product) on page load
    showForm('addProduct');
});

