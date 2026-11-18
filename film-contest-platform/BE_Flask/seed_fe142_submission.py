
import unicodedata
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)

from src.infrastructure.databases.factory_database import FactoryDatabase
from src.infrastructure.models.user_model import UserModel
from src.infrastructure.models.contest_model import ContestModel
from src.infrastructure.models.category_model import CategoryModel
from src.infrastructure.models.film_roll_model import FilmRollModel
from src.infrastructure.models.frame_model import FrameModel
from src.infrastructure.models.submission_model import SubmissionModel


def normalize(value):
    value = (value or "").lower().replace("đ", "d")
    value = unicodedata.normalize("NFD", value)
    return "".join(
        char for char in value
        if unicodedata.category(char) != "Mn"
    )


session = FactoryDatabase.get_database().get_session()

try:
    # 1. Tim participant
    participant = session.query(UserModel).filter_by(
        email="participant.fe142.test@example.com"
    ).first()

    if not participant:
        raise Exception("Khong tim thay participant.")

    # 2. Tim organizer va cuoc thi
    organizer = session.query(UserModel).filter_by(
        email="organizer.fe142.test@example.com"
    ).first()

    if not organizer:
        raise Exception("Khong tim thay organizer.")

    contest = session.query(ContestModel).filter_by(
        title="Cuoc thi nhiếp anh FE14.2 Test",
        created_by=organizer.id
    ).first()

    if not contest:
        raise Exception("Khong tim thay cuoc thi FE14.2.")

    # 3. Tim hang muc Thien nhien va phong canh
    categories = session.query(CategoryModel).filter_by(
        contest_id=contest.id
    ).all()

    category = next(
        (
            item for item in categories
            if "thien nhien" in normalize(item.name)
            and "phong canh" in normalize(item.name)
        ),
        None
    )

    if not category:
        raise Exception(
            "Khong tim thay hang muc Thien nhien va phong canh."
        )

    # 4. Tao Film Roll
    film_roll = session.query(FilmRollModel).filter_by(
        participant_id=participant.id,
        scan_specs="FE14.2_TEST_DATA"
    ).first()

    if not film_roll:
        film_roll = FilmRollModel(
            participant_id=participant.id,
            scan_specs="FE14.2_TEST_DATA",
            created_at=datetime.utcnow()
        )
        session.add(film_roll)
        session.flush()

    # 5. Tao Frame
    frame = session.query(FrameModel).filter_by(
        film_roll_id=film_roll.id,
        frame_number=1
    ).first()

    if not frame:
        frame = FrameModel(
            film_roll_id=film_roll.id,
            frame_number=1,
            shooting_location="Da Lat",
            created_at=datetime.utcnow()
        )
        session.add(frame)
        session.flush()

    # 6. Tao Submission
    submission = session.query(SubmissionModel).filter_by(
        frame_id=frame.id,
        title="Hoang hon tren nui"
    ).first()

    if not submission:
        submission = SubmissionModel(
            frame_id=frame.id,
            category_id=category.id,
            participant_id=participant.id,
            title="Hoàng hôn trên núi",
            description=(
                "Ánh nắng cuối ngày chiếu xuống những dãy núi, "
                "tạo nên khung cảnh thiên nhiên yên bình. "
                "Bầu trời chuyển màu cam đỏ trong ánh hoàng hôn."
            ),
            image_path="test-data/fe142_sample_photo.jpg",
            status="submitted",
            keywords="hoàng hôn, núi, thiên nhiên, phong cảnh",
            submitted_at=datetime.utcnow()
        )
        session.add(submission)
    else:
        # Dam bao bai test gan dung hang muc va tu khoa
        submission.category_id = category.id
        submission.description = (
            "Ánh nắng cuối ngày chiếu xuống những dãy núi, "
            "tạo nên khung cảnh thiên nhiên yên bình. "
            "Bầu trời chuyển màu cam đỏ trong ánh hoàng hôn."
        )
        submission.keywords = (
            "hoàng hôn, núi, thiên nhiên, phong cảnh"
        )

    session.commit()
    session.refresh(submission)

    print("\n===== TAO DU LIEU FE14.2 THANH CONG =====")
    print("Contest ID:", contest.id)
    print("Participant ID:", participant.id)
    print("Film Roll ID:", film_roll.id)
    print("Frame ID:", frame.id)
    print("Category ID:", category.id)
    print("Category:", category.name)
    print("Submission ID:", submission.id)
    print("Submission:", submission.title)

except Exception as error:
    session.rollback()
    print("\nTAO DU LIEU THAT BAI!")
    print("Loi:", error)

finally:
    session.close()
