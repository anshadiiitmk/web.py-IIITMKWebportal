import web, datetime

db=web.database(dbn="sqlite",db="IIITMK.db")

def get_posts():
    return db.select('OpinionPoll', order='id DESC')

def get_post(id):
    try:
        return db.select('OpinionPoll', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def new_post(title, text):
    db.insert('OpinionPoll', topic=title, content=text, posted_on=datetime.datetime.utcnow())

def del_post(id):
    db.delete('OpinionPoll', where="id=$id", vars=locals())

def update_post(id, title, text):
    db.update('OpinionPoll', where="id=$id", vars=locals(),
        topic=title, content=text)

def getAdmin(id):
  try:
		db.select("IIITMKLogin",where='account_type=$id',vars=locals())[0]
	except IndexError:
		return None
		
