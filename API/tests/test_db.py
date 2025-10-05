from ..data.db_session import create_session, global_init
from ..data.users import User

global_init("db/db.db")

# user = User()
# user.username = "Tima"
# user.password = "12345"
db_session = create_session()
# db_session.add(user)
# db_session.commit()

data = []
for user in db_session.query(User).all():
    print(user)
    data.append(user)
print(data)