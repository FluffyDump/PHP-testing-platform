from app import exceptions
import re, logging

#Perform a check if provided input contains letters-only
def letters_numbers_only(input: str) -> bool:
    if re.search(r'[^a-zA-Z0-9]', input):
        logging.warning(f"Input contains chars, input string: {input}")
        return False
    return True


#Perform a check if provided input possibly contains SQL query
def validate_sql_malicious_input(*args):
    malicious_patterns = [
        r"\bselect\b",
        r"\bdrop\b",
        r"\binsert\b",
        r"\bupdate\b",
        r"\bdelete\b",
        r"\bunion\b",
        r"\balter\b",
        r"\bcreate\b",
        r"\brename\b",
        r"\btruncate\b",
        r"\bgrant\b",
        r"\brevoke\b",
        r"\bexec\b",
        r"\bexecute\b",
        r"\bxp_\b",
        r"\bsp_\b",
        r"\binformation_schema\b",
        r"\bsysobjects\b",
        r"\bsyscolumns\b"
    ]

    pattern = re.compile("|".join(malicious_patterns), re.IGNORECASE)
    
    for arg in args:
        if arg is not None:
            if pattern.search(arg):
                logging.warning(f"Input contains possible SQL query: {arg}")
                raise exceptions.BadRequest("Pateikti duomenys netinkami!")