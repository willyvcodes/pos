# This script is used to seed the products into the database, edit the mock_products.json file to add or remove products

import asyncio
import httpx
import logging
import json
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def seed_products():
    API_URL = "http://localhost:8000/api/products/"

    script_dir = Path(__file__).parent
    json_path = script_dir / "mock_products.json"

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            products = data["products"]
    except FileNotFoundError:
        logger.error(f"Could not find mock_products.json at {json_path}")
        return
    except json.JSONDecodeError:
        logger.error("Invalid JSON format in mock_products.json")
        return

    async with httpx.AsyncClient() as client:
        for product in products:
            try:
                product_data = {
                    "name": product["name"],
                    "type": product["type"],
                    "price": product["price"],
                    "description": product["description"],
                    "thumbnail": product["thumbnail"],
                    "upc": product["upc"],
                }
                response = await client.post(API_URL, json=product_data)

                if response.status_code == 201:
                    logger.info(f"Successfully added product: {product['name']}")
                else:
                    logger.error(
                        f"Failed to add product {product['name']}: {response.text}"
                    )

            except Exception as e:
                logger.error(f"Error adding product {product['name']}: {str(e)}")

    logger.info("Product seeding completed!")


if __name__ == "__main__":
    asyncio.run(seed_products())
