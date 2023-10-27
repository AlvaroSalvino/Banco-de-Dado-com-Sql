import sqlalchemy as sqlA
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column, select
from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey


Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User (id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address (id={self.id}, email_address={self.email_address})"


print(User.__tablename__)
print(User.address)


# conexão com o banco de dados
engine = create_engine("sqlite://")

# Criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# Depreciado - Foi removido no em release
# print(engine.table_names())

# Investiga o esquema de banco de dados
inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("user_account"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    alvaro = User(
        name='alvaro',
        fullname='alvaro da Silva Salvino',
        address=[Address(email_address='alvaro.salvino@gmail.com')]
    )

    sandy = User(
        name='Sandy',
        fullname='Sandy Albuquerque',
        address=[Address(email_address='Sandy@email.com'),
                 Address(email_address='Sandygatinha@gostosa.com')]
    )

    patrick = User(name='patrick', fullname='patrick salvino')

# Enviando para o Banco de Dados (Persistência de dados)
    session.add_all([alvaro, sandy, patrick])

    session.commit()

stmt = select(User).where(User.name.in_(['alvaro']))
print('Recuperando usuários a partir de condição de filtragem')
for user in session.scalars(stmt):
    print(user)

stmt_address = select(Address).where(Address.user_id.in_([2]))
print('\nRecuperando os endereços de email de Sandy')
for stmt_address in session.scalars(stmt_address):
    print(stmt_address)

stmt_order = select(User).order_by(User.fullname.desc())
print('Recuperando info de maneira ordenada')
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
for result in session.scalars(stmt_join):
    print(result)

# print(select(User.fullname, Address.email_address).join_from(Address, User))

connection = 