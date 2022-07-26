from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


class AccessPageElements:
    """
    Author: Srinivas Beerge
    Purpose: The class is intended to have all the class object calls at one place
    """

    def get_sort_selector(self, driver):
        """Function to get all the sort options
            argument/s: driver object
            return: a list of sort elements
            """
        sorting_options = []
        sorting_dropdown = driver.find_element(By.NAME, "sort-select")
        sorting_options_attr = [x for x in sorting_dropdown.find_elements(By.TAG_NAME, "option")]
        for element in sorting_options_attr:
            sorting_options.append(element.get_attribute("value"))
        return sorting_options

    def get_table_content(self, driver, sort_option=None):
        """Function to convert formatting k=*1000, M=*1000000, B=*1000000000
            argument/s: driver object, option to sort
                if sort_option = None: get default table content
                if sort_option = option: get option specific table content
            return: a list
            """
        formatted_table_data_list = []
        # To find the content of table
        if not sort_option:
            raw_table_data = driver.find_element(By.CLASS_NAME, "table-content")
        else:
            table_data = Select(driver.find_element(By.NAME, "sort-select")).select_by_value('%s' % sort_option)
            raw_table_data = driver.find_element(By.CLASS_NAME, "table-content")
        raw_table_data_list = raw_table_data.text.split("\n")
        if len(raw_table_data_list)>=4:
            for ele in raw_table_data_list:
                if ele[0].isdigit() and (ele[-1] == "k"):
                    int_element = float(ele.strip("k")) * 1000
                    formatted_table_data_list.append(int_element)
                elif ele[0].isdigit() and (ele[-1] == "M"):
                    int_element = float(ele.strip("M")) * 1000000
                    formatted_table_data_list.append(int_element)
                elif ele[0].isdigit() and (ele[-1] == "B"):
                    int_element = float(ele.strip("B")) * 1000000000
                    formatted_table_data_list.append(int_element)
                elif ele[0].isdigit() and ele[-1].isdigit():
                    formatted_table_data_list.append(float(ele))
                else:
                    # these assignments help to sort from low to high
                    if ele == "low":
                        formatted_table_data_list.append("Low")
                    elif ele == "medium":
                        formatted_table_data_list.append("Med")
                    else:
                        formatted_table_data_list.append(ele.lower())
        return formatted_table_data_list

    def gen_default_table_matrix(self, driver):
        """Function to get a default table content to compare with UI table content
            argument/s: driver object
            sorting option 'name' considered as default
            return: a list of 'num_of_options x num_of_options' matrix
            """
        # print ("inside gen_default_table_matrix")
        table_content_nxn_matrix = []
        num_of_sort_options = len(self.get_sort_selector(driver))
        table_content_list = self.get_table_content(driver)
        # Below computation is to create a list containing all the row
        for i in range(0, len(table_content_list), num_of_sort_options):
            table_content_nxn_matrix.append(table_content_list[i:i + num_of_sort_options])
        # print("This is the test_list", table_content_nxn_matrix)
        # sort by names and we consider that as a default data
        sorted_list_by_name = sorted(table_content_nxn_matrix, key=lambda x: x[0])
        return sorted_list_by_name

    def ui_table_matrix_by_sort_opt(self, sort_option, driver):
        """Function to get UI table content depending on sort option
            argument/s: sort option, driver object
            return: a list of 'options x options' matrix
            """
        # print ("inside ui_table_matrix_by_sort_opt")
        opt_sorted_table_content_matrix = []
        num_of_sort_options = len(self.get_sort_selector(driver))
        table_content_list = self.get_table_content(driver, sort_option='%s' % sort_option)
        # Below computation is to create a list containing all the row
        for i in range(0, len(table_content_list), num_of_sort_options):
            opt_sorted_table_content_matrix.append(table_content_list[i:i + num_of_sort_options])
        return opt_sorted_table_content_matrix

    def modify_matrix_by_sort_opt(self, sort_option, driver):
        """Function to sort the default table content created in the function gen_default_table_matrix
            to a option sorted one to compare with UI table content.
            argument/s: sort option, driver object
            return: a list of 'num_of_options x num_of_options' matrix
            """
        # print ("inside modify_matrix_by_sort_opt")
        default_list_sorted_by_option = []
        all_sort_options = self.get_sort_selector(driver)
        # print ("all_sort_options", all_sort_options)
        for index in range(len(all_sort_options)):
            if all_sort_options[index] == sort_option:
                sorted_list_by_name = self.gen_default_table_matrix(driver)
                default_list_sorted_by_option = sorted(sorted_list_by_name, key=lambda x: x[index])
        # print("default_list_sorted_by_options", default_list_sorted_by_option)
        return default_list_sorted_by_option

    def filter_test_data(self, driver, filter_key):
        """Function to get the table content depending on the 'filter key'
            argument/s: driver object, filter key
            return: list containing nxm matrix
            """
        filter_count = 0
        filter_key = filter_key
        try:
            driver.find_element(By.XPATH, '//*[@id="filter-input"]').clear()
            driver.find_element(By.XPATH, '//*[@id="filter-input"]').send_keys(filter_key)
            table_data = driver.find_element(By.CLASS_NAME, "table-content")
            table_data_list = table_data.text.split("\n")
            # print(table_data_list)
            return table_data_list
        except Exception as e:
            print("element not found", e)