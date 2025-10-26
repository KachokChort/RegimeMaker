import json
import sqlite3
import datetime
from fastapi import FastAPI, Request
import uvicorn
from data import db_session
from data.users import User
from data.cycles import Cycle
from data.notes import Note

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


# REGISTRATION
@app.post("/sign_up/")
async def create_user(request: Request):
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


# CREATING_SYSTEM
@app.post("/create_cycle/")
async def create_system(request: Request):
    body = await request.body()

    data = json.loads(body)
    name = data.get("name")
    user = data.get("user")
    days_count = int(data.get("days_count"))
    pause = int(data.get("pause"))
    descriptions = data.get("descriptions")
    password = data.get("password")
    start_at = data.get("start_at")

    try:
        format_string = "%Y-%m-%d"
        date = datetime.datetime.strptime(start_at, format_string).date()
    except Exception as e:
        print(f"Error start_at: {e}")
        return {"error": "Invalid start_at."}
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
    if pause < 0:
        return {"error": "Negative pause."}
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
        new_cycle.pause = pause
        new_cycle.descriptions = descriptions
        new_cycle.start_at = start_at
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


# TODAY
@app.post("/day/")
async def create_system(request: Request):
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
        # -------------------------------
        date_user = db_sess.query(Cycle).filter(Cycle.user == user).first().start_at
        format_string = "%Y-%m-%d"
        date = datetime.datetime.strptime(day, format_string).date()
        date_user = datetime.datetime.strptime(date_user, format_string).date()
        days = date - date_user
        # print(date, date_user)
        # print(days)
        days = days.days
        # print(days)
        duties = []
        # print(db_sess.query(Cycle).filter(Cycle.user == user).all())
        for cycle in db_sess.query(Cycle).filter(Cycle.user == user).all():
            # print(cycle.days_count)
            dd = int(days) % (int(cycle.days_count) + int(cycle.pause))
            descriptions = cycle.descriptions
            # print(descriptions)
            try:
                duties.append(descriptions[abs(dd)])
            except IndexError as e:
                pass
            # print(duties)
        return {"verdict": "Successful getting duties.", "duties": duties}
        # -------------------------------
    except sqlite3.IntegrityError as e:
        print(e)
        return {"error": f"{e}"}
    except Exception as e:
        print(e)
        return {"error": f"{e}"}


@app.post("/delete_cycle/")
async def create_system(request: Request):
    body = await request.body()

    data = json.loads(body)
    cycle_name = data.get("cycle_name")
    user = data.get("user")
    password = data.get("password")

    if not user:
        return {"error": "User is required parameter."}
    if not password:
        return {"error": "Password is required parameter."}
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
        if cycle_name not in user_cycles:
            return {"error": f"You have not with cycle. Your cycles: {user_cycles}"}

        db_sess.query(Cycle).filter(Cycle.name == cycle_name).delete()
        db_sess.commit()

        return {"verdict": f"Successful delete cycle: {cycle_name}"}

    except sqlite3.IntegrityError as e:
        print(e)
        return {"error": f"{e}"}
    except Exception as e:
        print(e)
        return {"error": f"{e}"}


@app.post("/user_cycles/")
async def read_root(request: Request):
    body = await request.body()

    data = json.loads(body)

    user = data.get("user")
    password = data.get("password")

    if not user:
        return {"error": "User is required parameter."}
    if not password:
        return {"error": "Password is required parameter."}
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

        return {"verdict": "Successful getting cycles.", "cycles": user_cycles}

    except sqlite3.IntegrityError as e:
        print(e)
        return {"error": f"{e}"}
    except Exception as e:
        print(e)
        return {"error": f"{e}"}


@app.post("/create_note/")
async def create_system(request: Request):
    body = await request.body()

    data = json.loads(body)
    name = data.get("name")
    user = data.get("user")
    descriptions = data.get("descriptions")
    password = data.get("password")

    if not name:
        return {"error": "Name is required parameter."}
    if not password:
        return {"error": "Password is required parameter."}
    if not descriptions:
        return {"error": "Description is required parameter."}
    if type(descriptions) is not str:
        return {"error": "Invalid description."}
    try:
        db_session.global_init("db/db.db")
        db_sess = db_session.create_session()
        users = [user.username for user in db_sess.query(User).all()]
        if user not in users:
            return {"error": "Invalid user."}
        user_password = db_sess.query(User).filter(User.username == user).first().password
        if password != user_password:
            return {"error": f"Invalid password."}
        user_notes = [c.name for c in db_sess.query(Note).filter(Note.user == user)]
        if name in user_notes:
            return {"error": "You already have this note name."}

        #-----------------------------
        new_note = Note()
        new_note.name = name
        new_note.user = user
        new_note.descriptions = descriptions
        db_sess.add(new_note)
        db_sess.commit()
        db_sess.close()
        # -----------------------------

    except sqlite3.IntegrityError as e:
        print(e)
        return {"error": f"{e}"}
    except Exception as e:
        print(e)
        return {"error": f"{e}"}
    return {"verdict": f"You successful create new note with name: {name}"}


@app.post("/get_notes/")
async def read_root(request: Request):
    body = await request.body()

    data = json.loads(body)

    user = data.get("user")
    password = data.get("password")

    if not user:
        return {"error": "User is required parameter."}
    if not password:
        return {"error": "Password is required parameter."}
    try:
        db_session.global_init("db/db.db")
        db_sess = db_session.create_session()
        users = [user.username for user in db_sess.query(User).all()]
        if user not in users:
            return {"error": "Invalid user."}
        user_password = db_sess.query(User).filter(User.username == user).first().password
        if password != user_password:
            return {"error": f"Invalid password."}
        user_notes = [c.name for c in db_sess.query(Note).filter(Note.user == user)]

        return {"verdict": "Successful getting notes.", "notes": user_notes}

    except sqlite3.IntegrityError as e:
        print(e)
        return {"error": f"{e}"}
    except Exception as e:
        print(e)
        return {"error": f"{e}"}


@app.post("/delete_note/")
async def create_system(request: Request):
    body = await request.body()

    data = json.loads(body)
    note_name = data.get("note_name")
    user = data.get("user")
    password = data.get("password")

    if not user:
        return {"error": "User is required parameter."}
    if not password:
        return {"error": "Password is required parameter."}
    try:
        db_session.global_init("db/db.db")
        db_sess = db_session.create_session()
        users = [user.username for user in db_sess.query(User).all()]
        if user not in users:
            return {"error": "Invalid user."}
        user_password = db_sess.query(User).filter(User.username == user).first().password
        if password != user_password:
            return {"error": f"Invalid password."}
        user_notes = [c.name for c in db_sess.query(Note).filter(Note.user == user)]
        if note_name not in user_notes:
            return {"error": f"You have not with note. Your notes: {user_notes}"}

        db_sess.query(Note).filter(Note.name == note_name).delete()
        db_sess.commit()

        return {"verdict": f"Successful delete cycle: {note_name}"}

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
