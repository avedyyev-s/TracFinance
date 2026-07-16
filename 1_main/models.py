class Transaction:
    def __init__(self, transaction_id, user_id, amount, category, description):
        self.__transaction_id = transaction_id
        self.__user_id = user_id
        self.__amount = 0
        self.__category = ""
        self.__description = ""
        self.amount = amount
        self.category = category
        self.description =  description

    @property
    def transaction_id(self):
        return self.__transaction_id
    
    @property
    def user_id(self):
        return self.__user_id

    @property
    def amount(self):
        return self.__amount
    
    @property
    def category(self):
        return self.__category
    
    @property
    def description(self):
        return self.__description
    
    @amount.setter
    def amount(self, new_amount):
        if new_amount > 0 and isinstance(new_amount, int):
            self.__amount = new_amount

    @category.setter
    def category(self, new_category):
        if len(new_category.strip()) > 0:
            self.__category = new_category

    @description.setter
    def description(self, new_description):
        if len(new_description.strip()) > 0:
            self.__description = new_description