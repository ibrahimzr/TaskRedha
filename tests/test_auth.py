
def login_with_challenge(client,username,password):
    challenge=client.get("/auth/challenge").json()
    answer=",".join(str(n) for n in sorted(challenge["numbers"]))
    return client.post(
        "/auth/login",
        params={"challenge_token":challenge["challenge_token"],"challenge_answer":answer},
        data={"username":username,"password":password},
    )

SIGNUP={"username":"amina","email":"amina@example.com","password":"reads4ever"}

def test_signup_returns_customer_without_password(client):
    response=client.post("/auth/register",json=SIGNUP)
    assert response.status_code==201
    assert response.json()["role"]=="customer"
    assert "hashed_password" not in response.json()
    assert "password" not in response.json()

def test_signup_cannot_make_admin(client):
    response=client.post("/auth/register",json={**SIGNUP,"role":"admin"})
    assert response.json()["role"]=="customer"

def test_duplicate_username_is_rejected(client):
    client.post("/auth/register",json=SIGNUP)
    response=client.post("/auth/register",json={**SIGNUP,"email":"other@example.com"})
    assert response.status_code==409

def test_login_returns_token(client):
    client.post("/auth/register",json=SIGNUP)
    response=login_with_challenge(client,"amina","reads4ever")
    assert response.status_code==200
    assert response.json()["token_type"]=="bearer"

def test_wrong_password_and_unknown_user_look_same(client):
    client.post("/auth/register",json=SIGNUP)
    wrong=login_with_challenge(client,"amina","wrongpass1")
    missing=login_with_challenge(client,"ghost","wrongpass1")
    assert wrong.status_code==missing.status_code==401
    assert wrong.json()==missing.json()

def test_me_needs_token(client):
    assert client.get("/auth/me").status_code==401

def test_me_reports_logged_in_user(client,customer):
    response=client.get("/auth/me",headers=customer)
    assert response.status_code==200
    assert response.json()["username"]=="amina"
