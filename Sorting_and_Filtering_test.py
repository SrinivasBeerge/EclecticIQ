import unittest
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from access_page_elements import AccessPageElements


class VerifySortingFilterOptions(unittest.TestCase):
    """
    Author: Srinivas Beerge
    Purpose: Class inherits from the unittest framework to test single scenario tests
    The business logic function are maintained in a seperate file to make it organized and maintainable
    """
    base_url = "https://mystifying-beaver-ee03b5.netlify.app/"
    access_page_ele_obj = AccessPageElements()

    def setUp(self) -> None:
        """Function to create a driver, get the elements from the base_url
            assert: None
            """
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("chrome://settings/clearBrowsingData")
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        # Separate try;except block since we do not have exception message upon element not found
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.NAME, "sort-select")))

    def test_verify_title(self):
        """Function to test the title of the base_url
            assert True: when the title matches
            """
        driver = self.driver
        page_title_hardcode = "simplesite"
        page_title = driver.title
        self.assert_(page_title == page_title_hardcode, "Verify title test")

    def test_sort_by_option(self):
        """Function to test all the sort options. loop and self.subTest used to test all sort options
            assert True: when the table content collected from UI is equal to table content sorted using code
            """
        ui_generated_matrix_by_opt = []
        user_generated_matrix_by_opt = []
        driver = self.driver
        # change the variable name to table_content_by_name_sort
        # non_sorted_table_content = self.access_page_ele_obj.get_table_content(driver)
        # table_content_by_name = self.access_page_ele_obj.gen_default_table_matrix(driver)
        sort_options = self.access_page_ele_obj.get_sort_selector(driver)
        for option in sort_options[:-1]:
            with self.subTest(opt=option):
                ui_generated_matrix_by_opt = self.access_page_ele_obj.ui_table_matrix_by_sort_opt(option, driver)
                user_generated_matrix_by_opt = self.access_page_ele_obj.modify_matrix_by_sort_opt(option, driver)
                print ("-------", ui_generated_matrix_by_opt, "\n", user_generated_matrix_by_opt)
                self.assertEqual(ui_generated_matrix_by_opt, user_generated_matrix_by_opt, "Verify sort by option")

    def test_result_based_filter(self):
        """Function to test filter field where the result has entries
            assert True: when the table content collected from UI is equal to table content sorted using code
            """
        driver = self.driver
        filter_count = 0
        filter_key = "hi"
        # test_filters = {
        #     "for_positive_scenario": "hi",
        #     "for_negative_scenario": "apple$%apple"
        # }
        table_data_list = self.access_page_ele_obj.filter_test_data(driver, filter_key)
        non_sorted_data = self.access_page_ele_obj.gen_default_table_matrix(driver)
        num_of_sort_opts = len(self.access_page_ele_obj.get_sort_selector(driver))
        for lis in non_sorted_data:
            # print(lis)
            if filter_key in lis[0] or filter_key in lis[-1]:
                filter_count += 1
        self.assert_(((len(table_data_list) // num_of_sort_opts) == filter_count), "Test filter Positive scenario")

    def test_no_result_filter(self):
        """Function to test filter field where the result has NO entries / Null
            assert True: when the table content collected from UI is equal to table content sorted using code
            """
        driver = self.driver
        filter_count = 0
        filter_key = "apple$%apple"
        # test_filters = {
        #     "for_positive_scenario": "hi",
        #     "for_negative_scenario": "apple$%apple"
        # }
        table_data_list = self.access_page_ele_obj.filter_test_data(driver, filter_key)
        non_sorted_data = self.access_page_ele_obj.gen_default_table_matrix(driver)
        print ("this is non sorted data", non_sorted_data)
        num_of_sort_opts = len(self.access_page_ele_obj.get_sort_selector(driver))
        for lis in non_sorted_data:
            # print(lis)
            if filter_key in lis[0] or filter_key in lis[-1]:
                filter_count += 1
        self.assert_(((len(table_data_list) // num_of_sort_opts) == filter_count), "Test filter Positive scenario")

    def tearDown(self) -> None:
        self.driver.quit()


if __name__ == "__main__":
    """
    code to generate various types of reports can be used here
    """
    unittest.main()
