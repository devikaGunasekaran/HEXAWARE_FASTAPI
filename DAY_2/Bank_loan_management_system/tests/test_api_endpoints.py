from uuid import uuid4


def _unique_email(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:8]}@example.com"


def _create_user(client, role: str, name: str = "User") -> dict:
    payload = {
        "name": name,
        "email": _unique_email(role),
        "role": role,
        "password": "pass123",
    }
    resp = client.post("/users", json=payload)
    assert resp.status_code == 200, resp.text
    return resp.json()


def _create_product(client) -> dict:
    payload = {
        "product_name": "Personal Loan",
        "interest_rate": 10.5,
        "max_amount": 500000,
        "tenure_months": 24,
        "description": "General purpose loan",
    }
    resp = client.post("/loan-products", json=payload)
    assert resp.status_code == 200, resp.text
    return resp.json()


def _create_application(client, user_id: int, product_id: int, requested_amount: float = 200000) -> dict:
    resp = client.post(
        "/loan-applications",
        json={
            "user_id": user_id,
            "product_id": product_id,
            "requested_amount": requested_amount,
        },
    )
    assert resp.status_code == 200, resp.text
    return resp.json()


def test_users_post_url(client):
    payload = {
        "name": "Alice",
        "email": _unique_email("alice"),
        "role": "customer",
        "password": "secret123",
    }
    resp = client.post("/users", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] > 0
    assert body["email"] == payload["email"]


def test_users_get_by_id_url(client):
    user = _create_user(client, "customer", "Bob")
    resp = client.get(f"/users/{user['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == user["id"]


def test_users_list_url(client):
    _create_user(client, "customer")
    resp = client.get("/users?skip=0&limit=10")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


def test_users_update_url(client):
    user = _create_user(client, "customer", "Charlie")
    resp = client.put(f"/users/{user['id']}", json={"name": "Charlie Updated"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Charlie Updated"


def test_users_delete_url(client):
    user = _create_user(client, "customer", "Delete Me")
    del_resp = client.delete(f"/users/{user['id']}")
    assert del_resp.status_code == 200
    get_resp = client.get(f"/users/{user['id']}")
    assert get_resp.status_code == 404


def test_loan_products_post_url(client):
    resp = client.post(
        "/loan-products",
        json={
            "product_name": "Home Loan",
            "interest_rate": 8.2,
            "max_amount": 9000000,
            "tenure_months": 240,
            "description": "Home purchase",
        },
    )
    assert resp.status_code == 200
    assert resp.json()["id"] > 0


def test_loan_products_get_by_id_url(client):
    product = _create_product(client)
    resp = client.get(f"/loan-products/{product['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == product["id"]


def test_loan_products_list_url(client):
    _create_product(client)
    resp = client.get("/loan-products?skip=0&limit=10")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


def test_loan_products_update_url(client):
    product = _create_product(client)
    resp = client.put(f"/loan-products/{product['id']}", json={"tenure_months": 36})
    assert resp.status_code == 200
    assert resp.json()["tenure_months"] == 36


def test_loan_products_delete_url(client):
    product = _create_product(client)
    del_resp = client.delete(f"/loan-products/{product['id']}")
    assert del_resp.status_code == 200
    get_resp = client.get(f"/loan-products/{product['id']}")
    assert get_resp.status_code == 404


def test_loan_applications_post_url(client):
    customer = _create_user(client, "customer")
    product = _create_product(client)
    resp = client.post(
        "/loan-applications",
        json={"user_id": customer["id"], "product_id": product["id"], "requested_amount": 150000},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "pending"


def test_loan_applications_get_by_id_url(client):
    customer = _create_user(client, "customer")
    product = _create_product(client)
    app_obj = _create_application(client, customer["id"], product["id"])
    resp = client.get(f"/loan-applications/{app_obj['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == app_obj["id"]


def test_loan_applications_list_url(client):
    customer = _create_user(client, "customer")
    product = _create_product(client)
    _create_application(client, customer["id"], product["id"])
    resp = client.get("/loan-applications?skip=0&limit=10")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert len(resp.json()) >= 1


def test_loan_applications_update_status_url(client):
    customer = _create_user(client, "customer")
    officer = _create_user(client, "loan_officer")
    product = _create_product(client)
    app_obj = _create_application(client, customer["id"], product["id"])
    resp = client.put(
        f"/loan-applications/{app_obj['id']}/status",
        json={"status": "approved", "processed_by": officer["id"], "approved_amount": 120000},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "approved"
    assert body["processed_by"] == officer["id"]


def test_repayments_post_url(client):
    customer = _create_user(client, "customer")
    officer = _create_user(client, "loan_officer")
    product = _create_product(client)
    app_obj = _create_application(client, customer["id"], product["id"])
    approve_resp = client.put(
        f"/loan-applications/{app_obj['id']}/status",
        json={"status": "approved", "processed_by": officer["id"], "approved_amount": 100000},
    )
    assert approve_resp.status_code == 200

    repay_resp = client.post("/repayments", json={"loan_application_id": app_obj["id"], "amount_paid": 25000})
    assert repay_resp.status_code == 200
    assert repay_resp.json()["loan_application_id"] == app_obj["id"]


def test_loan_application_repayments_get_url(client):
    customer = _create_user(client, "customer")
    officer = _create_user(client, "loan_officer")
    product = _create_product(client)
    app_obj = _create_application(client, customer["id"], product["id"])
    approve_resp = client.put(
        f"/loan-applications/{app_obj['id']}/status",
        json={"status": "approved", "processed_by": officer["id"], "approved_amount": 100000},
    )
    assert approve_resp.status_code == 200

    add_resp = client.post("/repayments", json={"loan_application_id": app_obj["id"], "amount_paid": 10000})
    assert add_resp.status_code == 200

    list_resp = client.get(f"/loan-applications/{app_obj['id']}/repayments")
    assert list_resp.status_code == 200
    rows = list_resp.json()
    assert isinstance(rows, list)
    assert len(rows) == 1
    assert rows[0]["loan_application_id"] == app_obj["id"]
