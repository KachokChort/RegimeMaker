import json
import sqlite3
import datetime
from fastapi import FastAPI, Request
import uvicorn
from data import db_session
from data.users import User
from data.cycles import Cycle

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# REGISTRATION
@app.post("/sign_up/")
async def create_user(request:  Request):
    body = await request.body()

    data = json.loads(body)
    username = data.get("username")
    password = data.get("password")
    if not username or not password or not username.strip() or not password.strip():
        return {"error": "Username and password are required params."}
    if len(password) <= 3:
        return {"error": "Short password."}

    try:
        db_session.global_init("db/db.db")
        db_sess = db_session.create_session()
        users = [user.username for user in db_sess.query(User).all()]
        if username in users:
            return {"error": "This name is already taken"}
        new_user = User()
        new_user.username = username
        new_user.password = password
        db_sess.add(new_user)
        db_sess.commit()
        db_sess.close()
    except sqlite3.IntegrityError as e:
        return {"error": f"{e}"}
    except Exception as e:
        return {"error": f"{e}"}

    return {"verdict": f"You successful sign up with username: {username}."}

#CREATING_SYSTEM
@app.post("/create_cycle/")
async def create_system(request:  Request):
    body = await request.body()

    data = json.loads(body)
    name = data.get("name")
    user = data.get("user")
    days_count = int(data.get("days_count"))
    descriptions = data.get("descriptions")
    password = data.get("password")

    if not name:
        return {"error": "Name is required parameter."}
    if not password:
        return {"error": "Password is required parameter."}
    if not days_count:
        return {"error": "Days_count is required parameter."}
    if not descriptions:
        return {"error": "Description is required parameter."}
    if days_count != len(descriptions):
        return {"error": "Invalid count elements in descriptions."}
    try:
        db_session.global_init("db/db.db")
        db_sess = db_session.create_session()
        users = [user.username for user in db_sess.query(User).all()]
        if user not in users:
            return {"error": "Invalid user."}
        user_password = db_sess.query(User).filter(User.username == user).first().password
        if password != user_password:
            return {"error": f"Invalid password."}
        user_cycles = [c.name for c in db_sess.query(Cycle).filter(Cycle.user == user)]
        if name in user_cycles:
            return {"error": "You already have this cycle name."}
        new_cycle = Cycle()
        new_cycle.name = name
        new_cycle.user = user
        new_cycle.days_count = days_count
        new_cycle.descriptions = descriptions
        db_sess.add(new_cycle)
        db_sess.commit()
        db_sess.close()
    except sqlite3.IntegrityError as e:
        print(e)
        return {"error": f"{e}"}
    except Exception as e:
        print(e)
        return {"error": f"{e}"}
    return {"verdict": f"You successful create new cycle with name: {name}"}


#TODAY
@app.post("/day/")
async def create_system(request:  Request):
    body = await request.body()

    data = json.loads(body)
    user = data.get("user")
    day = data.get("day")
    password = data.get("password")

    if not user:
        return {"error": "User is required parameter."}
    if not password:
        return {"error": "Password is required parameter."}
    if not day:
        return {"error": "Day is required parameter."}
    try:
        db_session.global_init("db/db.db")
        db_sess = db_session.create_session()
        users = [user.username for user in db_sess.query(User).all()]
        if user not in users:
            return {"error": "Invalid user."}
        user_password = db_sess.query(User).filter(User.username == user).first().password
        if password != user_password:
            return {"error": f"Invalid password."}
        #-------------------------------
        date_user = db_sess.query(User).filter(User.username == user).first().created_at.date()
        format_string = "%Y-%m-%d"
        date = datetime.datetime.strptime(day, format_string).date()
        days = date - date_user
        # print(date, date_user)
        # print(days)
        days = days.days
        # print(days)
        duties = []
        # print(db_sess.query(Cycle).filter(Cycle.user == user).all())
        for cycle in db_sess.query(Cycle).filter(Cycle.user == user).all():
            #print(cycle.days_count)
            dd = int(days) % int(cycle.days_count)
            descriptions = cycle.descriptions
            print(descriptions)
            duties.append(descriptions[dd])
            print(duties)
        return duties
        # -------------------------------
    except sqlite3.IntegrityError as e:
        print(e)
        return {"error": f"{e}"}
    except Exception as e:
        print(e)
        return {"error": f"{e}"}


if __name__ == "__main__":
    uvicorn.run(
        "web:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )