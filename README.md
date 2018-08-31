# Spyglass

* Simple and Secure password management tool written in Python.

Spyglass creates random passwords for you and stores them in a hidden encrypted file. When you want to retrieve a password, ask spyglass to *temporarily* copy it to your clipboard. You can paste it into your browser without ever seeing the password. Then, it will be flushed from your clipboard after 15 seconds. 


## Install

Clone from source:
```
git clone https://github.com/Zsailer/spyglass
```

Install source using pip.
```
cd spyglass
pip install -e . 
```

## Usage

Initialize Spyglass. You only need to do this one time.
```
spyglass init
```

Create and store a random password. Give it a key and usename.
```
spyglass add paypal zsailer
```

List passwords stored in spyglass.
```
spyglass ls --username

Spyglass keys:
  - email
    - username: zachsailer

```

Generate a password.


