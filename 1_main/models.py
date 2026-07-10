class Transaction():
    def __init__(self, transaction_id, amount, category, transaction_type):
        self.__transaction_id = transaction_id
        self.__amount = 0
        self.__category = ""
        self.__transaction_type = ""
        self.amount = amount
        self.category = category
        self.transaction_type =  transaction_type

    @property
    def id(self):
        return self.__transaction_id
    
    @property
    def amount(self):
        return self.__amount
    
    @property
    def category(self):
        return self.__category
    
    @property
    def type(self):
        return self.__transaction_type
    
    @amount.setter
    def amount(self, new_amount):
        if new_amount > 0 and isinstance(new_amount, int):
            self.__amount = new_amount

    @category.setter
    def category(self, new_category):
        if len(new_category.strip()) > 0:
            self.__category = new_category

    @type.setter
    def type(self, new_type):
        if len(new_type.strip()) > 0:
            self.__transaction_type = new_type