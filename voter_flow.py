from EMS_PACKAGE import db_manager
from EMS_PACKAGE import log_manager
from EMS_PACKAGE import validations 


def check_result(V_id):
    ems,cur=db_manager.create_conn()
    
    query=f"Select ConstituencyID from Voter where VoterID={V_id}"
    x=cur.execute(query)
    y=x.fetchall()
       
    query2=f"Select CandidateName,PartyName from Candidate where ConstituencyID={y[0][0]} ORDER BY VoteBallot DESC LIMIT 1"
    a=cur.execute(query2)
    b=a.fetchall()
    
    print("Winner in your Constituency: ".center(123))
    print(f"Name:{b[0][0].title()}".center(120))
    print(f"Party:{b[0][1]}".center(120))
    ems.close()



def cast_vote(V_id): 
    ems,cur=db_manager.create_conn()
    query=f"Select ConstituencyID from Voter where VoterID={V_id}"
    a=cur.execute(query)
    b=a.fetchall()

    query2=f"Select CandidateID,CandidateName,PartyName from Candidate where ConstituencyID={b[0][0]}"
    x=cur.execute(query2)
    y=x.fetchall() 

    print("\nCandidates Contesting in your Constituency: ")
    print("\n")   

    for x in range(len(y)):
        print(f"Candidate ID {y[x][0]}: {y[x][1].upper()} from {y[x][2]}")

    input_vote=input("Enter Candidate ID to Cast Vote: ")
        
    if validations.check_if_blank(input_vote):
        if validations.check_if_int(input_vote):

            query3=f"Select CandidateID from Candidate where ConstituencyID={b[0][0]}"
            p=cur.execute(query3)
            q=p.fetchall()

            test_id=(int(input_vote),)
            if test_id not in q:
                print("ID doesn't exist!")
                return "recall"
            else:
                def sure():
                    input_sure=input("Are you Sure? You cannot recast your vote! Y/N: ")
                    sure_strip=input_sure.replace(" ","")
                    if sure_strip=='Y' or sure_strip=='y':
                        select_query=f"Select VoteBallot from Candidate where CandidateID={input_vote}"
                        t=cur.execute(select_query)
                        u=t.fetchall()

                        add_vote=(u[0][0])+1

                        update_query=f"Update Candidate SET VoteBallot={add_vote} where CandidateID={input_vote}"
                        cur.execute(update_query)
                        ems.commit()

                        update_attempt=f"Update Voter SET VotingAttempt=0 where VoterID={V_id}"
                        cur.execute(update_attempt)
                        ems.commit()
                        print("Your vote has been cast!")
                    elif sure_strip=='N' or sure_strip=='n':
                        return "no"
                    else:
                        print("Invalid Input!")
                        sure()
                if sure()=="no":
                    return "recall"
        else:
            print("Invalid Input!")
            return "recall"

    else:
        print("Invalid Input!")
        return "recall"




def live_poll(V_id):
    ems,cur=db_manager.create_conn()
    select_con=f"Select ConstituencyID from Voter where VoterID={V_id} "
    con=cur.execute(select_con)
    fetch_con=con.fetchall()
    
    select_can=f"Select CandidateName,PartyName,VoteBallot from Candidate where ConstituencyID= {fetch_con[0][0]} ORDER BY VoteBallot DESC"
    can=cur.execute(select_can)
    fetch_can=can.fetchall()
    
    select_con_name=f"select ConstituencyName from Election where ConstituencyID={fetch_con[0][0]}"
    con_name=cur.execute(select_con_name)
    fetch_con_name=con_name.fetchall()
    
    print(f"\n{fetch_con_name[0][0].title()}'s Live Poll: ")
    
    for x in range(len(fetch_can)):
          print(f"\n{fetch_can[x][0].upper()} from {fetch_can[x][1].upper()} with {fetch_can[x][2]} votes")

def voter_menu():
    v_choice=input("Press:\n1 to VOTE\n2 to CHECK RESULT\n3 to CHECK LIVE POLL\n4 to LOG OUT")
    return v_choice


def voter_login():
    #global V_id

    V_id=input("Please Enter id: ")
    
    ems,cur=db_manager.create_conn()

    if validations.check_if_blank(V_id):
        if validations.check_if_int(V_id):
            query=f"Select VoterID from Voter"
            x=cur.execute(query)
            y=x.fetchall()

            test_id=(int(V_id),)

            if test_id in y:
                rv=0
                query2=f"Select VoterName from Voter where VoterID={V_id}"
                a=cur.execute(query2)
                b=a.fetchall()
                
                print(f"Welcome {b[0][0]}!".title())
                print("Please Enter your password.You have 3 attempts.")
                for _ in range(3):
                    v_pass=input("Enter password: ")
                    
                    select_v_pass=f"Select VoterPassword from Voter where VoterID={V_id}"
                    exec_v_pass=cur.execute(select_v_pass)
                    fetch_v_pass=exec_v_pass.fetchall()
                    
                    if v_pass==fetch_v_pass[0][0]:
                        ems.close()
                        rv+=1 #rv=1
                        break
                    else:
                        print("Incorrect password!Try again!")
                else:
                    print("No more attempts left!")                                        
            else:
                print("ID does not exist!")
                return voter_login()
        else:
            print("Invalid Input")
            return voter_login()
    else:
        print("Invalid Input")
        return voter_login()
    
    if rv==1:
        log_manager.update_log(f"Voter ID= {V_id} logged in.")
        return V_id
    else:
        return "fail"
    
    
