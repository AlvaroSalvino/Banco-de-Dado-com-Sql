import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey


engine = create_engine('sqlite:///:memory')

metadata_obj = MetaData()
user = Table(
    'user',
    metadata_obj,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(40), nullable=False),
    Column('email_address', String(60)),
    Column('nickmane', String(50), nullable=False)
)

user_prefs = Table(
    'user_prefs', metadata_obj,
    Column('pref_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("user.user_id"), nullable=False),
    Column('pref_name', String(40), nullable=False),
    Column('pref_value', String(100))
)

print('\nInfo da tabela users')
print(user_prefs.primary_key)
print(user_prefs.constraints)

print(metadata_obj.tables)


for table in metadata_obj.sorted_tables:
    print(table)

metadata_obj.create_all(engine)


metadata_db_obj = MetaData()
financial_info = Table(
    'financial_info',
    metadata_db_obj,
    Column('id', Integer, primary_key=True),
    Column('value', String(100), nullable=False)
)

# Inserino info na tabela user
sql_insert = text("Insert into user values(1, 'Maria', 'asfasfino@gmail.com', 'Ma')")
engine.execute(sql_insert)

print('\nInfo da tabela financial_info')
print(financial_info.primary_key)
print(financial_info.constraints)

print('\nExecutando Statement sql')
sql = text('select * from user')
result = engine.execute(sql)
for row in result:
    print(row)



