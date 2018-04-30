file-emailer
============

This is a small program that emails Atom/RSS feed entries to you. It is
designed to be run periodically (e.g. as a cronjob).

PGP support coming soon!

<!--
## Table of contents
  -
  -
  -
-->

## Getting started

1. Download and install [Python3](https://www.python.org/).

2. Clone or [download](https://github.com/abithakt/feed-emailer/archive/master.zip) this repository.

2. Navigate to the folder and install the dependencies:
```
pip3 install -r requirements.txt
```
or
```
py -m pip install -r requirements.txt
```

3. Rename `example-config.yml` to `config.yml`. Edit it to include your details:

    1. Update `last_accessed` to a date of your choosing. For best results, set it to a date in the recent past or today's date.
        * On the first run, `feed-emailer` will email you all entries since the date stored in `last_accessed`.  
        * Make sure the date is in the format `YYYY-MM-DD HH:MM:SS`.
    2. Put your email address and password under `from` and `password`. This is the address from which emails will be sent.
    3. Put the recipient's email address under `to`.
    4. Under `smtp_server` and `smtp_port`, put your email provider's SMTP server and port.
    5. Finally, add the list of feeds you would like to subscribe to under `feeds`.

5. Run `feed-emailer.py`.
```
python3 feed-emailer.py
```
or
```
py feed-emailer.py
```

## Usage

Run

```
python3 feed-emailer.py
```

or

```
py feed-emailer.py
```

For best results, schedule this command to repeat (e.g. as a cronjob).


## Contributing

Please submit issues and feature requests [here](https://github.com/abithakt/feed-emailer/issues). Pull requests are welcome. For more information, feel free to email me.


## License

file-emailer is licensed under the GPLv3. For more details, see [LICENSE](LICENSE).

> Copyright (C) 2018 Abitha K Thyagarajan

> This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

> This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

> You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
