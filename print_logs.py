from sqlmodel import Session, select
from app.db import engine
from app.models import RequestLog


def main():
    with Session(engine) as session:
        rows = session.exec(select(RequestLog)).all()
        for r in rows:
            print(
                f"id={r.id}  op={r.operation}  in={r.input_json}  "
                f"out={r.result}  at={r.ts}"
            )


if __name__ == "__main__":
    main()
