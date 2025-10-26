from data.db_session import create_session, global_init
from data.users import User
from data.cycles import Cycle
from data.notes import Note

global_init("db/db.db")

# user = User()
# user.username = "Tima"
# user.password = "12345"
db_session = create_session()
# db_session.add(user)
# db_session.commit()

data = []
for user in db_session.query(User).all():
    print(vars(user))
    data.append(user)
print(data)

data = []
for cycle in db_session.query(Cycle).all():
    print(vars(cycle))
    data.append(cycle)
print(data)

data = []
for cycle in db_session.query(Note).all():
    print(vars(cycle))
    data.append(cycle)
print(data)

