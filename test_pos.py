import os
import pos


def setup_module(module):
    if os.path.exists(pos.DB_NAME):
        os.remove(pos.DB_NAME)
    pos.create_tables()


def teardown_module(module):
    if os.path.exists(pos.DB_NAME):
        os.remove(pos.DB_NAME)


def test_add_product_and_list():
    pos.add_product("Apple", 0.5)
    products = pos.list_products()
    assert len(products) == 1
    assert products[0][1] == "Apple"
    assert products[0][2] == 0.5


def test_record_sale_and_list():
    # product id 1 should exist from previous test
    pos.record_sale(1, 2)
    sales = pos.list_sales()
    assert len(sales) == 1
    sale = sales[0]
    assert sale[1] == "Apple"
    assert sale[2] == 2
