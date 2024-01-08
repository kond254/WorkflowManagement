import streamlit as st
import pandas as pd
from db import Databank 


def main():
    db = Databank()

    print(db.check_amount_of_candidates_in_TopCandidateDB(2251799813758473)[0][0]>0)       
    
    
    
    
if __name__ == '__main__':
    main()
