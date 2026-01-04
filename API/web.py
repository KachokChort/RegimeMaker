import json
import sqlite3
import datetime
from fastapi import FastAPI, Request
import uvicorn
from data import db_session
from data.users import User
from data.cycles import Cycle
from data.notes import Note
from data.muscles import MUSCLE_GROUPS

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello World"}


@app.post("/user/")
async def user(request: Request):
    body = await request.body()

    data = json.loads(body)
    username = data.get("username")
    password = data.get("password")
    if not username or not password or not username.strip() or not password.strip():
        return {"error": "Username and password are required params."}

    try:
        db_session.global_init("db/db.db")
        db_sess = db_session.create_session()
        users = [user.username for user in db_sess.query(User).all()]
        if username not in users:
            return {"error": "This user does not exist."}
        user_password = db_sess.query(User).filter(User.username == username).first().password
        if password != user_password:
            return {"error": f"Invalid password."}
    except sqlite3.IntegrityError as e:
        return {"error": f"{e}"}
    except Exception as e:
        return {"error": f"{e}"}

    return {"verdict": "This user exists."}


# REGISTRATION
@app.post("/sign_up/")
async def sign_up(request: Request):
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
        new_user.days = {}
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
async def create_cycle(request: Request):
    body = await request.body()

    data = json.loads(body)
    name = data.get("name")
    user = data.get("user")
    days_count = int(data.get("days_count"))
    pause = int(data.get("pause"))
    descriptions = data.get("descriptions")
    data_cycle = data.get("data_cycle")
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
    if not data_cycle:
        return {"error": "Data_cycle is required parameter."}
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
        new_cycle.data = data_cycle
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
async def day(request: Request):
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

        user_obj = db_sess.query(User).filter(User.username == user).first()

        users = [user.username for user in db_sess.query(User).all()]
        if user not in users:
            return {"error": "Invalid user."}
        user_password = user_obj.password
        if password != user_password:
            return {"error": f"Invalid password."}
        # -------------------------------
        format_string = "%Y-%m-%d"
        date = datetime.datetime.strptime(day, format_string).date()

        duties = {}
        for cycle in db_sess.query(Cycle).filter(Cycle.user == user).all():
            date_cycle = cycle.start_at
            print(date_cycle)
            date_cycle = datetime.datetime.strptime(date_cycle, format_string).date()
            days = date - date_cycle
            days = days.days
            dd = int(days) % (int(cycle.days_count) + int(cycle.pause))
            descriptions = cycle.descriptions
            # print(descriptions, dd)
            try:
                duties[descriptions[abs(dd)]] = 0
            except IndexError as e:
                print(e)
        # print(duties)
        # print("AHAHAAHAHHAHAAHHAHAAHHAAHHAAHAHAHAAHAH")
        if day not in user_obj.days:
            user_days = user_obj.days.copy()
            user_days[day] = duties
            user_obj.days = user_days.copy()
            db_sess.commit()
            db_sess.close()
            return {"verdict": "Successful getting duties.", "duties": duties}
        else:
            user_duties = user_obj.days[day].copy()
            for i in duties:
                if i in user_duties:
                    duties[i] = user_duties[i]
            print(duties)
            user_days = user_obj.days.copy()
            user_days[day] = duties
            user_obj.days = user_days.copy()
            db_sess.commit()
            db_sess.close()
            return {"verdict": "Successful getting duties.", "duties": duties}

        # -------------------------------
    except sqlite3.IntegrityError as e:
        print(e)
        return {"error": f"{e}"}
    except Exception as e:
        print(e)
        return {"error": f"{e}"}


@app.post("/delete_cycle/")
async def delete_cycle(request: Request):
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
        db_sess.close()

        return {"verdict": f"Successful delete cycle: {cycle_name}"}

    except sqlite3.IntegrityError as e:
        print(e)
        return {"error": f"{e}"}
    except Exception as e:
        print(e)
        return {"error": f"{e}"}


@app.post("/user_cycles/")
async def get_cycles(request: Request):
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
        user_cycles = [c for c in db_sess.query(Cycle).filter(Cycle.user == user)]
        # print(user_cycles)
        # db_sess.commit()
        # db_sess.close()

        return {"verdict": "Successful getting cycles.", "cycles": user_cycles}

    except sqlite3.IntegrityError as e:
        print(e)
        return {"error": f"{e}"}
    except Exception as e:
        print(e)
        return {"error": f"{e}"}


@app.post("/create_note/")
async def create_note(request: Request):
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

        # -----------------------------
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
async def get_notes(request: Request):
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
        user_notes = [n for n in db_sess.query(Note).filter(Note.user == user)]
        # db_sess.commit()
        # db_sess.close()
        return {"verdict": "Successful getting notes.", "notes": user_notes}

    except sqlite3.IntegrityError as e:
        print(e)
        return {"error": f"{e}"}
    except Exception as e:
        print(e)
        return {"error": f"{e}"}


@app.post("/delete_note/")
async def delete_note(request: Request):
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
        db_sess.close()

        return {"verdict": f"Successful delete cycle: {note_name}"}

    except sqlite3.IntegrityError as e:
        print(e)
        return {"error": f"{e}"}
    except Exception as e:
        print(e)
        return {"error": f"{e}"}


@app.post("/duty/")
async def duty(request: Request):
    body = await request.body()

    data = json.loads(body)
    selected_date = data.get("selected_date")
    duty_name = data.get("duty_name")
    username = data.get("user")
    password = data.get("password")

    # print(selected_date, duty_name)

    if not username:
        return {"error": "User is required parameter."}
    if not password:
        return {"error": "Password is required parameter."}
    try:
        db_session.global_init("db/db.db")
        db_sess = db_session.create_session()
        users = [user.username for user in db_sess.query(User).all()]
        if username not in users:
            return {"error": "Invalid user."}
        user_password = db_sess.query(User).filter(User.username == username).first().password
        if password != user_password:
            return {"error": f"Invalid password."}
        user = db_sess.query(User).filter(User.username == username).first()
        print(user.days.get(selected_date), duty_name)
        res = user.days.get(selected_date).get(duty_name)
        print(res)
        new_days = user.days.copy()
        db_sess.commit()
        new_days[selected_date][duty_name] = 1 - res
        # print(new_days)
        user.days = new_days.copy()

        db_sess.commit()

        return {"verdict": f"Successful change of duty completion.", "duties": user.days.copy()}

    except sqlite3.IntegrityError as e:
        print(e)
        return {"error": f"{e}"}
    except Exception as e:
        print(e)
        return {"error": f"{e}"}


@app.post("/analytics/")
async def analytics(request: Request):
    body = await request.body()

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format"}

    cycle_name = data.get("cycle_name")
    username = data.get("user")
    password = data.get("password")

    if not username:
        return {"error": "User is required parameter."}
    if not password:
        return {"error": "Password is required parameter."}

    try:
        with open('db/exercises.json', 'r', encoding="utf-8") as f:
            EXERCISES_DB = json.load(f)

        db_session.global_init("db/db.db")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == username).first()
        if not user:
            return {"error": "Invalid user."}
        if password != user.password:
            return {"error": "Invalid password."}

        cycle = db_sess.query(Cycle).filter(Cycle.user == username, Cycle.name == cycle_name).first()

        if not cycle:
            return {"error": f"Cycle '{cycle_name}' not found"}
        cycle_data = cycle.data
        if not cycle_data:
            return {"error": f"Data cycle not found"}

        print(cycle_data)

        # РАСЧЕТ ДНЕВНОЙ АНАЛИТИКИ И АНАЛИТИКИ ЗА ТРЕНИРОВКУ
        daily_analytics = {}
        total_analytics = {muscle: 0.0 for muscle in MUSCLE_GROUPS.keys()}
        days_count = len(cycle_data)

        for day_name, day_exercises in cycle_data.items():
            # print(f"Processing {day_name}: {day_exercises}")
            day_load = {muscle: 0.0 for muscle in MUSCLE_GROUPS.keys()}

            for exercise_data in day_exercises:
                exercise_id = str(exercise_data.get("id", ""))
                if not exercise_id:
                    continue
                sets_count = int(exercise_data.get("sets", 3))
                exercise_info = EXERCISES_DB[int(exercise_id)]

                if not exercise_info:
                    print(f"Exercise ID {exercise_id} not found in database")
                    continue
                muscles = exercise_info.get("muscles", {})

                for muscle, pr in muscles.items():
                    try:
                        muscle_pr = float(pr)
                    except (ValueError, TypeError):
                        muscle_pr = 0.0
                    load = sets_count * muscle_pr

                    if muscle in day_load:
                        day_load[muscle] += round(load * (7 / days_count), 2)

                    if muscle in total_analytics:
                        total_analytics[muscle] += round(load * (7 / days_count), 2)

            daily_analytics[day_name] = day_load

        # РАСЧЕТ СРЕДНЕЙ ДНЕВНОЙ АНАЛИТИКИ
        days_count = len(daily_analytics)
        avg_daily = {muscle: 0.0 for muscle in MUSCLE_GROUPS.keys()}

        if days_count > 0:
            for muscle in MUSCLE_GROUPS.keys():
                total = sum(daily_analytics[day][muscle] for day in daily_analytics)
                avg_daily[muscle] = round(total * (7 / days_count), 2)

        # СЧИТАЕМ СКОЛЬКО ПРОЦЕНТОВ ОТ ОПТИМАЛЬНОГО
        optimal_prs = {}

        for muscle_id, load in total_analytics.items():
            muscle_info = MUSCLE_GROUPS.get(muscle_id, {})
            optimal_weekly = muscle_info.get('optimal_weekly', 10)

            if optimal_weekly > 0:
                pr = round((load / optimal_weekly) * 100, 1)
            else:
                pr = 0

            optimal_prs[muscle_id] = pr

        # СТАТУС НАГРУЗКИ
        load_status = {}
        for muscle_id, pr in optimal_prs.items():
            if pr > 130:
                status = "overloaded"
                color = "#ff4444"
            elif pr > 80:
                status = "optimal"
                color = "#44ff44"
            elif pr > 40:
                status = "moderate"
                color = "#ffa500"
            elif pr > 10:
                status = "underloaded"
                color = "#ffff00"
            else:
                status = "untrained"
                color = "#cccccc"

            load_status[muscle_id] = {
                "status": status,
                "color": color,
                "pr": pr
            }

        # 3. РЕКОМЕНДАЦИИ
        recommendations = []

        for muscle_id, data in load_status.items():
            muscle_name = MUSCLE_GROUPS[muscle_id]['name']
            pr = data['pr']
            status = data['status']

            if status == "overloaded":
                rec = f"{muscle_name}: Перегрузка ({pr}%). Снизьте нагрузку."
                priority = "high"
            elif status == "optimal":
                rec = f"{muscle_name}: Оптимально ({pr}%)."
                priority = "low"
            elif status == "moderate":
                rec = f"{muscle_name}: Средняя нагрузка ({pr}%). Можно увеличить."
                priority = "medium"
            elif status == "underloaded":
                rec = f"{muscle_name}: Недогруз ({pr}%). Добавьте упражнения."
                priority = "high"
            else:
                rec = f"{muscle_name}: Не тренируется ({pr}%)."
                priority = "high"

            recommendations.append({
                "message": rec,
                "priority": priority,
                "muscle": muscle_name
            })
        recommendations.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["priority"]])

        # РЕЗУЛЬТАТ
        result = {
            "verdict": "Analytics calculated successfully",
            "cycle_name": cycle_name,
            "days_count": days_count,
            "daily_analytics": daily_analytics,
            "total_analytics": total_analytics,
            "average_daily": avg_daily,
            "optimal_percentages": optimal_prs,
            "load_status": load_status,
            "recommendations": recommendations[:5],
        }

        return result

    except sqlite3.IntegrityError as e:
        print(f"Database error: {e}")
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        print(f"Error in analytics: {e}")
        import traceback
        traceback.print_exc()
        return {"error": f"Calculation error: {str(e)}"}


@app.post("/get_exercises/")
async def exercises(request: Request):
    try:
        with open('db/exercises.json', encoding="utf-8") as f:
            res = json.load(f)
        return res
    except Exception as e:
        print(e)
        return {"error": f"{e}"}


if __name__ == "__main__":
    uvicorn.run(
        "web:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
