class ProductCreateSchema:

    def __init__(self, name: str, price, stock):
        self.name = self.validate_name(name)
        self.price = self.validate_price(price)
        self.stock = self.validate_stock(stock)

    def validate_name(self, value):
        if not value or not value.strip():
            raise ValueError("El nombre es obligatorio")
        return value.strip()

    def validate_price(self, value):
        try:
            price = float(value)
            if price < 0:
                raise ValueError
            return price
        except:
            raise ValueError("Precio inválido")

    def validate_stock(self, value):
        try:
            stock = int(value)
            if stock < 0:
                raise ValueError
            return stock
        except:
            raise ValueError("Stock inválido")