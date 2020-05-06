# this is a dummy script to demonstrate API functionality

from docx import Document
from flask import jsonify
import sys

# if __name__ == '__main__':
def dummy_to_lower(text): 
    result = text.lower()
    print(result)
    return((result))
    return(result)

dummy_to_lower('PROJECT TITLE: The Project Has A Name\n\nBACKGROUND: This is a short project detailing the background of the project, why the work is necessary, and how it fits into the greater context of the organization mission.  \n\nSCOPE:  The scope would detail the level of detail of the work, how it would be used, specific project goals, deliverables, features, functions, tasks, deadlines, timeframes, and costs.')