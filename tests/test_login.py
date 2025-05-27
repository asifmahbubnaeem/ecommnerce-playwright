import re
import time
import pytest
from playwright.sync_api import Page, expect, sync_playwright


invalid_user="qwert098"
invalid_passwd="987607"

valid_user="asiftest123"
valid_passwd="test123"


signUp_passwd=""
signUp_userName=""

@pytest.fixture(scope="module")
def signup_credentials():
	return {}

def test_01_login_withInvalid_credentials(page:Page):

	# with sync_playwright() as p:
	# 	browser =  p.chromium.launch(headless=False)
	# 	page =  browser.new_page()

	alert_seen = {"Status": False, "Type": "", "message": ""}
	def dialog_accept(dialog):
		alert_seen["Status"] = True
		alert_seen["Type"] = dialog.type
		alert_seen["message"] = dialog.message		
		dialog.accept()


	page.on("dialog", dialog_accept)
	page.goto('https://demoblaze.com')
	expect(page).to_have_title('STORE')
	page.on("console",lambda msg: print(f"some random text , page title = {page.title()}"))
	page.get_by_role("link", name="Log in").click()
	page.locator("#loginusername").click()
	page.locator("#loginusername").fill(invalid_user)
	page.locator('#loginpassword').fill(invalid_passwd)
	page.get_by_role("button", name="Log in").click()
	page.wait_for_timeout(3000)

	actual_dialog_type = alert_seen["Type"]
	actual_dialog_msg = alert_seen['message']
	assert alert_seen["Status"]==True, "Expected alert dialog was not triggered"
	assert alert_seen["Type"] == "alert", f"Unexpected dialog type:{actual_dialog_type}"
	assert alert_seen["message"] == "User does not exist.", f"Unexpected dialog message:{actual_dialog_msg}"
	page.wait_for_timeout(3000)


def test_02_SignUp(page:Page, signup_credentials):
	signUp_passwd = 'One23Four'
	signUp_userName = 'asifTest_'+str(round(time.time()*1000))

	alert_seen = {"Status": False, "Type": "", "message": ""}
	def dialog_handler(dialog):
		alert_seen["Status"] = True
		alert_seen["Type"] = dialog.type
		alert_seen["message"] = dialog.message
		dialog.accept()


	page.on("dialog", dialog_handler)
	page.goto('https://demoblaze.com')
	page.locator('#signin2').click()
	page.locator("#sign-username").click()
	page.locator("#sign-username").fill(signUp_userName)
	page.locator("#sign-password").click()
	page.locator("#sign-password").fill(signUp_passwd)
	page.get_by_role("button", name="Sign up").click()
	page.wait_for_timeout(3000)

	actual_dialog_type = alert_seen["Type"]
	actual_dialog_msg = alert_seen['message']
	assert alert_seen["Status"]==True, "SingnUp Status Failed, Expected alert dialog was not triggered"
	assert alert_seen["Type"] == "alert", f"SingnUp dialog type failed, Unexpected dialog type:{actual_dialog_type}"
	assert alert_seen["message"] == "Sign up successful.", f"SingnUp dialog message failed,Unexpected dialog message:{actual_dialog_msg}"
	page.wait_for_timeout(3000)

	signup_credentials['username'] = signUp_userName
	signup_credentials['password'] = signUp_passwd



def test_03_login_with_new_credentials(page:Page, signup_credentials):

	username = signup_credentials['username']
	password = signup_credentials['password']
	page.goto('https://demoblaze.com')
	expect(page).to_have_title('STORE')
	page.get_by_role("link", name="Log in").click()
	page.locator("#loginusername").click()
	page.locator("#loginusername").fill(username)
	page.locator('#loginpassword').fill(password)
	
	page.get_by_role("button", name="Log in").click()

	page.wait_for_timeout(3000)
	expect(page.locator('#nameofuser')).to_be_visible()
	expect(page.locator('#nameofuser')).to_contain_text('Welcome '+username)
	


def test_04_login_with_invalid_user(page:Page, signup_credentials):

	alert_seen = {"Status": False, "Type": "", "message": ""}
	def dialog_handler(dialog):
		alert_seen["Status"] = True
		alert_seen["Type"] = dialog.type
		alert_seen["message"] = dialog.message
		page.wait_for_timeout(2000)
		dialog.accept()


	page.on("dialog", dialog_handler)
	page.goto('https://demoblaze.com')
	page.get_by_role("link", name="Log in").click()
	page.locator("#loginusername").click()
	page.locator("#loginusername").fill(signup_credentials['username']+'_new')
	page.locator('#loginpassword').fill(signup_credentials['password'])
	page.get_by_role("button", name="Log in").click()
	page.wait_for_timeout(3000)

	actual_dialog_type = alert_seen["Type"]
	actual_dialog_msg = alert_seen['message']
	assert alert_seen["Status"]==True, "SignIn Status Failed, Expected alert dialog was not triggered"
	assert alert_seen["Type"] == "alert", f"SignIn dialog type failed, Unexpected dialog type:{actual_dialog_type}"
	assert alert_seen["message"] == "User does not exist.", f"SignIn dialog message failed,Unexpected dialog message:{actual_dialog_msg}"
	page.wait_for_timeout(3000)



def test_05_login_with_valid_user_empty_password(page:Page, signup_credentials):

	alert_seen = {"Status": False, "Type": "", "message": ""}
	def dialog_handler(dialog):
		alert_seen["Status"] = True
		alert_seen["Type"] = dialog.type
		alert_seen["message"] = dialog.message
		page.wait_for_timeout(2000)
		dialog.accept()


	page.on("dialog", dialog_handler)
	page.goto('https://demoblaze.com')
	page.get_by_role("link", name="Log in").click()
	page.locator("#loginusername").click()
	page.locator("#loginusername").fill(signup_credentials['username'])
	# page.locator('#loginpassword').fill()
	page.get_by_role("button", name="Log in").click()
	page.wait_for_timeout(3000)

	actual_dialog_type = alert_seen["Type"]
	actual_dialog_msg = alert_seen['message']
	assert alert_seen["Status"]==True, "SignIn Status Failed, Expected alert dialog was not triggered"
	assert alert_seen["Type"] == "alert", f"SignIn dialog type failed, Unexpected dialog type:{actual_dialog_type}"
	assert alert_seen["message"] == "Please fill out Username and Password.", f"SignIn dialog message failed,Unexpected dialog message:{actual_dialog_msg}"
	page.wait_for_timeout(3000)


def test_06_login_with_valid_user_empty_password(page:Page, signup_credentials):

	alert_seen = {"Status": False, "Type": "", "message": ""}
	def dialog_handler(dialog):
		alert_seen["Status"] = True
		alert_seen["Type"] = dialog.type
		alert_seen["message"] = dialog.message
		page.wait_for_timeout(2000)
		dialog.accept()


	page.on("dialog", dialog_handler)
	page.goto('https://demoblaze.com')
	page.get_by_role("link", name="Log in").click()
	page.locator("#loginusername").click()
	# page.locator("#loginusername").fill(signup_credentials['username']+'_new')
	page.locator('#loginpassword').fill(signup_credentials['password'])
	page.get_by_role("button", name="Log in").click()
	page.wait_for_timeout(3000)

	actual_dialog_type = alert_seen["Type"]
	actual_dialog_msg = alert_seen['message']
	assert alert_seen["Status"]==True, "SignIn Status Failed, Expected alert dialog was not triggered"
	assert alert_seen["Type"] == "alert", f"SignIn dialog type failed, Unexpected dialog type:{actual_dialog_type}"
	assert alert_seen["message"] == "Please fill out Username and Password.", f"SignIn dialog message failed,Unexpected dialog message:{actual_dialog_msg}"
	page.wait_for_timeout(3000)


def test_07_login_with_valid_user_invalid_password(page:Page, signup_credentials):

	alert_seen = {"Status": False, "Type": "", "message": ""}
	def dialog_handler(dialog):
		alert_seen["Status"] = True
		alert_seen["Type"] = dialog.type
		alert_seen["message"] = dialog.message
		page.wait_for_timeout(2000)
		dialog.accept()


	page.on("dialog", dialog_handler)
	page.goto('https://demoblaze.com')
	page.get_by_role("link", name="Log in").click()
	page.locator("#loginusername").click()
	page.locator("#loginusername").fill(signup_credentials['username'])
	page.locator('#loginpassword').fill(signup_credentials['password']+'0')
	page.get_by_role("button", name="Log in").click()
	page.wait_for_timeout(3000)

	actual_dialog_type = alert_seen["Type"]
	actual_dialog_msg = alert_seen['message']
	assert alert_seen["Status"]==True, "SignIn Status Failed, Expected alert dialog was not triggered"
	assert alert_seen["Type"] == "alert", f"SignIn dialog type failed, Unexpected dialog type:{actual_dialog_type}"
	assert alert_seen["message"] == "Wrong password.", f"SignIn dialog message failed,Unexpected dialog message:{actual_dialog_msg}"
	page.wait_for_timeout(3000)


def test_08_login_with_invalid_user_valid_password(page:Page, signup_credentials):

	alert_seen = {"Status": False, "Type": "", "message": ""}
	def dialog_handler(dialog):
		alert_seen["Status"] = True
		alert_seen["Type"] = dialog.type
		alert_seen["message"] = dialog.message
		page.wait_for_timeout(2000)
		dialog.accept()


	page.on("dialog", dialog_handler)
	page.goto('https://demoblaze.com')
	page.get_by_role("link", name="Log in").click()
	page.locator("#loginusername").click()
	page.locator("#loginusername").fill(signup_credentials['username']+'_edit')
	page.locator('#loginpassword').fill(signup_credentials['password'])
	page.get_by_role("button", name="Log in").click()
	page.wait_for_timeout(3000)

	actual_dialog_type = alert_seen["Type"]
	actual_dialog_msg = alert_seen['message']
	assert alert_seen["Status"]==True, "SignIn Status Failed, Expected alert dialog was not triggered"
	assert alert_seen["Type"] == "alert", f"SignIn dialog type failed, Unexpected dialog type:{actual_dialog_type}"
	assert alert_seen["message"] == "User does not exist.", f"SignIn dialog message failed,Unexpected dialog message:{actual_dialog_msg}"
	page.wait_for_timeout(3000)


def test_09_logout(page: Page, signup_credentials):

	username = signup_credentials['username']

	page.goto('https://demoblaze.com')
	page.get_by_role("link", name="Log in").click()
	page.locator("#loginusername").click()
	page.locator("#loginusername").fill(signup_credentials['username'])
	page.locator('#loginpassword').fill(signup_credentials['password'])
	page.get_by_role("button", name="Log in").click()
	page.wait_for_timeout(3000)

	expect(page.locator('#nameofuser')).to_be_visible()
	expect(page.locator('#nameofuser')).to_contain_text('Welcome '+username)

	page.locator('#logout2').click()
	page.wait_for_selector(f"text=Welcome {username}", state="detached")
	assert not page.is_visible(f"text=Welcome {username}")
	page.wait_for_timeout(2000)

