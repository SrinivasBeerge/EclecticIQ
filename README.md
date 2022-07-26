EclecticIQ - Test the website and its options

Description: The project is intended to test the website and its elements.

Problem statement: 
The website has two major functionality to test:
	Filter: To filter the elements in the table.
	Sort: A dropdown containing options to sort the table.

Solution:
Selenium with python flavor is used to test all the web elements.
Unittest framework is used to verify the small scenarios that must be checked for correctness.

How to use:
- Install all the required packages using the requirement.txt.
- The project contain two python files
	1. access_page_elements.py : containing functions to access the page objects and a few other functions to compute the business logic.
	2. Sorting_and_Filtering.py : This is the start point of the testing. Running this file will run all the tests and print the result in the console.
