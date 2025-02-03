from mongodb import DBConnection

db = DBConnection()
company_info = db.get_collection("employees").find_one()

if company_info:
    print("✅ Successfully retrieved employees information:", company_info)
else:
    print("⚠️ No employees data found.")