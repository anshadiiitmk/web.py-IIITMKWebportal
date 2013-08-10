#!/usr/bin/env python
"""A simple Web Portal for IIITMK Friends"""

import web
import sys
import Image
import model  	#db functions defined module
import datetime

### Url mappings

urls = ('/' ,'IIITMKIndex',
'/register', 'Register',
'/myHomePage', 'Home',
'/editProfile','EditProfile',
'/viewDiscussionBoard' ,'DiscussionBoard',
'/viewDiscussions' ,'Discussions',
'/postDiscussion' ,'NewDiscussion',
'/viewNews&Events','NewsandEvents',
'/viewMessageBox','Message',
'/composeMessage','compose',
'/viewSentMessages','Sent',
'/viewMembers','Member',
'/listFriends','Friends',
'/viewOpinionPolls','ViewPoll',
'/createPoll','NewOpinionPoll',
'/viewsinglepoll/(\d+)','Viewsinglepoll',

'/adminLogin','Admin',

'/login', 'Login',
 '/logout', 'Logout',

)

### Templates

render=web.template.render('templates/')




try:
	db=web.database(dbn="sqlite",db="IIITMK.db")
except: 
	print "Could not connect to database"
	sys.exit()

class IIITMKIndex:
	def GET(self):
		return render.loginScreen()
	def POST(self):

		
		inp=web.input()
		users=db.select('IIITMKLogin')
		for user in users:
			if(inp.username==user.username and inp.passwordbox==user.password):
				
				return render.myHomePage(inp.username)

			else:
				return render.unAuthorised(name=inp.username)

	

class Register:

	
	def GET(self):
		inp=web.input()
		param=""
       		return render.createProfile(param)

	def POST(self):

		i = web.input()
    		if i.form_action == 'Upload':
         		#Image Upload
			try:
				x = web.input(profile_pic_file={})
				filedir='./static/profilepics' 	#/path/where/you/want/to/save image
				if 'profile_pic_file' in x:
					filepath=x.profile_pic_file.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
					filename=filepath.split('/')[-1] # splits the / and chooses the last part (the filename with extension)
					fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
					fout.write(x.profile_pic_file.file.read()) # writes the uploaded file to the newly created file.
					fout.close() # closes the file, upload complete.

					infile = filedir +'/'+filename
					outfile = infile + ".thumbnail"
					im = Image.open(filedir +'/'+filename)
					im.thumbnail((120, 120))
					im.save(outfile, im.format)
				return render.createProfile(outfile)
			except:
				print "Could not upload image;Unexpected error:", sys.exc_info()[0]
				sys.exit()
	
    		else:
         # Do submit button action
			inp=web.input()
			inp.profilepic=""
			toLoginTable=db.insert('IIITMKLogin',username=inp.username, password=inp.password,account_type=inp.acc_type);
			toUserdetailsTable=db.insert('UserDetails',username=inp.username,fullname=inp.fullname,email=inp.email,account_type=inp.acc_type,designation=inp.designation,age=inp.age,batch=inp.batch,profilepic=inp.profilepic)
			return render.myHomePage(inp.username)



class EditProfile:
	def GET(self):
		inp=web.input();
		username=inp.username
		
		user=db.query("select * from UserDetails where username=$username",vars={'username',username})
		db.commit()

		row=user
		inp.username=row["username"]
		inp.fullname=row["fullname"]
		inp.email=row["email"]
		inp.batch=row["batch"]
		inp.designation=row["designation"]


		return render.editProfile(inp.username)
	def POST(self):
		inp=web.input()

class Admin:
	def GET(self):
		return render.adminLogin()
	def POST(self):
		admin=model.getAdmin(1)
		admin=db.select('IIITMKLogin')
		for user in users:
			if(inp.username==user.username and inp.passwordbox==user.password):
				
				return render.myHomePage(inp.username)

			else:
				return render.unAuthorised(name=inp.username)




class Home:
	def GET(self):
		return render.myHomePage()
	def POST(self):
		inp=web.input()
		#check if item=1 or 2 or 3



class NewOpinionPoll:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,size=30,description="Post title:"),
        web.form.Textarea('content', web.form.notnull, rows=10, cols=80,description="Post content:"),
        web.form.Button('Post entry'),)

    def GET(self):
        form = self.form()
        return render.createPoll(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.createPoll(form)
	model.new_post(form.d.title,form.d.content);
	raise web.seeother('/createPoll')

class ViewPoll:
	def GET(self):
		"""view opinion polls"""
		posts=model.get_posts()
		return render.viewOpinionPolls(posts)

class Viewsinglepoll:
	def GET(self,id):
		""" View single post """
		post = model.get_post(int(id))
		return render.viewSinglePoll(post)

class DiscussionBoard:
	def GET(self):
		return render.viewDiscussionBoard()
	def POST(self):
		inp=web.input()
		#if(inp.input.name=="add_disc"):
			#raise web.seeother('/')
		return render.postDiscussion()
		#else:
			#return render.comment()

class Discussions:
	def GET(self):
		return render.viewDiscussions()
class NewDiscussion:
	def GET(self):
		return render.postDiscussion()
class NewsandEvents:
	def GET(self):
		return render.viewNewsandEvents()
class Message:
	def GET(self):
		return render.viewMessageBox()
class compose:
	def GET(self):
		return render.composeMessage()
class Sent:
	def GET(self):
		return render.viewSentMessages()
class Member:
	def GET(self):
		return render.viewMembers()
class Friends:
	def GET(self):
		return render.listFriends()
class Poll:
	def GET(self):
		return render.listOpinionPolls()

	
if __name__=='__main__':
	app=web.application(urls,globals())
	app.run()
