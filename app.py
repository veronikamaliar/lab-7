from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date, func
from sqlalchemy.orm import declarative_base, Session, relationship
from datetime import datetime


# Підключення до бази даних
engine = create_engine('sqlite:///ownincome.db', echo=False)
Base = declarative_base()

# Оголошення класів моделей
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    expenses = relationship("Expense", back_populates="user")
    incomes = relationship("Income", back_populates="user")

class ExpenseCategory(Base):
    __tablename__ = 'expense_categories'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String)
    expenses = relationship("Expense", back_populates="category")

class Expense(Base):
    __tablename__ = 'expenses'
    expense_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    category_id = Column(Integer, ForeignKey('expense_categories.category_id'))
    amount = Column(Float)
    date_incurred = Column(Date)
    user = relationship("User", back_populates="expenses")
    category = relationship("ExpenseCategory", back_populates="expenses")

class IncomeSource(Base):
    __tablename__ = 'income_sources'
    income_source_id = Column(Integer, primary_key=True)
    source_name = Column(String)
    description = Column(String)
    incomes = relationship("Income", back_populates="source")

class Income(Base):
    __tablename__ = 'incomes'
    income_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    income_source_id = Column(Integer, ForeignKey('income_sources.income_source_id'))
    amount = Column(Float)
    date_received = Column(Date)
    user = relationship("User", back_populates="incomes")
    source = relationship("IncomeSource", back_populates="incomes")


# Створення таблиць
Base.metadata.create_all(engine)

# Створення сесії
def create_session():
    return Session(engine)

# Створення нового користувача
def create_user(session, first_name, last_name, email, password):
    user = User(first_name=first_name, last_name=last_name, email=email, password=password)
    session.add(user)
    session.commit()

# Створення нової категорії витрат
def create_expense_category(session, category_name):
    category = ExpenseCategory(category_name=category_name)
    session.add(category)
    session.commit()

# Створення нової витрати
def create_expense(session, user_id, category_id, amount, date_incurred):
    expense = Expense(user_id=user_id, category_id=category_id, amount=amount, date_incurred=date_incurred)
    session.add(expense)
    session.commit()

# Створення нового джерела доходу
def create_income_source(session, source_name, description):
    source = IncomeSource(source_name=source_name, description=description)
    session.add(source)
    session.commit()

# Створення нового доходу
def create_income(session, user_id, income_source_id, amount, date_received):
    income = Income(user_id=user_id, income_source_id=income_source_id, amount=amount, date_received=date_received)
    session.add(income)
    session.commit()


# Отримати дані
def get_all_users(session):
    return session.query(User).all()

def get_all_expense_categories(session):
    return session.query(ExpenseCategory).all()

def get_all_expense(session):
    return session.query(Expense).all()

def get_all_income_source(session):
    return session.query(IncomeSource).all()

def get_all_income(session):
    return session.query(Income).all()


# Оновлення даних
def update_user(session, user_id, first_name=None, last_name=None, email=None, password=None):
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        if password:
            user.password = password
        session.commit()

def update_expense_category(session, category_id, category_name):
    category = session.query(ExpenseCategory).filter(ExpenseCategory.category_id == category_id).first()
    if category:
        category.category_name = category_name
        session.commit()

def update_expense(session, expense_id, amount=None, date_incurred=None, user_id=None, category_id=None):
    expense = session.query(Expense).filter(Expense.expense_id == expense_id).first()
    if expense:
        if amount:
            expense.amount = amount
        if date_incurred:
            expense.date_incurred = date_incurred
        if user_id:
            expense.user_id = user_id
        if category_id:
            expense.category_id = category_id
        session.commit()

def update_income_source(session, income_source_id, source_name=None, description=None):
    source = session.query(IncomeSource).filter(IncomeSource.income_source_id == income_source_id).first()
    if source:
        if source_name:
            source.source_name = source_name
        if description:
            source.description = description
        session.commit()

def update_income(session, income_id, amount=None, date_received=None, user_id=None, income_source_id=None):
    income = session.query(Income).filter(Income.income_id == income_id).first()
    if income:
        if amount:
            income.amount = amount
        if date_received:
            income.date_received = date_received
        if user_id:
            income.user_id = user_id
        if income_source_id:
            income.income_source_id = income_source_id
        session.commit()


# Пошук даних
def search_income_sources_by_name(session, source_name):
    return session.query(IncomeSource).filter(IncomeSource.source_name == source_name).first()


# Видалення даних
def delete_user(session, user_id):
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        session.delete(user)
        session.commit()

def delete_expense_category(session, category_id):
    category = session.query(ExpenseCategory).filter(ExpenseCategory.category_id == category_id).first()
    if category:
        session.delete(category)
        session.commit()

def delete_expense(session, expense_id):
    expense = session.query(Expense).filter(Expense.expense_id == expense_id).first()
    if expense:
        session.delete(expense)
        session.commit()

def delete_income_source(session, income_source_id):
    source = session.query(IncomeSource).filter(IncomeSource.income_source_id == income_source_id).first()
    if source:
        session.delete(source)
        session.commit()

def delete_income(session, income_id):
    income = session.query(Income).filter(Income.income_id == income_id).first()
    if income:
        session.delete(income)
        session.commit()


# Закриття сесії
def close_session(session):
    session.close()

session = create_session()


# CRUD операції

users_to_add = [
    ['John', 'Smith', 'john.smith@gmail.com', '123J45'],
    ['Ann', 'Mari', 'ann.mari@gmail.com', '6A789']
]
for item in users_to_add:
    create_user(session, item[0], item[1], item[2], item[3])


expense_categories_to_add = [
    ['Food'],
    ['Transport'],
    ['Utilities']
]
for item in expense_categories_to_add:
    create_expense_category(session, item[0])

income_sources_to_add = [
    ['Salary', 'Monthly salary from employer'],
    ['Freelance', 'Freelance work income'],
    ['Investment', 'Income from investments']
]
for item in income_sources_to_add:
    create_income_source(session, item[0], item[1])


expenses_to_add = [
    [1, 1, 200, datetime.strptime('2024-12-01', '%Y-%m-%d').date()],
    [2, 2, 50, datetime.strptime('2024-12-01', '%Y-%m-%d').date()],
    [1, 3, 100, datetime.strptime('2024-12-01', '%Y-%m-%d').date()]
]
for item in expenses_to_add:
    create_expense(session, item[0], item[1], item[2], item[3])



incomes_to_add = [
    [1, 1, 1500, datetime.strptime('2024-12-01', '%Y-%m-%d').date()],
    [2, 2, 1200, datetime.strptime('2024-12-01', '%Y-%m-%d').date()],
    [1, 3, 800, datetime.strptime('2024-12-01', '%Y-%m-%d').date()]
]
for item in incomes_to_add:
    create_income(session, item[0], item[1], item[2], item[3])


update_user(session, user_id=1, email='johnnn@gmail.com')

delete_expense_category(session, category_id=3)

income_source = search_income_sources_by_name(session, 'Фріланс')
if income_source:
    print(income_source.source_name, income_source.description)
else:
    print("Джерело доходу не знайдено.")



# Вивід всіх даних
all_users = get_all_users(session)
print("Всі користувачі:")
for user in all_users:
    print(user.user_id, user.first_name, user.last_name, user.email)

all_expense_categories = get_all_expense_categories(session)
print("Всі категорії витрат:")
for category in all_expense_categories:
    print(category.category_id, category.category_name)

all_income_sources = get_all_income_source(session)
print("Всі джерела доходу:")
for source in all_income_sources:
    print(source.income_source_id, source.source_name, source.description)

all_expenses = get_all_expense(session)
print("Всі витрати:")
for expense in all_expenses:
    print(expense.expense_id, expense.user_id, expense.category_id, expense.amount, expense.date_incurred)

all_incomes = get_all_income(session)
print("Всі доходи:")
for income in all_incomes:
    print(income.income_id, income.user_id, income.income_source_id, income.amount, income.date_received)




# Закриття сесії
close_session(session)