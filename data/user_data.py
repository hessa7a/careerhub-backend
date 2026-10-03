from models.user import UserModel

def create_test_users():
    user1 = UserModel(name="Arjun", email="arjun@devmail.in", phone="11111111", role="applicant")
    user1.set_password("123")

    user2 = UserModel(name="Emma Johnson", email="emma.johnson@email.com", phone="22222222", role="applicant")
    user2.set_password("123")

    user3 = UserModel(name="Fatima Ali", email="fatima.ali@mail.ae", phone="33333333", role="applicant")
    user3.set_password("123")

    user4 = UserModel(name="Lucas Silva", email="lucas.silva@correo.br", phone="44444444", role="applicant")
    user4.set_password("123")

    user5 = UserModel(name="Elena Popov", email="elena.popov@mail.ru", phone="55555555", role="applicant")
    user5.set_password("123")

    return [user1, user2, user3, user4, user5]

user_list = create_test_users()