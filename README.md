# BOJ-AC-codes-length-scraper

### [Caution] Baekjoon Online Judge strictly prohibits web scraping, and excessive traffic may result in site access being suspended.

### This scraper has a DELAY_PER_PAGE value of 10 seconds to minimize the impact on the site's traffic, and <font color="red">this program was developed only as an exercise in scraper development and is not actually used</font>.

<br>

### Brief introduction

A scraper to calculate the length of each 'problem description' and the 'average length of the AC codes' for problems on Baekjoon Online Judge

<br>

### Purpose of the program

How can I find easy questions on the BOJ?<br>
If you can sort questions by the average length of the answer codes or the length of the problem description, you can quickly find easy questions.<br>
BOJ and solved.ac have a variety of sorting criteria for questions, but you can't sort by "average length of answer codes" or "length of problem description".<br>
So we built this scraper to allow you to search for problems by adding these criteria.<br>

<br>

### How to use

1. Set the variables on lines 8-15 of the 'boj-ac-codes-length-scraper.py' file accordingly.<br>

<div align="center">

![image](https://github.com/yeohj0710/BOJ-AC-codes-length-scraper/assets/93759367/25674c92-195d-41b6-be8b-788d2a42af6f)<br>

</div>

   <b>user_id</b>: The user's BOJ id. When searching, we will search among the problems that the user hasn't solved yet.<br>
   <b>min_difficulty</b>: The lower bound of the problem tier to search for. Write it as a string, like 'b3'.<br>
   <b>max_difficulty</b>: The upper limit of the problem tier to search. Write it as a string, like 's3'.<br>
   <b>min_solvers_count</b>: Lower bound for the number of people who solved the problem.<br>
   <b>max_solvers_count</b>: Upper limit for the number of people who solved the problem.<br>
   <b>min_average_try</b>: The lower bound for the average number of attempts by people who solved the problem.<br>
   <b>max_average_try</b>: The upper bound for the average number of attempts by people who solved the problem.<br>
   <b>language_cpp</b>: If set to True, only solutions from people who solved in C++ will be counted.<br>

<br>

2. If there are any other issues you want to exclude from the search, add them to the 'excluded-problems-list', one per line.<br>

<div align="center">

![image](https://github.com/yeohj0710/BOJ-AC-codes-length-scraper/assets/93759367/505b723f-db2a-4889-8913-6fa969170109)

</div>

<br>

3. Run 'boj-ac-codes-length-scraper.py'.<br>

<br>

4. The questions are saved in the '검색_결과_데이터.csv' file, which you can sort by each column to see the questions that were found.<br>

<div align="center">

![image](https://github.com/yeohj0710/BOJ-AC-codes-length-scraper/assets/93759367/0258cfcf-2e45-40d3-b193-3bcb45a2aa89)

</div>

<br>

### Features of the program

- This scraper adds each question to a CSV file as soon as it is scraped, so even if the program crashes in the middle of a scrape, the data from questions retrieved before the crash will all be saved in the CSV file.
- Before the program adds data to the CSV file, questions that are excluded from new search results are automatically deleted from the CSV file.
- Valid problem data already in the CSV file will not be deleted, only the new data will be added to the CSV file.
- Only the retrieved problem data that does not already exist in the CSV file will be added to the CSV file in a randomized order, so you can avoid having certain problem IDs being added to the CSV file in droves.

<br>
<br>
