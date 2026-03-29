# Quiz questions database for Python
quiz_questions = {
    "beginner": [
        {
            "question": "What is the output of print(2 ** 3)?",
            "options": ["5", "6", "8", "9"],
            "correct": 2,
            "explanation": "The ** operator performs exponentiation. 2**3 means 2 raised to power 3 = 8"
        },
        {
            "question": "Which of the following is a valid variable name in Python?",
            "options": ["2var", "_var", "var-name", "var name"],
            "correct": 1,
            "explanation": "Variable names can start with a letter or underscore, but not with numbers"
        },
        {
            "question": "What is the data type of the value 3.14?",
            "options": ["int", "float", "str", "bool"],
            "correct": 1,
            "explanation": "3.14 is a floating-point number (float)"
        },
        {
            "question": "Which function is used to get input from user?",
            "options": ["print()", "input()", "get()", "scan()"],
            "correct": 1,
            "explanation": "input() is used to take user input in Python"
        },
        {
            "question": "What does len('Python') return?",
            "options": ["5", "6", "7", "Error"],
            "correct": 1,
            "explanation": "len() returns the number of characters in a string. 'Python' has 6 characters"
        }
    ],
    "intermediate": [
        {
            "question": "What is a lambda function?",
            "options": ["A named function", "An anonymous function", "A built-in function", "A recursive function"],
            "correct": 1,
            "explanation": "Lambda functions are anonymous, single-line functions in Python"
        },
        {
            "question": "Which of the following is mutable?",
            "options": ["tuple", "string", "list", "int"],
            "correct": 2,
            "explanation": "Lists are mutable (can be changed), while tuples, strings, and ints are immutable"
        },
        {
            "question": "What does the 'self' keyword represent in Python classes?",
            "options": ["The class itself", "The instance of the class", "A static method", "A class variable"],
            "correct": 1,
            "explanation": "'self' represents the instance of the class"
        },
        {
            "question": "What is the output of [1,2,3] * 2?",
            "options": ["[2,4,6]", "[1,2,3,1,2,3]", "Error", "[1,2,3,2]"],
            "correct": 1,
            "explanation": "Multiplying a list repeats its contents: [1,2,3] * 2 = [1,2,3,1,2,3]"
        },
        {
            "question": "Which method is used to add an element to a set?",
            "options": ["add()", "append()", "insert()", "push()"],
            "correct": 0,
            "explanation": "add() is used to add elements to a set"
        }
    ],
    "advanced": [
        {
            "question": "What is a decorator in Python?",
            "options": ["A design pattern", "A function that modifies other functions", "A class inheritance", "A data type"],
            "correct": 1,
            "explanation": "Decorators are functions that modify the behavior of other functions"
        },
        {
            "question": "What is the purpose of __init__ method?",
            "options": ["To initialize class attributes", "To destroy objects", "To create static methods", "To import modules"],
            "correct": 0,
            "explanation": "__init__ is the constructor method that initializes object attributes"
        },
        {
            "question": "What is a generator in Python?",
            "options": ["A function that returns a list", "A function that yields values one at a time", "A random number generator", "A type of loop"],
            "correct": 1,
            "explanation": "Generators use yield to produce a sequence of values lazily"
        },
        {
            "question": "What does the GIL (Global Interpreter Lock) do?",
            "options": ["Locks global variables", "Prevents multiple threads from executing simultaneously", "Manages memory", "Handles exceptions"],
            "correct": 1,
            "explanation": "GIL allows only one thread to execute at a time in CPython"
        },
        {
            "question": "What is the output of list(zip([1,2], ['a','b']))?",
            "options": ["[(1,'a'), (2,'b')]", "[[1,2], ['a','b']]", "[1,'a',2,'b']", "Error"],
            "correct": 0,
            "explanation": "zip() combines elements from multiple iterables into tuples"
        }
    ]
}

def get_questions_by_level(level, count=5):
    """Get specified number of questions for a given level"""
    if level in quiz_questions:
        questions = quiz_questions[level]
        return questions[:count]  # Return first 'count' questions
    return []