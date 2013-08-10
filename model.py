import web, datetime,sys

try:
	db=web.database(dbn="sqlite",db="IIITMK.db")
except: 
	print "Could not connect to database"
	sys.exit()

def getUsers():
	 return db.select('IIITMKLogin', order='id DESC')

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
    db.update('OpinionPoll', where="id=$id", vars=locals(),topic=title, content=text)

def getAdminDetails(id):
	try:
		
		return db.select('IIITMKLogin',what='username,password',where='account_type=$id')
		
	except IndexError:
		return None

def get_UserDetails(username):
	return db.select('IIITMKLogin',where='username=$username')


def get_Requests():
	return db.select('UserDetails',vars=locals(),where='valid=0')


def approveUser(id):
	try:
		db.update('UserDetails',where="id=$id",vars=locals(),valid=1)
	except IndexError:
		return None

def rejectUser(id):
	try:
		db.update('UserDetails',where="id=$id",vars=locals(),valid=0)
	except IndexError:
		return None













		
