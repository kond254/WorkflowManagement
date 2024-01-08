import streamlit as st
import pandas as pd



def main():
    json_array=[{"process_id":2251799813721666,"first_name":"test","last_name":"test","gender":"m","email":"test@test.de","linkedin":"testlinkedin","adress":"testsrr. 20","city":"testcity","zip_code":12345,"country":"testcountry","age":23,"previous_company":"testPrevComp","rating":8},{"process_id":2251799813721666,"first_name":"test","last_name":"test","gender":"m","email":"test@test.de","linkedin":"testlinkedin","adress":"testsrr. 20","city":"testcity","zip_code":12345,"country":"testcountry","age":23,"previous_company":"testPrevComp","rating":8}]
    for candidate in json_array:
        process_id = candidate.get("process_id")
        first_name = candidate.get("first_name")
        last_name = candidate.get("last_name")
        gender = candidate.get("gender")
        email = candidate.get("email")
        linkedin = candidate.get("linkedin")
        address = candidate.get("adress")  # Note: "adress" is a typo, it should be "address"
        city = candidate.get("city")
        zip_code = candidate.get("zip_code")
        country = candidate.get("country")
        age = candidate.get("age")
        previous_company = candidate.get("previous_company")
        rating = candidate.get("rating")
        print(f"Processing candidate: {first_name} {last_name}, Email: {email}, Age: {age}")
    
    
if __name__ == '__main__':
    main()
