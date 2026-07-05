from backend.app.services.password_service import PasswordService


def test_hash_password_does_not_return_plaintext():
    password_service = PasswordService()
    password = "CorrectHorseBatteryStaple123!"
    password_hash = password_service.hash_password(password)
    assert password != password_hash

def test_verify_password_returns_true_for_correct_password():
    password_service = PasswordService()
    password = "CorrectHorseBatteryStaple123!"
    password_hash = password_service.hash_password(password)
    assert password_service.verify_password(password, password_hash)

def test_verify_password_returns_false_for_incorrect_password():
    password_service = PasswordService()
    correct_password = "CorrectHorseBatteryStaple123!"
    incorrect_password = "WrongPassword123!"
    password_hash = password_service.hash_password(correct_password)
    assert not password_service.verify_password(incorrect_password, password_hash)
