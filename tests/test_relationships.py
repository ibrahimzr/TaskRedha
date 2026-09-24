def test_new_author_has_no_books_or_profile(client,staff):
    response=client.post("/authors",json={"name":"Frank Herbert"},headers=staff)
    assert response.status_code==201
    assert response.json()["books"]==[]
    assert response.json()["profile"] is None

def test_book_shows_nested_author_and_genres(client,staff):
    author=client.post("/authors",json={"name":"Frank Herbert"},headers=staff).json()
    fiction=client.post("/genres",json={"name":"fiction"},headers=staff).json()
    classic=client.post("/genres",json={"name":"classic"},headers=staff).json()
    book=client.post(
        "/books",
        json={"title":"Dune","author_id":author["id"],"genre_ids":[fiction["id"],classic["id"]],"price":12.5,"stock":3},
        headers=staff,
    ).json()
    assert book["author"]=={"id":author["id"],"name":"Frank Herbert"}
    assert sorted(g["name"] for g in book["genres"])==["classic","fiction"]

def test_author_list_counts_books_and_keeps_zero(client,staff):
    herbert=client.post("/authors",json={"name":"Frank Herbert"},headers=staff).json()
    client.post("/authors",json={"name":"Jane Austen"},headers=staff)
    client.post("/books",json={"title":"Dune","author_id":herbert["id"],"price":12.5},headers=staff)
    counts={a["name"]:a["book_count"] for a in client.get("/authors").json()}
    assert counts=={"Frank Herbert":1,"Jane Austen":0}
    assert [a["name"] for a in client.get("/authors?has_books=true").json()]==["Frank Herbert"]

def test_author_has_one_replaceable_profile(client,staff):
    author=client.post("/authors",json={"name":"Frank Herbert"},headers=staff).json()
    client.put(f"/authors/{author['id']}/profile",json={"bio":"First draft."},headers=staff)
    response=client.put(f"/authors/{author['id']}/profile",json={"bio":"Wrote Dune."},headers=staff)
    assert response.json()["profile"]=={"bio":"Wrote Dune.","website":None}

def test_filter_by_genre_uses_junction_table(client,staff):
    author=client.post("/authors",json={"name":"Walt Whitman"},headers=staff).json()
    poetry=client.post("/genres",json={"name":"poetry"},headers=staff).json()
    client.post("/books",json={"title":"Leaves of Grass","author_id":author["id"],"genre_ids":[poetry["id"]],"price":9.0},headers=staff)
    assert [b["title"] for b in client.get("/books?genre=poetry").json()]==["Leaves of Grass"]
    assert client.get("/books?genre=mystery").json()==[]
