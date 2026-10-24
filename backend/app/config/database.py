import json
import os
import urllib.parse
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from .settings import settings
from ..utils.logger import logger

def sanitize_mongodb_uri(uri: str) -> str:
    """
    Ensures password in MongoDB URI is escaped according to RFC 3986
    even if it contains special characters like '@', ':', '#', '%', etc.
    """
    if "://" not in uri or "@" not in uri:
        return uri
    prefix, rest = uri.split("://", 1)
    last_at_idx = rest.rfind("@")
    if last_at_idx == -1:
        return uri
    creds = rest[:last_at_idx]
    hosts = rest[last_at_idx + 1:]
    if ":" in creds:
        username, password = creds.split(":", 1)
        decoded_password = urllib.parse.unquote_plus(password)
        encoded_password = urllib.parse.quote_plus(decoded_password)
        return f"{prefix}://{username}:{encoded_password}@{hosts}"
    return uri

class DatabaseManager:
    """
    Unified Data Layer supporting MongoDB Atlas with transparent high-performance
    in-memory and JSON storage fallback.
    """
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.data: Dict[str, List[Dict[str, Any]]] = {
            "users": [],
            "accounts": [],
            "transactions": [],
            "cards": [],
            "loans": [],
            "bills": [],
            "disputes": [],
            "offers": [],
            "approvals": [],
            "audit_logs": []
        }
        self.is_connected = False
        self.mongo_client = None
        self.mongo_db = None
        self.connection_status = "uninitialized"
        self.connection_error = None

        # 1. Load seed records into local store
        self._load_seed_data()

        # 2. Attempt MongoDB Atlas connection
        self._init_mongodb()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = DatabaseManager()
            return cls._instance

    def _init_mongodb(self):
        uri = settings.MONGODB_URI
        db_name = settings.MONGODB_DB_NAME

        if not uri:
            self.connection_status = "no_uri_configured"
            logger.info("[DatabaseManager] No MONGODB_URI configured. Running in memory mode.")
            return

        if "<db_password>" in uri:
            self.connection_status = "placeholder_password"
            masked_uri = uri.split("@")[-1] if "@" in uri else uri
            self.connection_error = "Placeholder <db_password> detected in MONGODB_URI. Replace with your MongoDB Atlas password in backend/.env to persist directly to cloud."
            logger.warning(f"[DatabaseManager] {self.connection_error} (Cluster: {masked_uri})")
            return

        try:
            from pymongo import MongoClient
            sanitized_uri = sanitize_mongodb_uri(uri)
            logger.info(f"[DatabaseManager] Connecting to MongoDB Atlas cluster...")
            client = MongoClient(sanitized_uri, serverSelectionTimeoutMS=4000)
            client.admin.command("ping")
            self.mongo_client = client
            self.mongo_db = client[db_name]
            self.is_connected = True
            self.connection_status = "connected"
            logger.info(f"[DatabaseManager] Successfully CONNECTED to MongoDB Atlas database: '{db_name}'")

            # Seed initial collections into MongoDB Atlas if currently empty
            self._sync_seed_to_mongodb()
        except Exception as e:
            err_str = str(e)
            self.is_connected = False
            self.connection_status = "connection_failed"
            if "bad auth" in err_str.lower() or "authentication failed" in err_str.lower():
                self.connection_error = "Atlas authentication failed. Please ensure the password in backend/.env matches your Atlas Database User (Security -> Database Access -> Edit Password)."
            else:
                self.connection_error = err_str
            logger.warning(f"[DatabaseManager] Could not connect to MongoDB Atlas ({self.connection_error}). Operating in memory fallback mode.")

    def _sync_seed_to_mongodb(self):
        """
        Populates MongoDB Atlas collections from local seed data if they are empty.
        """
        if not self.is_connected or self.mongo_db is None:
            return

        try:
            for coll_name, records in self.data.items():
                coll = self.mongo_db[coll_name]
                count = coll.count_documents({})
                if count == 0 and records:
                    to_insert = [dict(r) for r in records]
                    coll.insert_many(to_insert)
                    logger.info(f"[DatabaseManager] Seeded {len(records)} records into MongoDB Atlas collection: '{coll_name}'")
        except Exception as e:
            logger.error(f"[DatabaseManager] Failed to sync seed data to MongoDB Atlas: {e}")

    def _load_seed_data(self):
        seed_dir = settings.SEED_DIR
        try:
            # Users
            users_file = seed_dir / "users.json"
            if users_file.exists():
                with open(users_file, "r", encoding="utf-8") as f:
                    self.data["users"] = json.load(f)

            # Accounts
            accounts_file = seed_dir / "accounts.json"
            if accounts_file.exists():
                with open(accounts_file, "r", encoding="utf-8") as f:
                    self.data["accounts"] = json.load(f)

            # Transactions
            txns_file = seed_dir / "transactions.json"
            if txns_file.exists():
                with open(txns_file, "r", encoding="utf-8") as f:
                    self.data["transactions"] = json.load(f)

            # Loans
            loans_file = seed_dir / "loans.json"
            if loans_file.exists():
                with open(loans_file, "r", encoding="utf-8") as f:
                    self.data["loans"] = json.load(f)

            # Default Cards
            self.data["cards"] = [
                {
                    "card_id": "CRD-9081",
                    "customer_id": "C1001",
                    "card_number": "**** **** **** 8821",
                    "card_type": "DEBIT",
                    "network": "VISA",
                    "card_holder": "AARAV SHARMA",
                    "expiry_date": "08/28",
                    "status": "ACTIVE",
                    "daily_limit": 50000.0,
                    "international_enabled": False,
                    "contactless_enabled": True
                },
                {
                    "card_id": "CRD-4412",
                    "customer_id": "C1001",
                    "card_number": "**** **** **** 3094",
                    "card_type": "CREDIT",
                    "network": "MASTERCARD",
                    "card_holder": "AARAV SHARMA",
                    "expiry_date": "11/29",
                    "status": "ACTIVE",
                    "credit_limit": 200000.0,
                    "available_limit": 190000.0,
                    "statement_due_date": "2026-11-05",
                    "minimum_due": 1000.0,
                    "total_due": 10000.0,
                    "billing_cycle": "15th of month"
                }
            ]

            # Default Scheduled Bills / Recurring payments (Matches Use Case 7)
            self.data["bills"] = [
                {
                    "bill_id": "BIL-881",
                    "customer_id": "C1001",
                    "biller_name": "BESCOM Electricity Board",
                    "category": "UTILITIES",
                    "amount": 2500.0,
                    "due_date": "2026-10-28",
                    "status": "UPCOMING",
                    "auto_pay": True
                },
                {
                    "bill_id": "BIL-882",
                    "customer_id": "C1001",
                    "biller_name": "Airtel Xstream Fiber",
                    "category": "TELECOM",
                    "amount": 1499.0,
                    "due_date": "2026-10-30",
                    "status": "UPCOMING",
                    "auto_pay": True
                },
                {
                    "bill_id": "BIL-883",
                    "customer_id": "C1001",
                    "biller_name": "Netflix Premium Subscription",
                    "category": "SUBSCRIPTION",
                    "amount": 649.0,
                    "due_date": "2026-10-29",
                    "status": "UPCOMING",
                    "auto_pay": True
                },
                {
                    "bill_id": "BIL-884",
                    "customer_id": "C1001",
                    "biller_name": "Credit Card Minimum Dues",
                    "category": "CREDIT_CARD",
                    "amount": 10000.0,
                    "due_date": "2026-11-05",
                    "status": "UPCOMING",
                    "auto_pay": False
                },
                {
                    "bill_id": "BIL-885",
                    "customer_id": "C1001",
                    "biller_name": "Home Loan EMI Auto-Debit",
                    "category": "LOAN_EMI",
                    "amount": 20000.0,
                    "due_date": "2026-11-05",
                    "status": "UPCOMING",
                    "auto_pay": True
                }
            ]

            # Default Personalized Offers (Matches Use Case 10)
            self.data["offers"] = [
                {
                    "offer_id": "OFF-PRE-01",
                    "customer_id": "C1001",
                    "offer_type": "PRE_APPROVED_LOAN",
                    "title": "Pre-Approved Personal Loan of ₹5,00,000",
                    "description": "Instant disbursement at preferential 9.99% p.a. interest rate with zero paperwork.",
                    "max_amount": 500000.0,
                    "interest_rate": 9.99,
                    "max_tenure_months": 48,
                    "valid_until": "2026-11-30",
                    "status": "AVAILABLE"
                },
                {
                    "offer_id": "OFF-CRD-02",
                    "customer_id": "C1001",
                    "offer_type": "CREDIT_LIMIT_INCREASE",
                    "title": "Complimentary Credit Limit Upgrade",
                    "description": "Upgrade your credit card limit from ₹2,00,000 to ₹3,50,000 at zero cost.",
                    "new_limit": 350000.0,
                    "valid_until": "2026-11-15",
                    "status": "AVAILABLE"
                }
            ]

            logger.info("Database loaded local seed records successfully.")
        except Exception as e:
            logger.error(f"Failed to load seed data: {e}")

    # Generic CRUD supporting real MongoDB Atlas + memory mirror
    def find_one(self, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if self.is_connected and self.mongo_db is not None:
            try:
                doc = self.mongo_db[collection].find_one(query, {"_id": 0})
                if doc:
                    return dict(doc)
            except Exception as e:
                logger.warning(f"[DatabaseManager] Mongo find_one error: {e}. Falling back to memory.")

        for item in self.data.get(collection, []):
            if all(item.get(k) == v for k, v in query.items()):
                return dict(item)
        return None

    def find(self, collection: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if self.is_connected and self.mongo_db is not None:
            try:
                cursor = self.mongo_db[collection].find(query or {}, {"_id": 0})
                return [dict(d) for d in cursor]
            except Exception as e:
                logger.warning(f"[DatabaseManager] Mongo find error: {e}. Falling back to memory.")

        items = self.data.get(collection, [])
        if not query:
            return [dict(i) for i in items]
        return [dict(i) for i in items if all(i.get(k) == v for k, v in query.items())]

    def insert_one(self, collection: str, document: Dict[str, Any]) -> Dict[str, Any]:
        doc = dict(document)
        if "created_at" not in doc:
            doc["created_at"] = datetime.now(timezone.utc).isoformat()

        if self.is_connected and self.mongo_db is not None:
            try:
                mongo_copy = dict(doc)
                self.mongo_db[collection].insert_one(mongo_copy)
                mongo_copy.pop("_id", None)
            except Exception as e:
                logger.warning(f"[DatabaseManager] Mongo insert error: {e}")

        if collection not in self.data:
            self.data[collection] = []
        self.data[collection].append(doc)
        return doc

    def update_one(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        success = False
        if self.is_connected and self.mongo_db is not None:
            try:
                res = self.mongo_db[collection].update_one(query, {"$set": update})
                success = res.modified_count > 0 or res.matched_count > 0
            except Exception as e:
                logger.warning(f"[DatabaseManager] Mongo update error: {e}")

        for idx, item in enumerate(self.data.get(collection, [])):
            if all(item.get(k) == v for k, v in query.items()):
                item.update(update)
                item["updated_at"] = datetime.now(timezone.utc).isoformat()
                return True
        return success

    def delete_one(self, collection: str, query: Dict[str, Any]) -> bool:
        if self.is_connected and self.mongo_db is not None:
            try:
                res = self.mongo_db[collection].delete_one(query)
                if res.deleted_count > 0:
                    pass
            except Exception as e:
                logger.warning(f"[DatabaseManager] Mongo delete_one error: {e}")

        items = self.data.get(collection, [])
        for idx, item in enumerate(items):
            if all(item.get(k) == v for k, v in query.items()):
                del items[idx]
                return True
        return False

    def delete_many(self, collection: str, query: Dict[str, Any]) -> int:
        count = 0
        if self.is_connected and self.mongo_db is not None:
            try:
                res = self.mongo_db[collection].delete_many(query)
                count = res.deleted_count
            except Exception as e:
                logger.warning(f"[DatabaseManager] Mongo delete_many error: {e}")

        items = self.data.get(collection, [])
        new_items = [item for item in items if not all(item.get(k) == v for k, v in query.items())]
        deleted = len(items) - len(new_items)
        self.data[collection] = new_items
        return max(count, deleted)

    def get_status_info(self) -> Dict[str, Any]:
        """
        Returns connection metadata for API health & UI status badge.
        """
        uri = settings.MONGODB_URI or ""
        masked_uri = ""
        if "@" in uri:
            parts = uri.split("@")
            prefix = parts[0].split("://")[0] + "://"
            user = parts[0].split("://")[1].split(":")[0] if ":" in parts[0] else "user"
            masked_uri = f"{prefix}{user}:****@{parts[1]}"
        elif uri:
            masked_uri = uri[:15] + "****"

        return {
            "is_connected": self.is_connected,
            "database_type": "MongoDB Atlas" if self.is_connected else "In-Memory Seed Mirror",
            "cluster_uri": masked_uri,
            "database_name": settings.MONGODB_DB_NAME,
            "status": self.connection_status,
            "error_detail": self.connection_error
        }

db = DatabaseManager.get_instance()
