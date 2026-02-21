import pandas as pd
import os
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, ForeignKey, MetaData, Table
from sqlalchemy.orm import sessionmaker
from backend.config import settings

class DatasetLoader:
    def __init__(self, data_path: str = "backend/data"):
        self.data_path = data_path
        self.engine = create_engine(settings.DATABASE_URL)
        self.metadata = MetaData()

    def define_schema(self):
        # 1. Customers
        Table('customers', self.metadata,
            Column('customer_id', String, primary_key=True),
            Column('customer_unique_id', String),
            Column('customer_zip_code_prefix', Integer),
            Column('customer_city', String),
            Column('customer_state', String)
        )

        # 2. Geolocation
        Table('geolocation', self.metadata,
            Column('geolocation_zip_code_prefix', Integer),
            Column('geolocation_lat', Float),
            Column('geolocation_lng', Float),
            Column('geolocation_city', String),
            Column('geolocation_state', String)
        )

        # 3. Products
        Table('products', self.metadata,
            Column('product_id', String, primary_key=True),
            Column('product_category_name', String),
            Column('product_name_lenght', Float),
            Column('product_description_lenght', Float),
            Column('product_photos_qty', Float),
            Column('product_weight_g', Float),
            Column('product_length_cm', Float),
            Column('product_height_cm', Float),
            Column('product_width_cm', Float)
        )

        # 4. Sellers
        Table('sellers', self.metadata,
            Column('seller_id', String, primary_key=True),
            Column('seller_zip_code_prefix', Integer),
            Column('seller_city', String),
            Column('seller_state', String)
        )

        # 5. Orders
        Table('orders', self.metadata,
            Column('order_id', String, primary_key=True),
            Column('customer_id', String, ForeignKey('customers.customer_id')),
            Column('order_status', String),
            Column('order_purchase_timestamp', DateTime),
            Column('order_approved_at', DateTime),
            Column('order_delivered_carrier_date', DateTime),
            Column('order_delivered_customer_date', DateTime),
            Column('order_estimated_delivery_date', DateTime)
        )

        # 6. Order Items
        Table('order_items', self.metadata,
            Column('order_id', String, ForeignKey('orders.order_id')),
            Column('order_item_id', Integer),
            Column('product_id', String, ForeignKey('products.product_id')),
            Column('seller_id', String, ForeignKey('sellers.seller_id')),
            Column('shipping_limit_date', DateTime),
            Column('price', Float),
            Column('freight_value', Float)
        )

        # 7. Order Payments
        Table('order_payments', self.metadata,
            Column('order_id', String, ForeignKey('orders.order_id')),
            Column('payment_sequential', Integer),
            Column('payment_type', String),
            Column('payment_installments', Integer),
            Column('payment_value', Float)
        )

        # 8. Order Reviews
        Table('order_reviews', self.metadata,
            Column('review_id', String, primary_key=True),
            Column('order_id', String, ForeignKey('orders.order_id')),
            Column('review_score', Integer),
            Column('review_comment_title', String),
            Column('review_comment_message', String),
            Column('review_creation_date', DateTime),
            Column('review_answer_timestamp', DateTime)
        )

        # 9. Category Translation
        Table('category_translation', self.metadata,
            Column('product_category_name', String, primary_key=True),
            Column('product_category_name_english', String)
        )

    def load_data(self):
        print("Cleaning existing tables for a fresh load...")
        # Drop all tables in reverse order of foreign keys to avoid conflicts
        self.metadata.drop_all(self.engine)
        
        print("Creating tables...")
        self.metadata.create_all(self.engine)

        files_to_tables = {
            "olist_customers_dataset.csv": "customers",
            "olist_geolocation_dataset.csv": "geolocation",
            "olist_products_dataset.csv": "products",
            "olist_sellers_dataset.csv": "sellers",
            "olist_orders_dataset.csv": "orders",
            "olist_order_items_dataset.csv": "order_items",
            "olist_order_payments_dataset.csv": "order_payments",
            "olist_order_reviews_dataset.csv": "order_reviews",
            "product_category_name_translation.csv": "category_translation"
        }

        # Identify Primary Key columns for each table to drop duplicates
        pk_columns = {
            "customers": "customer_id",
            "products": "product_id",
            "sellers": "seller_id",
            "orders": "order_id",
            "order_reviews": "review_id",
            "category_translation": "product_category_name"
        }

        for file_name, table_name in files_to_tables.items():
            file_path = os.path.join(self.data_path, file_name)
            if not os.path.exists(file_path):
                print(f"Warning: File {file_path} not found. Skipping.")
                continue

            print(f"Loading {file_name} into {table_name}...")
            df = pd.read_csv(file_path)
            
            # Handle date columns
            date_cols = [col for col in df.columns if 'date' in col or 'timestamp' in col or 'approved_at' in col]
            for col in date_cols:
                df[col] = pd.to_datetime(df[col])

            # Drop duplicates if PK is defined
            if table_name in pk_columns:
                df = df.drop_duplicates(subset=[pk_columns[table_name]])

            df.to_sql(table_name, self.engine, if_exists='append', index=False)
            print(f"Successfully loaded {table_name}.")

if __name__ == "__main__":
    loader = DatasetLoader()
    loader.define_schema()
    loader.load_data()
