# scripts/smoke_test.py
from app import db
db.create_listing("TEST1","Bread",5,"2030-01-01","P001","bakery","Mumbai","bakery","breakfast")
assert db.get_listing("TEST1") is not None
db.update_listing("TEST1", quantity=7)
assert db.get_listing("TEST1")["quantity"] == 7
db.delete_listing("TEST1")
assert db.get_listing("TEST1") is None
print("CRUD smoke test passed.")
