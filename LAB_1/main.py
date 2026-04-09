from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('sqlite:///lab1.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Group(Base):
    __tablename__ = 'GROUPS'
    id_group = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(30))
    course = Column(Integer)

class Student(Base):
    __tablename__ = 'STUDENTS'
    id_student = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    surname = Column(String(50))
    birthday = Column(String(10))
    id_group = Column(Integer, ForeignKey('GROUPS.id_group'))

class Subject(Base):
    __tablename__ = 'SUBJECTS'
    id_subject = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(String(50))
    hours_per_subject = Column(Integer)
    atestation_form = Column(String(30))

class Plan(Base):
    __tablename__ = 'PLANS'
    id_group = Column(Integer, ForeignKey('GROUPS.id_group'), primary_key=True)
    id_subject = Column(Integer, ForeignKey('SUBJECTS.id_subject'), primary_key=True)

Base.metadata.create_all(engine)

session.add_all([
    Group(group_name='PO135', course=1),
    Group(group_name='PO135', course=1),
    Group(group_name='PO235', course=2),
    Group(group_name='PO235', course=2),
    Group(group_name='PO335', course=3),
    Group(group_name='PO335', course=3)
])

session.add_all([
    Subject(subject_name='PHYSICS', hours_per_subject=200),
    Subject(subject_name='MATH', hours_per_subject=120),
    Subject(subject_name='BASE ALGORITHMIZATION', hours_per_subject=70),
    Subject(subject_name='DATABASE DESIGN', hours_per_subject=130),
    Subject(subject_name='VISUAL PROGRAMMING TOOLS', hours_per_subject=90),
    Subject(subject_name='OOP', hours_per_subject=70)
])

session.add_all([
    Student(name='Fedorenko', surname='P.', birthday='25.12.1997', id_group=1),
    Student(name='Zingel', surname='O.', birthday='25.12.1985', id_group=2),
    Student(name='Savitskayan', surname='N.',birthday='22.09.1987', id_group=3),
    Student(name='Kovalchuk', surname='M.', birthday='17.06.1992', id_group=4),
    Student(name='Kovrigo', surname='T.', birthday='13.05.1992', id_group=5),
    Student(name='Shpanko', surname='N.', birthday='14.08.1992', id_group=6)
])
session.commit()
session.query(Group).filter(Group.group_name =='PO135').update({"group_name": "PO134"})
session.query(Group).filter(Group.group_name == 'PO135').delete()

for s in session.query(Subject).filter(Subject.subject_name.in_(['VISUAL PROGRAMMING TOOLS', 'OOP'])):
    s.hours_per_subject = s.hours_per_subject + 30

session.query(Subject).filter(Subject.subject_name == 'BASE ALGORITHMIZATION').update({"atestation_form": "ZACHET"})
session.query(Subject).filter(Subject.subject_name !='BASE ALGORITHMIZATION').update({"atestation_form": "EXAM"})
session.commit()

print("--- STUDENTS ---")
all_students = session.query(Student).all()
for s in all_students:
    print(f"ID: {s.id_student} | Имя: {s.name} | Фамилия: {s.surname} | Группа: {s.id_group}")

print("\n--- GROUPS ---")
all_groups = session.query(Group).all()
for g in all_groups:
    print(f"ID: {g.id_group} | Название: {g.group_name} | Курс: {g.course}")

print("\n--- SUBJECTS ---")
all_subjects = session.query(Subject).all()
for sub in all_subjects:
    print(f"Предмет: {sub.subject_name} | Часы: {sub.hours_per_subject} | Форма: {sub.atestation_form}")
