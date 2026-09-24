from app.security import create_access_token,hash_password,read_user_id_from_token,verify_password

def test_hashes_differ():
    assert hash_password("reads4ever")!=hash_password("reads4ever")

def test_hash_verifies_only_correct_password():
    hashed=hash_password("reads4ever")
    assert verify_password("reads4ever",hashed)
    assert not verify_password("wrongpass1",hashed)

def test_token_round_trip():
    token=create_access_token(7)
    assert read_user_id_from_token(token)==7

def test_tampered_token_is_rejected():
    token=create_access_token(7)+"x"
    assert read_user_id_from_token(token) is None
