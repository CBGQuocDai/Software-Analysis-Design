from infrastructure.repositories.customer_repo import CustomerRepository

class LoginCustomer:

    def execute(self, email, password):
        repo = CustomerRepository()
        user = repo.find_by_email(email)

        if user and user.password == password:
            return user
        return None
