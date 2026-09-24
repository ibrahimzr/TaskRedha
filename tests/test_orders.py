def test_order_reduces_stock(client,customer,a_book):
    response=client.post("/orders",json={"book_id":a_book["id"],"quantity":2},headers=customer)
    assert response.status_code==201
    assert response.json()["total_price"]==25.0
    assert client.get(f"/books/{a_book['id']}").json()["stock"]==1

def test_too_many_books_is_refused(client,customer,a_book):
    response=client.post("/orders",json={"book_id":a_book["id"],"quantity":5},headers=customer)
    assert response.status_code==409
    assert client.get(f"/books/{a_book['id']}").json()["stock"]==3

def test_order_owner_comes_from_token(client,customer,a_book):
    response=client.post("/orders",json={"book_id":a_book["id"],"quantity":1,"user_id":999},headers=customer)
    assert response.status_code==201
    assert response.json()["user_id"]!=999

def test_missing_book_is_404(client,customer):
    assert client.post("/orders",json={"book_id":999},headers=customer).status_code==404

def test_customer_sees_only_own_orders(client,customer,staff,a_book):
    client.post("/orders",json={"book_id":a_book["id"]},headers=customer)
    client.post("/orders",json={"book_id":a_book["id"]},headers=staff)
    assert len(client.get("/orders",headers=customer).json())==1
    assert len(client.get("/orders",headers=staff).json())==2

def test_someone_elses_order_looks_missing(client,customer,staff,a_book):
    order=client.post("/orders",json={"book_id":a_book["id"]},headers=staff).json()
    assert client.get(f"/orders/{order['id']}",headers=customer).status_code==404

def test_only_staff_can_change_status(client,customer,staff,a_book):
    order=client.post("/orders",json={"book_id":a_book["id"]},headers=customer).json()
    assert client.patch(f"/orders/{order['id']}/status",json={"status":"shipped"},headers=customer).status_code==403
    assert client.patch(f"/orders/{order['id']}/status",json={"status":"shipped"},headers=staff).status_code==200

def test_cancel_restores_stock(client,customer,staff,a_book):
    order=client.post("/orders",json={"book_id":a_book["id"],"quantity":2},headers=customer).json()
    client.patch(f"/orders/{order['id']}/status",json={"status":"cancelled"},headers=staff)
    assert client.get(f"/books/{a_book['id']}").json()["stock"]==3
