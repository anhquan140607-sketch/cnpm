
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(override=True)

from src.infrastructure.databases.factory_database import FactoryDatabase
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.models.contest_model import ContestModel
from src.infrastructure.models.category_model import CategoryModel

session = FactoryDatabase.get_database().get_session()

try:
    # Tim tai khoan organizer
    organizer = session.query(UserModel).filter_by(
        email="organizer.fe142.test@example.com"
    ).first()

    if not organizer:
        raise Exception("Khong tim thay tai khoan organizer.")

    now = datetime.utcnow()

    # Kiem tra cuoc thi da ton tai chua
    contest = session.query(ContestModel).filter_by(
        title="Cuoc thi nhiếp anh FE14.2 Test",
        created_by=organizer.id
    ).first()

    if not contest:
        contest = ContestModel(
            title="Cuoc thi nhiếp anh FE14.2 Test",
            theme="Ve dep cuoc song",
            description="Cuoc thi dung de kiem thu chuc nang FE14.2.",
            regulations="Moi nguoi tham gia co the gui anh theo cac hang muc.",
            submission_start=now - timedelta(days=1),
            submission_end=now + timedelta(days=30),
            judging_start=now + timedelta(days=31),
            judging_end=now + timedelta(days=45),
            status="published",
            config_locked=False,
            created_by=organizer.id,
            created_at=now,
            updated_at=now
        )

        session.add(contest)
        session.flush()

    # Ba hang muc va tu khoa nhan dien
    categories = [
        {
            "name": "Thien nhien va phong canh",
            "rules": "Nui rung bien song cay coi hoa la bau troi hoang hon binh minh."
        },
        {
            "name": "Chan dung va con nguoi",
            "rules": "Chan dung khuon mat con nguoi cam xuc gia dinh ban be."
        },
        {
            "name": "Kien truc va do thi",
            "rules": "Nha cua toa nha cau duong pho thanh pho cong trinh."
        }
    ]

    for item in categories:
        existing = session.query(CategoryModel).filter_by(
            contest_id=contest.id,
            name=item["name"]
        ).first()

        if not existing:
            category = CategoryModel(
                contest_id=contest.id,
                name=item["name"],
                max_photos_per_participant=5,
                submission_rules=item["rules"],
                award_structure=None,
                created_at=now
            )
            session.add(category)

    session.commit()

    print("\n===== TAO DU LIEU FE14.2 THANH CONG =====")
    print("Contest ID:", contest.id)
    print("Contest:", contest.title)
    print("Organizer ID:", organizer.id)

    saved_categories = session.query(CategoryModel).filter_by(
        contest_id=contest.id
    ).all()

    for category in saved_categories:
        print(
            "Category ID:", category.id,
            "| Name:", category.name
        )

except Exception as error:
    session.rollback()
    print("LOI:", error)

finally:
    session.close()
