# Pre-School Bill


#### Python script to get and inform homemates about Pre-School bill in current month

##### Copyright (C) 2019 Andrzej Michalski 

<small>
<small>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
</small>
</small>


#### Description
In home there is a problem with get infromation about Pre-School bills. 
Information are stored in webpage which is needed to log and check if 
there are new bills. You have to check this systematically everyday at the begining
of month, because term of payment is to 15th day of month.

Module is written to work on Raspberry Pi3 (RPi3) (Hassbian) on home. RPi3 is turn
on constantly because it is home manager. Script is written in Python 3
and is running everyday by Crontab.

Program use Requests to get data from site, after that data is parsing
by BeautifullSoup module. Next step is creating and sending email with Yagmail 
(home RPi3 has own email adress to communicate with users). After that
the informing e-mail, about bill to pay in month is sent to me and my wife.
Sending depends from logged information, if e-mail with information
was sent in this month action is not performed.

Program requires two text files:
- data.txt - log file in which data of payment for every month is recorded
- user_data.txt - file in which login data are stored

Unit Tests are perfomed in unittest library. To test sending e-mail mocks are used.

#### Base requirements
1. Python 3 - in this case Python 3.5
2. Virtualenv

#### Installation
1. Clone this git repository
2. Create virtualenv - "virtualenv --python=python3 .venv
3. Install requirements with pip - "pip install -r requirements.txt"
4. Make base file executable - "chmod +x preschool_bill.py"
5. Create empty log file - "touch data.txt"
6. Create user data file - "touch user_data.txt"
7. Edit user data file in this convention:
```txt
LOGIN <user_login>
PASSWORD <user_password>
EMAILS test1@gmail.com test2@gmail.com
GMAIL_USER mail_for_RPi3@gmail.com
GMAIL_PASS <pass_for_mail_RPi3>
```
8. Run preschool_bill.py file - "/absolute/path/to/preschool_bill.py"


