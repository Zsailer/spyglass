import random
import string
import pprint

from zxcvbn import zxcvbn

def generate_password(
    length=8,
    alpha=True,
    capital=True,
    numeric=True,
    special=True,
    other=None,
    ):
    """Generate a random password.
    
    Parameters 
    ----------
    length : int
        length of password.
    
    alpha : bool
        If True, include lowercase characters in password

    capital : bool
        If True, include uppercase characters in password.

    numeric : bool
        If True, include digits in password.

    special : bool
        If True, include various special characters in password. (see string.puntuation)

    other : list or None (default is None)
        A list of characters to sample for the password.
    """
    # List of characters to choose from.
    options = []
    
    # Add lowercase alphabet
    if alpha: 
        options += string.ascii_lowercase 

    # Add capital letters
    if capital and alpha:
        options += string.ascii_uppercase

    # Add numeric characters
    if numeric:
        options += string.digits

    # Add special characters
    if special: 
        options += string.punctuation

    # If other is a list
    if isinstance(other, list):
        options += other
    elif other is not None:
        raise Exception("Other must be a list")

    # Build password from options list
    password = ''.join([random.choice(options) for i in range(length)])
    return password


def calculate_strength(password, full_report=False):
    """Gets a score from 0->4, evaluating the strength of a 
    password following DropBox's algorithm.
    """
    results = zxcvbn(password)

    # Return full report or just score.
    if full_report:
        return results

    return results["score"]

def print_score_results(results, full_report=False):

    if full_report:
        print()
        print("Password statistics:")
        pprint.pprint(results, depth=2)
        print()

    else:
        score = results["score"]
        scoring_responses = {
            0: "This password is extremely vulnerable. Consider a new password.",
            1: "This password is quite vulnerable. Consider a new password.",
            2: "This password is okay, but could be more secure.",
            3: "This password is pretty good.",
            4: "This password is great--very secure."
        }

        print()
        print(f"Password score: {score} of 4.")
        print(scoring_responses[score])
        print()
