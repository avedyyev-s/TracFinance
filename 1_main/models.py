class Transaction:
    def __init__(self, transaction_id, user_id, wallet_id, category_id, transaction_type, amount, description):
        self.__transaction_id = transaction_id
        self.__user_id = user_id
        self.__wallet_id = wallet_id
        self.__category_id = 0
        self.__transaction_type = ""
        self.__amount = 0
        self.__description = ""
        self.transaction_type = transaction_type
        self.amount = amount
        self.category_id = category_id
        self.description =  description

    @property
    def transaction_id(self):
        return self.__transaction_id
    @property
    def user_id(self):
        return self.__user_id
    @property
    def wallet_id(self):
        return self.__wallet_id
    @property
    def category_id(self):
        return self.__category_id
    @property
    def transaction_type(self):
        return self.__transaction_type
    @property
    def amount(self):
        return self.__amount
    @property
    def description(self):
        return self.__description

    @category_id.setter
    def category_id(self, new_category_id):
        if new_category_id > 0 and isinstance(new_category_id, int):
            self.__category_id = new_category_id
    @transaction_type.setter
    def transaction_type(self, new_transaction_type):
        if new_transaction_type == "income" or new_transaction_type == "expense":
            self.__transaction_type = new_transaction_type
    @amount.setter
    def amount(self, new_amount):
        if new_amount > 0 and isinstance(new_amount, (int, float)):
            self.__amount = new_amount
    @description.setter
    def description(self, new_description):
        if len(new_description.strip()) > 0:
            self.__description = new_description


class Wallet:
    def __init__(self, wallet_id, user_id, name, balance):
        self.__wallet_id = wallet_id
        self.__user_id = user_id
        self.__name = ""
        self.__balance = 0
        self.name = name
        self.balance = balance

    @property
    def wallet_id(self):
        return self.__wallet_id
    @property
    def user_id(self):
        return self.__user_id
    @property
    def name(self):
        return self.__name
    @property
    def balance(self):
        return self.__balance

    @name.setter
    def name(self, new_name):
        if len(new_name.strip()) > 0:
            self.__name = new_name
    @balance.setter
    def balance(self, new_balance):
        if isinstance(new_balance, (int, float)):
            self.__balance = new_balance

class Category():
    def __init__(self, category_id, user_id, name, category_type, icon="🏷️"):
        self.__category_id = category_id
        self.__user_id = user_id
        self.__name = ""
        self.__category_type = ""
        self.__icon = ""
        self.name = name
        self.category_type = category_type
        self.icon = icon

    @property
    def category_id(self):
        return self.__category_id
    @property
    def user_id(self):
        return self.__user_id
    @property
    def name(self):
        return self.__name
    @property
    def category_type(self):
        return self.__category_type
    @property
    def icon(self):
        return self.__icon

    @name.setter
    def name(self, new_name):
        if len(new_name.strip()) > 0:
            self.__name = new_name
    @category_type.setter
    def category_type(self, new_category_type):
        if new_category_type == "income" or new_category_type == "expense":
            self.__category_type = new_category_type
    @icon.setter
    def icon(self, new_icon):
        if len(new_icon.strip()) > 0:
            self.__icon = new_icon
