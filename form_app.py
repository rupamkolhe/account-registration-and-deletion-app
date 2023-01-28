
from deta import Deta 
import streamlit as st 

projectName = 'your_project_name'
projectKey = 'your_project_key'

deta = Deta(projectKey)
db = deta.Base('simpleDB')

def create_user(data):
	if db.put(data):
		return True
	return False

def checkUser(data):
	item = db.fetch().items
	keys = ['birth_date','gender','key','username']
	if item :
		for i in item:
			row = True
			for key in keys:
				row *= (data[key] == i[key])
			if row :
				return True
		return False
	return False
def deleteUser(data):
	item = db.fetch().items
	keys = ['key','username']
	if item :
		for i in item:
			row = True
			for key in keys:
				row *= (data[key] == i[key])
			if row :
				return True
		return False
	return False
if 'userResponse' not in st.session_state:
	st.session_state.userResponse = {}
if 'imageState' not in st.session_state:
	st.session_state.imageState = ''

if st.session_state.userResponse:
	if checkUser(st.session_state.userResponse):
		if not st.session_state.imageState:
			st.image('fir_agaya.jpg')
			st.success('Account is already Registered !')
		else :
			st.image(st.session_state.imageState)
		form = st.form('delete_form')
		user = form.text_input('Enter Name')
		password = form.text_input('Enter password',type='password')
		acc = {'username':user,'key':password+user}
		if form.form_submit_button('Delete Account'):
			if deleteUser(acc):
				db.delete(acc['key'])
				st.session_state.userResponse = {}
				st.session_state.imageState = ''
				st.experimental_rerun()
			else:
				st.session_state.imageState = 'kya_kr_rha_hai.jpg'
				st.experimental_rerun()
	else:
		status = create_user(st.session_state.userResponse)
		if status:
			st.success('successfully Registered !')
		else :
			st.warning('something went wrong !')
			if st.button('Register Again'):
				st.session_state.userResponse = {}
				st.experimental_rerun()


if not st.session_state.userResponse:
	form = st.form('my_form')
	user = form.text_input('Enter Name')
	gender = form.radio('Gender',options=('Male','Female'))
	birth_date = form.date_input('Enter Birth Date',value=None)
	password = form.text_input('Enter password',type='password')
	if form.form_submit_button('Submit'):
		st.session_state.userResponse = {'username':user,
						'gender':gender,
						'birth_date':birth_date.strftime('%Y/%m/%d'),
						'key':password+user}
		st.experimental_rerun()
