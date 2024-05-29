from EMS_PACKAGE import db_manager

def check_if_blank(intput):
    intput_strip=intput.strip()
    
    if len(intput_strip)!=0:
        return True
    else:
        return False


def check_if_int(intput):
    intput_strip=intput.strip()
    
    if intput_strip.isdigit():
        return True
        
    else:
        return False
    
def check_name(input_name):
    input_name_no_space=input_name.replace(" ","")
    
    if len(input_name_no_space)==0 or input_name.isspace():
        print("Name cannot be blank!")
        return False
        
        
    elif not(input_name_no_space.isalpha()):
        print("Name can only have letters")
        return False
        
    elif len(input_name.split())<2:
        print("Enter First name AND Last name!")
        return False
        
    elif len(input_name.split())>2:
        print("Enter First name and Last name ONLY!")
        return False
    
    elif len(input_name)>50:
        print("Name can only have 50 characters!")
        
    else:
        return True
    
def check_time(V_id):
    import datetime
    ems,cur=db_manager.create_conn()
    current=datetime.datetime.now()

    query=f"Select ConstituencyID from Voter where VoterID={V_id}"
    x=cur.execute(query)
    y=x.fetchall()


    q1=f"Select StartTime,EndTime from Election where ConstituencyID={y[0][0]}"
    a=cur.execute(q1)
    b=a.fetchall()


    st=b[0][0]
    sy,sm,sd,sh,smm,ss=st.split("/")

    start_time=datetime.datetime(int(sy),int(sm),int(sd),int(sh),int(smm),int(ss))    

    et=b[0][1]
    ey,em,ed,eh,emm,es=et.split("/")

    end_time=datetime.datetime(int(ey),int(em),int(ed),int(eh),int(emm),int(es))
    
    ems.close()

    if end_time<current:
        return "over"

    elif current<start_time:
        return "not_started"

    else:        
        return "proceed"
    
def check_attempt(V_id):
    ems,cur=db_manager.create_conn()
   
    query1=f"Select VotingAttempt from Voter where VoterID={V_id}"
    a=cur.execute(query1)
    b=a.fetchall()
    
    if b[0][0]==1:
        ems.close()
        return True
    
    else:
        ems.close()
        return False
    

