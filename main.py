from os import urandom
from bs4 import BeautifulSoup
import requests
import json
import os
from pathlib import Path

supported_lan = [
    ('++', 'cpp'),
    ('gcc', 'c'),
    ('clang', 'c'),
    ('JavaScript', 'js'),
    ('Java', 'java'),
    ('Python', 'py'),
    ('C#', 'cs'),
    ('D ', 'd'),
    ('Node', 'js'),
    ('Kotlin', 'kt'),
    ('Go ', 'go'),
    ('Ruby', 'rb'),
    ('Rust', 'rs'),
    ('Perl', 'pl'),
    ('Scala', 'scala'),
    ('Pascal', 'pas'),
    ('Haskell', 'hs'),
    ('PHP', 'php')

]


class Codeforces:
    def __init__(self, username) -> None:
        self.username = username
        self.submissions = list(tuple())
        if not os.path.exists('./src'):
            path = os.path.join('.', 'src')
            os.mkdir(path)
        # if os.
        file = Path("./src/submissions.txt")
        if not file.is_file():
            file = open('./src/submissions.txt', 'w')

    def isValidUser(self):
        url = f'https://codeforces.com/api/user.info?handles={self.username}'
        obj = requests.get(url)
        obj = json.loads(obj.text)
        if obj['status'] == 'OK':
            return True
        return False

    def _getSourceCode(self, contestid: int, submission: int):
        url = f'https://codeforces.com/contest/{contestid}/submission/{submission}'
        html_file = requests.get(url).text
        try:
            soup = BeautifulSoup(html_file, 'lxml')
            code = soup.find('pre', id='program-source-text').text
        # print(code)
            return code
        except:
            return None

    def _getAllSubmissions(self):
        url = f'https://codeforces.com/api/user.status?handle={self.username}'
        try:
            parsed_obj = requests.get(url)
            parsed_obj = json.loads(parsed_obj.text)
        except Exception as e:
            print('Error Occured...\n{e}')
            return

        if parsed_obj['status'] != 'OK':
            print('API falied')
            return
        parsed_obj = parsed_obj['result']
        for sub in parsed_obj:

            lang = sub['programmingLanguage']
            for l in supported_lan:
                if l[0] in lang:
                    lang = l[1]
                    break

            if sub['verdict'] == 'OK':
                with open('./src/submissions.txt', 'r') as f:
                    lines = f.readlines()
                    alreadyExists = False
                for line in lines:
                    if f"{sub['problem']['contestId']}{sub['problem']['index']}" in line:
                        print(
                            f"{sub['problem']['contestId']}{sub['problem']['index']} already exists...")
                        alreadyExists = True
                        break

                if alreadyExists:
                    continue

                self.submissions.append(
                    (sub['id'], (sub['problem']['contestId'], sub['problem']['index'], lang)))
                # print(sub)

    def _saveSubmissions(self):
        for submission in self.submissions:
            submission_id = submission[0]
            contest_id = submission[1][0]
            problem_index = submission[1][1]
            lang = submission[1][2]
            file = f'./src/{contest_id}'
            # print(file)
            if not os.path.exists(file):
                os.makedirs(file, 0o777, False)
                # print(file)
            file += f'/{problem_index}.{lang}'
            print(f'creating {file}')
            src_code = self._getSourceCode(contest_id, submission_id)
            if src_code == None:
                print(f'Error while parsing code {contest_id}{probelm_index}')
                continue
            # print(contest_id)
            f = open(file, 'w')
            f.write(src_code)
            f.close()
            # if not alreadyExists:
            with open('./src/submissions.txt', 'a') as x:
                x.write(f'{contest_id}{problem_index}\n')


uname = str(input('Enter your codeforces username: '))
want_readme = str(input('Do you want a readme file (y/n): '))
PVCODES = Codeforces(username=uname)

isvalid = PVCODES.isValidUser()
if not isvalid:
    print('User not valid.......\nTry Again :(')

else:

    PVCODES._getAllSubmissions()
    PVCODES._saveSubmissions()


if want_readme == 'y':
    intial_readme = f"""<h2 align=center> All Codeforces Submissions</h2>
<p align=right>
<a href="https://codeforces.com/profile/{uname}">codeforces handle</a>
</p>

### This README.md is generated by using [codeforces-submissions](https://github.com/pvcodes/codeforces-submissions)

<hr>

<div>
<table border=solid  align=center>
    <thead align=center>
      <tr>
        <th width=150>Contests</th>
        <th width=300>Submission Question Index with code link</th>
      </tr
    </thead>
    <tbody align=center>
"""

    file = Path("README.md")
    if not file.is_file():
        file = open('README.md', 'w')
        file.write(intial_readme)
        file.close()

    for sub in PVCODES.submissions:
        try:
            contest_id = sub[1][0]
            probelm_index = sub[1][1]
            lang = sub[1][2]

            inserted = f"""      <tr>
                <td><a href="https://codeforces.com/contest/{contest_id}/">CF {contest_id}</td> 
                    <td><a href="/src/{contest_id}/{probelm_index}.{lang}">{probelm_index}</td>
                </tr>
        """

            with open('README.md', 'a') as f:
                f.write(inserted)

        except:
            print('Error occured while creating readme.. :(')

    f = open('README.md', 'a')
    footer = f'<br><br><br>'
    f.write(footer)
    f.close()
