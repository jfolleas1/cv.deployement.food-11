## Model configuration

IM_RESIZE_DIMENSION = (229,229)

MODEL_OUTPUT_CLASSES = [
    'bread',
    'dairy_product',
    'dessert',
    'egg',
    'fried_food',
    'meat', 
    'noodles_pasta',
    'rice',
    'seafood',
    'soup',
    'vegetable or fruit'
]

## Application configuration

ALLOWED_EXTENTIONS = ["JPEG", "JPG", "PNG"]

LOCAL_SAVE_IM_PATH = './static'

GS_SAVE_IM_PATH = None

API_CALL_ONLY = False