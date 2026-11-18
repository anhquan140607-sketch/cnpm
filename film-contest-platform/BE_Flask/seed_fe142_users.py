"""
FE14.2 - Test Account Seeder

Chỉ sử dụng để tạo tài khoản kiểm thử trong môi trường development.
Không sử dụng các tài khoản này trong môi trường production.
"""
from dotenv import load_dotenv
load_dotenv(override=True)

from src.services.auth_service import AuthService

service = AuthService()

accounts = [
    {
        "email": "organizer.fe142.test@example.com",
        "password": "Fe142Test@2026",
        "full_name": "Organizer FE142 Test",
        "role": "organizer"
    },
    {
        "email": "participant.fe142.test@example.com",
        "password": "Fe142Test@2026",
        "full_name": "Participant FE142 Test",
        "role": "participant"
    }
]

for account in accounts:
    try:
        result = service.register(
            email=account["email"],
            password=account["password"],
            full_name=account["full_name"],
            role=account["role"]
        )

        print(
            "Tao tai khoan thanh cong:",
            result["user"]["email"],
            "| ID:",
            result["user"]["id"],
            "| Role:",
            result["user"]["role"]
        )

    except Exception as error:
        print("Khong the tao:", account["email"])
        print("Ly do:", error)
