from infrastructure.repositories.customer_repo import CustomerRepository

class RegisterCustomer:

    def execute(self, name, email, password):
        repo = CustomerRepository()
        return repo.create(name, email, password)
