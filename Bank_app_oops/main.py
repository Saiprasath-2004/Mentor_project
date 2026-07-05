class User:

    def __init__(self,name,balance):
        self.name = name
        self.__balance = balance

    def get_balance(self):
        return self.__balance
    
    def deduct_balance(self,amount):
        self.__balance -= amount

    def add_balance(self,amount):
        self.__balance += amount

    def display_balance(self):
        print(f"Current Balance: {self.__balance}")


class Bank:

    def withdraw(self,user,amount):

        if amount <= 0:
            print("Invalid amount")
            return False

        if amount <= user.get_balance():
            user.deduct_balance(amount)
            print(f"Rs {amount} withdrawn successfully")
            return True

        print("Insufficient Balance")
        return False


    def deposit(self,user,amount):

        if amount <= 0:
            print("Invalid amount")
            return False

        user.add_balance(amount)
        print(f"Rs {amount} deposited successfully")
        return True
    
user1 = User("Sai",5000)
bank = Bank()

user1.display_balance()
bank.withdraw(user1,1000)
bank.deposit(user1,2000)

user1.display_balance()