from django import template


register = template.Library()





@register.filter(name="price_format")
def Price_Format(value):
    price = float(value)
    price=str(price).split('.')
    if price[1] == '0':
        return price[0]
    else:
        return float(value)
