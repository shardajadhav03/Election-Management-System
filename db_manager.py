from EMS_PACKAGE import log_manager
def create_conn():
    import sqlite3
    ems=sqlite3.connect('Database_for_EMS')
    cur=ems.cursor()
    
    log_manager.update_log("Connected to Database!")

    pragma_status=F"PRAGMA foreign_keys"
    ps=cur.execute(pragma_status)
    fk=ps.fetchall()

    if fk[0][0]==0:
        on=f"PRAGMA foreign_keys = ON"
        cur.execute(on)
        ems.commit()
    return ems,cur