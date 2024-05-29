import random
from EMS_PACKAGE import db_manager
from EMS_PACKAGE import log_manager
from EMS_PACKAGE import validations

def admin_login():
    ems,cur=db_manager.create_conn()
    rv=0
    print("\nWelcome!You have 3 login attempts.\n")
    for ran in range(3):
        in_id = input("Enter Admin ID: ")
        in_pass= input("Enter password: ")
        print("\n")
        
        if validations.check_if_blank(in_id) and validations.check_if_int(in_id) and validations.check_if_blank(in_pass):
            query1=f"Select AdminID,AdminPassword from Admin"
            x=cur.execute(query1)
            y=x.fetchall()

            if (int(in_id),in_pass) in y:
                query2=f"Select AdminName from Admin where AdminID={in_id}"
                a=cur.execute(query2)
                b=a.fetchall()

                print(f"Welcome {b[0][0]}!")
                ems.close()                
                log_manager.update_log(f"admin {in_id} logged in")
                rv+=1 #rv=1
                break
                

            else:
                print("Invalid ID OR Password\nTry Again!")
        else:
            print("Invalid ID OR Password\nTry Again!")
            
    else:
        rv+=2 #rv=2
        
    if rv==1:
        return "proceed"
    elif rv==2:
        return 'fail'
        
def admin_menu():
    adChoice=input("Press:\n1 to Conduct Election\n2 to Add Voter\n3 to Update Voter\n4 to LOG OUT")
    adChoicestrip=adChoice.replace(" ","")
    return adChoicestrip
    
def insert_election(cname,sdate,edate):
    ems,cur=db_manager.create_conn()
    query=f"Insert into Election(ConstituencyName,StartTime,EndTime) values('{cname}','{sdate}','{edate}')"
    cur.execute(query)
    ems.commit()
    ems.close()
    return
    
def add_time():
    import datetime
    year=2022
    min_dur=30
    max_dur=60
    
    def dur(start_time):
        duration=input("\nEnter Election duration: ")
        
        try:
            dur_strip=duration.strip()
            if int(dur_strip)<min_dur:
                print(f"Duration must be atleast {min_dur} days!")
                return dur(start_time)
            elif int(dur_strip)>max_dur:
                print(f"Duration can't be greater than {max_dur} days!")
                return dur(start_time)
            else:
                end_time=start_time+datetime.timedelta(days=int(duration))
                print_e_time=end_time.strftime("%c")
                print(f"\nElection End time is {print_e_time}")
                
                return end_time


        except:
            print("Invalid Input!")
            dur(start_time)
            
    tod=datetime.date.today()
    
    print(f"\nPlease Enter Date of Commencement: ")
    
    m=input("Enter Month: ")
    d=input("Enter Day: ")
    
    print("Enter Start Time: ")
    h=input("Hour: ")
    mm=input("Minutes: ")
    
    try:
        start_time=datetime.datetime(int(year),int(m),int(d),int(h),int(mm))
        start_time_date=datetime.date(int(year),int(m),int(d))
        
        if start_time_date<=tod:
            print("Please set a date in Future!")
            return add_time()
    except:
        print("Invalid Input!")
        return add_time()
        
    else:
        print_s_time=start_time.strftime("%c")
        print(f"\nElection Start time is {print_s_time}")
        
        end_time=dur(start_time)
        
        start_time_string=start_time.strftime("%Y/%m/%d/%H/%M/%S")
        end_time_string=end_time.strftime("%Y/%m/%d/%H/%M/%S")
        
        log_manager.update_log(f"Election start time set as: {start_time_string} ")
        log_manager.update_log(f"Election End time set as: {end_time_string} ")
        
        return start_time_string, end_time_string
    
def add_constituency():

    input_con=input("Enter Constituency Name: ")
    input_con_low=input_con.lower().strip()

    ems,cur=db_manager.create_conn()


    select_con=f"Select ConName from Constituencies"
    exc=cur.execute(select_con)
    fetch_con=exc.fetchall()

    test_con=(input_con_low,)

    if test_con in fetch_con:
        test2="Select ConstituencyName from Election"
        t2=cur.execute(test2)
        fetcht2=t2.fetchall()
        
        if test_con in fetcht2:
            print("Election details already present for this Constituency!")
            return add_constituency()
        else:
            print("Constituency Added!")
            log_manager.update_log(f"New Constituency added in Election Table={input_con}")
            ems.close()    
            return input_con
    else:
        print("Invalid Constituency!")
        log_manager.log_error(f"Cannot assign Constituency for value={input_con}")
        return add_constituency()
    
def conduct_election():
    constituency=add_constituency()
    
    start_time_string,end_time_string=add_time()
    
    insert_election(constituency,start_time_string,end_time_string)
    
    print(f"\nElection Details:\nConstituency: {constituency.title()}\nFrom: {start_time_string}\nTo:   {end_time_string}")
    
    
    return "done" 

def insert_voter(vn,vid,vdob,vpass):
    ems,cur=db_manager.create_conn()
    query=f"insert into Voter(VoterName,ConstituencyID,VoterDOB,VoterPassword) values('{vn}',{vid},'{vdob}','{vpass}')"
    cur.execute(query)
    ems.commit()
    ems.close()

def generate_password():
    lower="abcdefghijklmnopqrstuvwxyz"
    upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits="1234567890"
    specialchar="!@#$%^&*()"
    
    passlength=8
    
    allchar=lower+upper+digits+specialchar
    
    ad_password="".join(random.sample(allchar,passlength))
    
    print(f"Password Assigned: {ad_password}") 
    return ad_password


def input_dob2():
    import datetime
    print('\nPlease Enter Date of Birth in YYYY/MM/DD format: ')
    y=input('Year: ')
    m=input('Month: ')
    d=input('Day: ')
    
          
    try:
        trial_time=datetime.date(int(y),int(m),int(d))
        print(f'Date: {trial_time}')

        def calculate_age(y,m,d):

            dob=datetime.date(int(y),int(m),int(d))
            max_date=datetime.date.today()


            x=max_date.year-dob.year

            if dob.month>max_date.month:
                x-=1
            elif dob.month==max_date.month:
                if dob.day>max_date.day:
                    x-=1

            if x<18:
                print(f"Voter Must be of atleast 18 years of age!")
                log_manager.log_error(f"Unable to assign DOB for values={y}/{m}/{d}")
                return input_dob2()

            elif x>120:
                print("Invalid Age!")
                log_manager.log_error(f"Unable to assign DOB for values={y}/{m}/{d}")
                return input_dob2()
            else:
                print("Date of Birth stored!")
                log_manager.update_log(f"DOB Assigned value={y}/{m}/{d}")
                return (f"{y}_{m}_{d}")

        dob=calculate_age(y,m,d)
        return dob

         
    except:
        print('Invalid Date!')
        log_manager.log_error(f"Unable to assign DOB for values={y}/{d}/{m}")
        return input_dob2()
            

def assign_constituency():
    ems,cur=db_manager.create_conn()
    select_const=f"Select ConstituencyID,ConstituencyName from Election"
    execute_sc=cur.execute(select_const)
    fetch_const=execute_sc.fetchall()
    
    print("\nPlease Choose Constituency: ")
    print('\nPress: ')

    for x in range(len(fetch_const)):
        print(f"{fetch_const[x][0]} for {fetch_const[x][1]}")


    const_choice=input()
    if validations.check_if_blank(const_choice):
        if validations.check_if_int(const_choice):

            const_list=[]
            for a in range(len(fetch_const)):
                b=fetch_const[a][0]
                const_list.append(b)
                            
            int_con=int(const_choice)
            if int_con in const_list:
                int_con_index=const_list.index(int_con)
                print(f"\nConstituency Assigned: {fetch_const[int_con_index][1]}")
                log_manager.update_log(f"Constituency Assigned Value: {const_choice}")
                ems.close()
                return int_con
            else:
                print("Invalid Input!")
                log_manager.log_error(f"Unable to assign Constituency for value={const_choice}")
                return assign_constituency()    
        else:
            print('Invalid Input!')
            log_manager.log_error(f"Unable to assign Constituency for value={const_choice}")
            return assign_constituency()
    else:
        print("Field Can't be blank!")
        return assign_constituency()

def add_name():
    name=input('Full Name: ')
    if validations.check_name(name):
        print(f"Name Stored!")
        log_manager.update_log(f"Voter Name Assigned value={name}")
        return name          
    else:
        log_manager.log_error(f"Unable to Assign Name for value={name}")
        return add_name()

def add_voter():
    log_manager.update_log('Admin chose "add voter" ')
    print('Please Enter Voter Details: ')
    
    #name:
    v_name=add_name()
    
    #ConstituencyID
    v_con_id=assign_constituency()
    
    #dob
    v_dob=input_dob2()
    
    #password
    v_password=generate_password()
    
    insert_voter(v_name,v_con_id,v_dob,v_password)
    
    print("\nVoter details added: \n")
    print(f"Name: {v_name}\nConstituency ID: {v_con_id}\nDate of Birth: {v_dob}\nPassword: {v_password}\n")    
    return "done"
    
def update_constituency():
    up_v_id=choose_voter()
    ems,cur=db_manager.create_conn()
    query=f"Select ConstituencyID from Voter where VoterID={up_v_id}"
    a=cur.execute(query)
    b=a.fetchall()
    old_id=b[0][0]
    
    query1=f"Select ConstituencyName from Election where ConstituencyID={old_id}"
    x=cur.execute(query1)
    y=x.fetchall()
    old_con=y[0][0].upper()
    print(f"\nOld Constituency: {old_con}\n")
    
    def input_new_constituency():
        select_const=f"Select ConstituencyID,ConstituencyName from Election"
        execute_sc=cur.execute(select_const)
        fetch_const=execute_sc.fetchall()


        print("\nPlease Choose Constituency: ")
        print('\nPress: ')

        for x in range(len(fetch_const)):
            print(f"{fetch_const[x][0]} for {fetch_const[x][1]}")

        const_choice=input()

        if validations.check_if_blank(const_choice) and validations.check_if_int(const_choice):
            const_list=[]
            for a in range(len(fetch_const)):
                b=fetch_const[a][0]
                const_list.append(b)

            int_con=int(const_choice)

            if int_con in const_list:

                update_query=f"Update Voter set ConstituencyID={int_con} where VoterId={up_v_id}"
                cur.execute(update_query)
                ems.commit()


                query4=f"Select ConstituencyName from Election where ConstituencyID={int_con}"
                xx=cur.execute(query4)
                yy=xx.fetchall()
                new_con=yy[0][0].upper()


                mess=f"\nConstituency updated from {old_con} to {new_con}"
                log_manager.update_log(f"{mess} for voter ID: {up_v_id}")

                print(mess)
                ems.close()

            else:
                print("Invalid Input!")
                log_manager.log_error(f"Cannot update constituency")
                input_new_constituency()

        else:
            print('Invalid Input!')
            log_manager.log_error(f"Cannot update constituency")
            input_new_constituency()
    input_new_constituency()

def update_name():
    ems,cur=db_manager.create_conn()
    up_vote_id=choose_voter()
    query=f"Select VoterName from Voter where VoterID={up_vote_id}"
    a=cur.execute(query)
    b=a.fetchall()
    old_name=b[0][0].upper()
    print(f"\nCurrent Name: {old_name}")
    
    def input_new_name():
        upname=input('Enter New Name: ')

        if validations.check_name(upname):        
            query1=f"UPDATE Voter SET VoterName='{upname.lower()}' WHERE VoterID={up_vote_id}"
            cur.execute(query1)
            print(f"\nName updated from {old_name} to {upname.upper()}")
            log_manager.update_log(f"Name updated from {old_name} to {upname.upper()} for Voter ID:{up_vote_id}")
            ems.commit()
            ems.close()
        else:
            log_manager.log_error(f"Unable to update name for value {upname}")
            input_new_name()
    input_new_name()
        
def choose_voter():
    ems,cur=db_manager.create_conn()
    up_v_id=input("Please Enter Voter ID: ")

    if validations.check_if_blank(up_v_id):
        if validations.check_if_int(up_v_id):
            query=f"Select VoterID from Voter"
            x=cur.execute(query)
            y=x.fetchall()

            test_id=(int(up_v_id),)

            if test_id in y:
                ems.close()
                return up_v_id.strip()
            else:
                print("ID does not exist!")
                return choose_voter()
        else:
            print("Invalid Input")
            return choose_voter()
    else:
        print("Invalid Input")
        return choose_voter()
            
def update_dob():
    up_v_id=choose_voter()
    ems,cur=db_manager.create_conn()
    query=f"Select VoterDOB from Voter where VoterID={up_v_id}"
    a=cur.execute(query)
    b=a.fetchall()
    old_dob=b[0][0]
    
    print(f"\nCurrent Date of Birth: {old_dob}")
          
    new_dob=input_dob2()
    
    print(f"\nDate of Birth updated from {old_dob} to {new_dob}")
    log_manager.update_log(f"DOB updated from {old_dob} to {new_dob} for Voter ID:{up_v_id}")
    
    updob=f"UPDATE Voter SET VoterDOB='{new_dob}' where VoterID={up_v_id}"
    cur.execute(updob)
    ems.commit()
    ems.close()
        
def update_menu():
    upchoice=input("Update:\n1 Name\n2 Constituency\n3 Date of Birth\n4 Return to Menu")
    up_choice_strip=upchoice.replace(" ","")
    return up_choice_strip
        
