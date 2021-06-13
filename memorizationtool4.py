from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

def get_menuno():
    while True:
        print("1. Add flashcards")
        print("2. Practice flashcards")
        print("3. Exit")
        number = input()
        if number in ("1", "2", "3"):
            return int(number)
        print(f"{number} is not an option")
        print()

def get_addmenuno():
    while True:
        print("1. Add a new flashcard")
        print("2. Exit")
        number = input()
        if number in ("1", "2"):
            return int(number)
        print()
        print(f"{number} is not an option")
        print()

def add_card(session):
    while True:
        no = get_addmenuno()
        if no == 2:
            return
    
        print()
        while True:
            print("Question:")
            question = input()
            if question != "":
                break
        while True:
            print("Answer:")
            answer = input()
            if answer != "":
                break
        write_db(session, question, answer)
        print()

def delete_card(session, row):
    session.delete(row)
    session.commit()

def edit_card(session, row):
    print(f"current question: {row.question}")
    print("please write a new question:")
    question = input()
    print()
    print(f"current answer: {row.answer}")
    print("please write a new answer:")
    answer = input()
    print()
    row.question = question
    row.answer = answer
    session.commit()

def rankup(session, row):
    if row.box == 3:
        delete_card(session, row)
    else:
        row.box += 1
        session.commit()

def rankdown(session, row):
    if row.box == 1:
        return
    else:    
        row.box -= 1
        session.commit()

def update_card(session, row):
    while True:
        print('press "d" to delete the flashcard:')
        print('press "e" to edit the flashcard:')
        de = input()
        if de in ("d", "e"):
            break
        print(f"{de} is not an option")

    print()
    if de == "d":
        delete_card(session, row)
    elif de == "e":
        edit_card(session, row)

def score_card(session, row):
    while True:
        print('press "y" if your answer is correct:')
        print('press "n" if your answer is wrong:')
        yn = input()
        if yn in ("y", "n"):
            break
        print(f"{yn} is not an option")
    print()
    if yn == "y":
        rankup(session, row)
    elif yn == "n":
        rankdown(session, row)

def practice_card(session):
    rows = query_db(session)
    if len(rows) == 0:
        print("There is no flashcard to practice!")
        return

    print()
    for row in rows:
        while True:
            print(f"Question: {row.question}")
            print('press "y" to see the answer:')
            print('press "n" to skip:')
            print('press "u" to update:')
            ynu = input()
            if ynu in ("y", "n", "u"):
                break
            print(f"{ynu} is not an option")
        if ynu == "y":
            print()
            print(f"Answer: {row.answer}")
            score_card(session, row)
        elif ynu == "n":
            print()
            score_card(session, row)
        elif ynu == "u":
            update_card(session, row)
    print()

def write_db(session, question, answer):
    new_row = Table(question=question, answer=answer, box=1)
    session.add(new_row)
    session.commit()

def query_db(session):
    return session.query(Table).all()

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base = declarative_base()

class Table(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String)
    answer = Column(String)
    box = Column(Integer)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

while True:
    no = get_menuno()
    if no == 1:
        add_card(session)
    elif no == 2:
        practice_card(session)
    elif no == 3:
        break
    print()
print("Bye!")