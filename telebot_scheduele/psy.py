import datetime

import psycopg2
import datetime


def rasp_day(day):
    conn = psycopg2.connect(database="sch_db",
                            user="postgres",
                            password="admin",
                            host="localhost",
                            port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sch.timetable WHERE day = '%s' AND week = '%s' OR day = '%s' AND week = 'all' ORDER "
                   "BY id" % (str(day), week(), str(day)))
    records = list(cursor.fetchall())
    records = [list(x) for x in records]
    for i in range(len(records)):
        cursor.execute("SELECT full_name FROM sch.teacher WHERE subject = '%s'" % str(records[i][2]))
        records[i].append(cursor.fetchall()[0][0])
    table = ('%s\n_________________________\n' % day)
    conn.commit()
    if records:
        for i in range(len(records)):
            # table += ('%s | %s | %s\n' % (records[i][4], records[i][2], records[i][3])) на случай выхода на очное
            table += ('%s | Дист. | %s | %s\n' % (records[i][4], records[i][2], records[i][-1]))
        table += '_________________________\n'
        return table
    else:
        table += 'Отдыхаем\n'
        table += '_________________________\n'
        return table


def rasp_week(week_choose):
    conn = psycopg2.connect(database="sch_db",
                            user="postgres",
                            password="admin",
                            host="localhost",
                            port="5432")
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
    table = ''
    if week() == 'up':
        rev_week = 'down'
    else:
        rev_week = 'up'
    if week_choose == 'current':
        for i in range(len(days)):
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM sch.timetable WHERE day = '%s' AND week = '%s' OR day = '%s' AND week = 'all' ORDER "
                "BY id" % (str(days[i]), week(), str(days[i])))
            records = list(cursor.fetchall())
            records = [list(x) for x in records]
            for j in range(len(records)):
                cursor.execute("SELECT full_name FROM sch.teacher WHERE subject = '%s'" % str(records[j][2]))
                records[j].append(cursor.fetchall()[0][0])
                conn.commit()
            table += ('%s\n_________________________\n' % days[i])
            if records:
                for f in range(len(records)):
                    # table += ('%s | %s | %s\n' % (records[f][4], records[f][2], records[f][3])) на случай выхода на
                    # очное
                    table += ('%s | Дист. | %s | %s\n' % (records[f][4], records[f][2], records[f][-1]))
                table += '_________________________\n\n'
            else:
                table += 'Отдыхаем\n'
                table += '_________________________\n\n'
        return table
    elif week_choose == 'next':
        for i in range(len(days)):
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM sch.timetable WHERE day = '%s' AND week = '%s' OR day = '%s' AND week = 'all' ORDER "
                "BY id" % (str(days[i]), rev_week, str(days[i])))
            records = list(cursor.fetchall())
            records = [list(x) for x in records]
            for j in range(len(records)):
                cursor.execute("SELECT full_name FROM sch.teacher WHERE subject = '%s'" % str(records[j][2]))
                records[j].append(cursor.fetchall()[0][0])
                conn.commit()
            table += ('%s\n_________________________\n' % days[i])
            if records:
                for f in range(len(records)):
                    # table += ('%s | %s | %s\n' % (records[f][4], records[f][2], records[f][3])) на случай выхода на
                    # очное
                    table += ('%s | Дист. | %s | %s\n' % (records[f][4], records[f][2], records[f][-1]))
                table += '_________________________\n\n'
            else:
                table += 'Отдыхаем\n'
                table += '_________________________\n\n'
        return table


def week():
    d1 = datetime.date(2021, 11, 22)
    d2 = datetime.date.today()
    result = (d2 - d1).days // 7
    if result % 2 == 0:
        result = 'up'
    else:
        result = 'down'
    return result
