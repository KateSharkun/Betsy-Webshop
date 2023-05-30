import main
import models
import unittest


class PeeweeTestCases(unittest.TestCase):

    def test_user_products(self):
        assert main.list_user_products(2) == ['apple', 'hat']

    def test_search(self):
        assert main.search('p') == ['apple', 'pants']

    def test_list_products_per_tag(self):
        assert main.list_products_per_tag(3) == ['hat']

    def test_update_stock(self):
        main.update_stock(2, 1)
        assert models.Product.get_by_id(2).quantity == 1

    def test_purchase_product(self):
        #would it be better to use fixtures here for function calling and querying?
        main.purchase_product(1, 2, 1)
        query = models.Purchases.select().where(
            models.Purchases.user_id == 2 & models.Purchases.product_id == 1)

        assert [item.user.id for item in query] == [2]

    def test_remove_product(self):
        main.remove_product(1)
        with self.assertRaises(Exception):
            models.Purchases.select().where(models.Product.get_by_id(1))

if __name__ == '__main__':
    unittest.main()