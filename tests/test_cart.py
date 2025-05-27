import pytest
import re
from playwright.sync_api import Page, expect

@pytest.fixture
def login():
	pass



# @pytest.fixture
def goto_Home_page(page: Page):
	page.goto('https://demoblaze.com')

def goto_cart_page(page: Page):
	if 'cart.html' in page.url:
		return
	page.get_by_role("link", name="Cart", exact=True).click()
	page.wait_for_timeout(2000)
	assert 'cart.html' in page.url

def alert_info_init():
	alert_info = {"Status": False, "Type": "", "Message": ""}
	return alert_info

def cart_add_dialog_assertion(alert_info:object):
	actual_dialog_type = alert_info["Type"]
	actual_dialog_msg = alert_info["Message"]
	alert_seen = alert_info["Status"]
	assert alert_seen==True, "Product added dialog was not triggered"
	assert actual_dialog_type == "alert", f"Unexpected dialog type:{actual_dialog_type}"
	assert actual_dialog_msg == "Product added", f"Unexpected dialog type:{actual_dialog_type}"

def add_to_cart_action(page:Page,category_name:str, product_name:str):

	goto_Home_page(page)
	alert_info = alert_info_init()
	def dialog_handler(dialog):
		alert_info["Status"]= True
		alert_info["Type"]= dialog.type
		alert_info["Message"] = dialog.message
		dialog.dismiss()

	page.once("dialog", dialog_handler)
	page.get_by_role("link", name=f"{category_name}").click()
	page.get_by_role("link", name=f"{product_name}").click()
	page.get_by_role("link", name="Add to cart").click()
	page.wait_for_timeout(2000)
	return alert_info

def check_cart_page_for_products(page, product_name):
	goto_cart_page(page)
	expect(page.get_by_text(f"{product_name}")).to_be_attached()


def check_cart_total_price(page: Page, product_count:int):
	rows = page.locator("tr.success")
	assert rows.count()==product_count , f"Missmatch product count, actual product count = {product_count}"
	total_price = 0
	for i in range(rows.count()):
		
		cell_price = rows.nth(i).locator("td:nth-child(3)")
		total_price += int(cell_price.inner_text().strip())

		cell_product = rows.nth(i).locator("td:nth-child(2)")
	assert str(total_price)== page.locator("h3#totalp").inner_text(), f"Incorrect total price, actual total price={total_price}"


def delete_from_cart_page(page: Page, product_name:str):
	rows = page.locator("tr.success")
	count_before_deleting = rows.count()
	delete_cell=None
	for i in range(rows.count()):
		cell_product = rows.nth(i).locator("td:nth-child(2)")
		if product_name in cell_product.inner_text().strip():
			delete_cell = rows.nth(i).locator("td:nth-child(4)")
			delete_cell.locator("text=Delete").click()
	page.wait_for_timeout(3000)
	rows = page.locator("tr.success")
	assert rows.count() == count_before_deleting -1, f"Total cart item should be {rows.count()}"

def item_not_found_after_delete_from_cart(page: Page, product_name:str):
	assert not page.is_visible(f"text={product_name}")

def total_price_from_cart(page: Page):
	rows = page.locator("tr.success")
	total_price = 0
	for i in range(rows.count()):
		total_price += int(rows.nth(i).locator("td:nth-child(3)").inner_text().strip())
	return total_price


def get_the_product_price(page: Page,product_category:str,product_name:str):
	goto_Home_page(page)
	page.get_by_role("link", name=f"{product_category}").click()
	page.get_by_role("link", name=f"{product_name}").click()
	page.wait_for_timeout(3000)
	price_str = page.locator('h3.price-container').inner_text().strip()
	price_num = re.search(r'\d+',price_str).group()
	return int(price_num)




# @pytest.mark.skip(reason="temporary")
def test_01_select_category_without_login(page: Page):
	alert_info = add_to_cart_action(page, "Phones", "Nokia lumia")
	cart_add_dialog_assertion(alert_info)
	
	alert_info = add_to_cart_action(page, "Laptops", "Sony vaio i7")
	cart_add_dialog_assertion(alert_info)
	
	alert_info = add_to_cart_action(page, "Monitors", "Apple monitor")
	cart_add_dialog_assertion(alert_info)

	alert_info = add_to_cart_action(page, "Phones", "Nexus 6")
	cart_add_dialog_assertion(alert_info)

	check_cart_page_for_products(page,"Nexus 6")
	check_cart_page_for_products(page,"Apple monitor")
	check_cart_page_for_products(page,"Sony vaio i7")
	check_cart_page_for_products(page,"Nokia lumia")
	
	check_cart_total_price(page,4)


def test_02_delete_and_update_cart_without_login(page: Page):
	add_to_cart_action(page, "Phones", "Nokia lumia")
	add_to_cart_action(page, "Laptops", "Sony vaio i7")
	add_to_cart_action(page, "Monitors", "Apple monitor")

	check_cart_page_for_products(page,"Sony vaio i7")
	check_cart_page_for_products(page,"Nokia lumia")
	check_cart_page_for_products(page,"Apple monitor")

	total_price_before_deleting = total_price_from_cart(page)

	delete_from_cart_page(page,"Sony vaio i7")
	item_not_found_after_delete_from_cart(page,"Sony vaio i7")

	total_price_after_deleting = total_price_from_cart(page)
	price_of_deleting_product = get_the_product_price(page, "Laptops","Sony vaio i7")
	assert total_price_before_deleting-price_of_deleting_product==total_price_after_deleting, "price not updated from cart"


