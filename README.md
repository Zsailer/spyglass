# Spyglass

*Simple password generator/management tool written in Python.*

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
> spyglass init
```

Generate a random password for username `zsailer`. Spyglass also scores your password using Dropbox's [zxcvbn](https://github.com/dwolfhub/zxcvbn-python).
```
> spyglass add bank zsailer

Password score: 4 of 4.
This password is great--very secure.

Password successfully added!

```

Or store a password you're already using
```
> spyglass add gmail zach --password mypassword


Password score: 1 of 4.
This password is quite vulnerable. Consider a new password.

Password successfully added!

```

List passwords stored in spyglass.
```
> spyglass ls --username

Spyglass keys:
  - email
    - username: zachsailer

```

Copy that password to your clipboard. 
```
> spyglass get bank

Username: zsailer
Password copied to clipboard!

```

Score any password you want to try. 
```
> spyglass score trythispassword

Password score: 2 of 4.
This password is okay, but could be more secure.

```



