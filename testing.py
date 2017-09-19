from app import db,Users,LeaveDetail
from sqlalchemy import text
leave = Users.query.filter_by(id=1).first()

results = db.engine.execute(text("select username,sdate,edate,days from users join leavedetail on users.id = "
                                 "leavedetail.usr_id where users.id = {}".format(1)))

for d in results:
    print '{}#{}#{}'.format(d[1].split()[0],d[2].split()[0],d[3])
    #print d