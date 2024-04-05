import requests
from bs4 import BeautifulSoup
import time
from random import shuffle
import os
import csv

user_id = "baekjoon"
min_difficulty = "b3"
max_difficulty = "g4"
min_solvers_count = 50000
max_solvers_count = 1000000
min_average_try = 1
max_average_try = 1.8
language_cpp = True

DELAY_PER_PAGE = 10
FILE_NAME = "검색_결과_데이터.csv"
EARLY_TERMINATION_FLAG = True
PAGES_TO_SCRAPE_PER_RUN = 10

excluded_problem_ids = []


def get_total_pages(solved_ac_url):
    response = requests.get(solved_ac_url)

    soup = BeautifulSoup(response.content, "html.parser")

    total_pages = int(soup.find("div", class_="css-18lc7iz").find_all("a")[-1].text)

    return total_pages


def scrape_problem_solved_ac_infos(solved_ac_each_page_url):
    response = requests.get(solved_ac_each_page_url)

    soup = BeautifulSoup(response.content, "html.parser")

    problems = soup.find_all("tr", class_="css-1ojb0xa")[1:]

    each_page_problems_solved_ac_infos = {}

    for problem in problems:
        anchors = problem.find_all("a", class_="css-q9j30p")

        problem_id = anchors[0].text
        problem_tier = anchors[0].find("img")["alt"]
        problem_title = anchors[1].find("span", class_="__Latex__").text

        divs = problem.find_all("div", class_="css-1ujcjo0")

        problem_solvers_count = divs[0].text
        problem_average_try = divs[1].text

        each_page_problems_solved_ac_infos[problem_id] = {
            "problem_tier": problem_tier,
            "problem_title": problem_title,
            "problem_solvers_count": problem_solvers_count,
            "problem_average_try": problem_average_try,
        }

    return each_page_problems_solved_ac_infos


def get_problem_solved_ac_infos(solved_ac_url, total_pages):
    problems_info = {}

    for i in range(total_pages):
        solved_ac_each_page_url = solved_ac_url + f"&page={i+1}"
        problems_info.update(scrape_problem_solved_ac_infos(solved_ac_each_page_url))

        print(f"solved.ac 페이지 스크랩 중... ({i + 1}/{total_pages})")
        time.sleep(DELAY_PER_PAGE)

    return problems_info


def check_file_header_exists_or_create():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", encoding="utf-8"):
            pass

    header_exists = True

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        first_row = next(reader, None)

        if not first_row:
            header_exists = False

    if header_exists:
        return

    with open(FILE_NAME, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "문제 번호",
            "제목",
            "난이도",
            "푼 사람 수",
            "평균 시도",
            "정답 코드의 평균 길이",
            "문제 본문 길이",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    return


def remove_excluded_problems_from_dict(problems_solved_ac_info):
    with open("excluded-problems-list.txt", "r", encoding="utf-8") as txtfile:
        for line in txtfile:
            if line.strip():
                excluded_problem_ids.append(line.strip())

    for excluded_problem_id in excluded_problem_ids:
        if excluded_problem_id in problems_solved_ac_info:
            del problems_solved_ac_info[excluded_problem_id]

    print(f"조건을 만족하는 문제가 총 {len(problems_solved_ac_info)}개 검색되었습니다.")

    return problems_solved_ac_info


def remove_unlisted_problems_from_csv(problems_solved_ac_info):
    problem_ids_of_dict = list(problems_solved_ac_info.keys())

    temp_file = FILE_NAME + ".tmp"

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as infile, open(
        temp_file, "w", newline="", encoding="utf-8"
    ) as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            if row["문제 번호"] in excluded_problem_ids:
                continue
            if row["문제 번호"] in problem_ids_of_dict:
                writer.writerow(row)

    os.replace(temp_file, FILE_NAME)

    return


def remove_existing_problems_from_dict(problems_solved_ac_info):
    csv_problem_ids = []

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        rows = csv.DictReader(file)

        for row in rows:
            csv_problem_ids.append(row["문제 번호"])

    for csv_problem_id in csv_problem_ids:
        if csv_problem_id in problems_solved_ac_info:
            del problems_solved_ac_info[csv_problem_id]

    return problems_solved_ac_info


def shuffle_problems_solved_ac_info(problems_solved_ac_info):
    keys = list(problems_solved_ac_info.keys())

    shuffle(keys)

    shuffled_dict = {key: problems_solved_ac_info[key] for key in keys}

    return shuffled_dict


def get_problem_body_length(problem_url):
    response = requests.get(
        problem_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        },
    )

    soup = BeautifulSoup(response.content, "html.parser")

    total_problem_body_length = 0

    paragraphs = soup.find("div", id="problem_description").find_all("p")

    for paragraph in paragraphs:
        total_problem_body_length += len(paragraph.text)

    paragraphs = soup.find("div", id="problem_input").find_all("p")

    for paragraph in paragraphs:
        total_problem_body_length += len(paragraph.text)

    return total_problem_body_length


def get_avg_solution_length(problem_ac_codes_url):
    response = requests.get(
        problem_ac_codes_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        },
    )

    soup = BeautifulSoup(response.content, "html.parser")

    total_solution_length = 0
    solution_count = 0

    rows = soup.find("div", class_="table-responsive").find_all("tr")

    for row in rows:
        cells = row.find_all("td")

        if len(cells) >= 2:
            solution_length = int(cells[-2].text)

            if solution_length >= 10000:
                continue

            total_solution_length += solution_length
            solution_count += 1

    if solution_count == 0:
        return float("inf")

    return total_solution_length // solution_count


def get_problems_boj_info_and_write_csv_file(problems_info):
    print(
        f"이미 저장된 문제들을 제외한 {len(problems_info)}개의 문제를 검색 결과 데이터 파일에 추가합니다."
    )

    scraped_page_count = 0
    existing_data_count = 0

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows_list = list(reader)
        existing_data_count += len(rows_list)

    for problem_id, problem_info in problems_info.items():
        problem_exists = False

        with open(FILE_NAME, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["문제 번호"] == problem_id:
                    problem_exists = True
                    break

        if problem_exists:
            scraped_page_count += 1
            continue

        problem_url = f"https://acmicpc.net/problem/{problem_id}"
        problem_info["problem_body_length"] = get_problem_body_length(problem_url)

        time.sleep(DELAY_PER_PAGE)

        problem_ac_codes_url = f"https://www.acmicpc.net/problem/status/{problem_id}/1"

        if language_cpp:
            problem_ac_codes_url = (
                f"https://www.acmicpc.net/problem/status/{problem_id}/1001/1"
            )

        problem_info["avg_solution_length"] = get_avg_solution_length(
            problem_ac_codes_url
        )

        if problem_info["avg_solution_length"] == float("inf"):
            scraped_page_count += 1
            continue

        print(
            f"boj.kr 문제 페이지 스크랩 중... ({existing_data_count + scraped_page_count + 1}/{existing_data_count + len(problems_info)})"
        )
        time.sleep(DELAY_PER_PAGE)

        with open(FILE_NAME, "a", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "문제 번호",
                "제목",
                "난이도",
                "푼 사람 수",
                "평균 시도",
                "정답 코드의 평균 길이",
                "문제 본문 길이",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(
                {
                    "문제 번호": problem_id,
                    "제목": problem_info["problem_title"],
                    "난이도": problem_info["problem_tier"],
                    "푼 사람 수": problem_info["problem_solvers_count"],
                    "평균 시도": problem_info["problem_average_try"],
                    "정답 코드의 평균 길이": problem_info["avg_solution_length"],
                    "문제 본문 길이": problem_info["problem_body_length"],
                }
            )

        scraped_page_count += 1

        if (
            EARLY_TERMINATION_FLAG == True
            and scraped_page_count >= PAGES_TO_SCRAPE_PER_RUN
        ):
            print(
                f"프로그램 실행 1회당 스크랩 횟수 {PAGES_TO_SCRAPE_PER_RUN}회에 도달하여 프로그램을 조기 종료합니다."
            )
            return

    print("검색된 모든 문제에 대해 데이터가 성공적으로 생성되었습니다.")

    return


solved_ac_url = f"https://solved.ac/search?query=%21%40{user_id}+*{min_difficulty}..{max_difficulty}+s%23{min_solvers_count}..{max_solvers_count}+t%23{min_average_try}..{max_average_try}"

total_pages = get_total_pages(solved_ac_url)

problems_solved_ac_info = get_problem_solved_ac_infos(solved_ac_url, total_pages)

check_file_header_exists_or_create()

problems_solved_ac_info = remove_excluded_problems_from_dict(problems_solved_ac_info)

remove_unlisted_problems_from_csv(problems_solved_ac_info)

problems_solved_ac_info = remove_existing_problems_from_dict(problems_solved_ac_info)

shuffled_problems_solved_ac_info = shuffle_problems_solved_ac_info(
    problems_solved_ac_info
)

get_problems_boj_info_and_write_csv_file(shuffled_problems_solved_ac_info)

# sort_csv_file()
