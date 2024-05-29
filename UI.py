def welcome_page():
    heading="Maharashtra Legislative assembly election 2022".center(120)
    sub_heading="Conducted by State Election Commission".center(120)
    
    print(heading)
    print(sub_heading)
    
    
    welcome_input=input("Press:\n1 if you're an ADMIN \n2 if you're a VOTER \n3 to EXIT ")
    if welcome_input=='1':
        return '1'        
    elif welcome_input=='2':
        return '2'
        
    elif welcome_input=='3':
        return '3'
    else:
        return '0'
        
      
    
    