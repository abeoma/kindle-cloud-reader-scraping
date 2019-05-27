from typing import Dict, Any

from models_generated import Product


def convert_to_dict(product: Product) -> Dict[str, Any]:
    return {
        key: value for key, value in product.__dict__.items() if not key.startswith("_")
    }
