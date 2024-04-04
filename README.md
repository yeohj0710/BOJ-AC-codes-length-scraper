# BOJ-AC-codes-length-scraper

### [Caution] Baekjoon Online Judge strictly prohibits web scraping, and excessive traffic may result in site access being suspended.

### This scraper has a DELAY_PER_PAGE value of 10 seconds to minimize the impact on the site's traffic, and the program was developed only as an exercise in scraper development and is not actually used.

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
   <b>user_id</b>: The user's BOJ id. When searching, we will search among the problems that the user hasn't solved yet.<br>
   <b>min_difficulty</b>: The lower bound of the problem tier to search for. Write it as a string, like 'b3'.<br>
   <b>max_difficulty</b>: The upper limit of the problem tier to search. Write it as a string, like 's3'.<br>
   <b>min_solvers_count</b>: Lower bound for the number of people who solved the problem.<br>
   <b>max_solvers_count</b>: Upper limit for the number of people who solved the problem.<br>
   <b>min_average_try</b>: The lower bound for the average number of attempts by people who solved the problem.<br>
   <b>max_average_try</b>: The upper bound for the average number of attempts by people who solved the problem.<br>
   <b>language_cpp</b>: If set to True, only solutions from people who solved in C++ will be counted.<br>

2. If there are any other issues you want to exclude from the search, add them to the 'excluded-problems-list', one per line.<br>

3. Run 'boj-ac-codes-length-scraper.py'.<br>

4. The questions are saved in the '검색*결과*데이터.csv' file, which you can sort by each column to see the questions that were found.<br>

<br>

### Features of the program

This scraper adds each question to a CSV file as soon as it is scraped, so even if the program crashes in the middle of a scrape, the data from questions retrieved before the crash will all be saved in the CSV file.

<br>
<br>
