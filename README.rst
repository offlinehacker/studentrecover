Studentrecover
##############

A small tool that recovers username for uni-lj by brute forcing all possible
combinations and using antigate for captcha cracking.

Install
#######

    $ python setup.py install

Usage
#####

Register on antigate and get your antigate userid, everything else is simple
as::

    $ studentcracker --firstname <first_name> --lastname <last_name> --date <dd-mm-yyyy> --studentid 64080*** --faculty <FE|FRI|...> --antigateid <your_antigate_id>
