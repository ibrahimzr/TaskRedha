def make_book(client,staff,title="Dune"):
    author=client.post("/authors",json={"name":"Frank Herbert"},headers=staff).json()
    genre=client.post("/genres",json={"name":"fiction"},headers=staff).json()
    return {
        "title":title,
        "author_id":author["id"],
        "genre_ids":[genre["id"]],
        "price":12.5,
        "stock":3,
    }

def test_anyone_can_list_books_and_it_starts_empty(client):
    assert client.get("/books").json()==[]

def test_staff_can_add_book(client,staff):
    response=client.post("/books",json=make_book(client,staff),headers=staff)
    assert response.status_code==201
    assert response.json()["id"] is not None

def test_new_book_appears_in_list(client,staff):
    client.post("/books",json=make_book(client,staff),headers=staff)
    assert [b["title"] for b in client.get("/books").json()]==["Dune"]

def test_visitor_cannot_add_book(client,staff):
    payload=make_book(client,staff)
    assert client.post("/books",json=payload).status_code==401

def test_customer_cannot_add_book(client,staff,customer):
    payload=make_book(client,staff)
    assert client.post("/books",json=payload,headers=customer).status_code==403

def test_blank_title_is_refused(client,staff):
    payload=make_book(client,staff)
    payload["title"]="   "
    assert client.post("/books",json=payload,headers=staff).status_code==422

def test_missing_author_is_404(client,staff):
    response=client.post("/books",json={"title":"Ghost","author_id":999,"price":1.0},headers=staff)
    assert response.status_code==404

def test_staff_can_change_price(client,staff,a_book):
    response=client.patch(f"/books/{a_book['id']}",json={"price":11.0},headers=staff)
    assert response.status_code==200
    assert response.json()["price"]==11.0
    assert response.json()["title"]=="Dune"

def test_only_admin_can_delete_book(client,staff,admin,a_book):
    assert client.delete(f"/books/{a_book['id']}",headers=staff).status_code==403
    assert client.delete(f"/books/{a_book['id']}",headers=admin).status_code==204
    assert client.get(f"/books/{a_book['id']}").status_code==404
