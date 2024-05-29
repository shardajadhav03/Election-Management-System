from EMS_PACKAGE import UI
from EMS_PACKAGE import admin_flow
from EMS_PACKAGE import voter_flow
from EMS_PACKAGE import validations
from EMS_PACKAGE import log_manager

def main_code():
    welc_page=UI.welcome_page()
    if welc_page=='1':
        ad_log=admin_flow.admin_login()
        if ad_log=="proceed":
            def run_ad_menu():
                ad_menu=admin_flow.admin_menu()
                if ad_menu=='1':
                    con_add=admin_flow.conduct_election()
                    if con_add=="done":
                        print("\nReturning to Menu\n")
                        return run_ad_menu()
                elif ad_menu=='2':
                    if admin_flow.add_voter()=="done":
                        print("\nReturning to Menu\n")
                        return run_ad_menu()                                                                           
                elif ad_menu=='3':
                    def update_v_menu():
                        up_value=admin_flow.update_menu()
                        if up_value=="1":
                            admin_flow.update_name()
                            print("\nReturning to Update Menu\n")
                            return update_v_menu()
                        elif up_value=="2":
                            admin_flow.update_constituency()
                            print("\nReturning to Update Menu\n")
                            return update_v_menu()
                        elif up_value=="3":
                            admin_flow.update_dob()
                            print("\nReturning to Update Menu\n")
                            return update_v_menu()                            
                        elif up_value=="4":
                            print("\nReturning to Menu\n")
                            return run_ad_menu()
                        else:
                            print("\nInvalid Input!\n")
                            return update_v_menu()
                    update_v_menu()                                               
                elif ad_menu=='4':
                    print("\nReturning to Home\n")
                    return main_code()
                else:
                    print("Invalid Input")
                    return run_ad_menu()
            run_ad_menu()
        elif ad_log=='fail':
            print("No more Attempts!\nReturning to Home!")
            return main_code()
            
            
    elif welc_page=='2':
        Voter_id=voter_flow.voter_login()
        if Voter_id=="fail":
            print("\nReturning to Home\n")
            return main_code()
        else:
            def voter_methods():
                voter_choice=voter_flow.voter_menu()
                if voter_choice=='4':
                    print("\nReturning to Home\n")
                    return main_code()
                elif voter_choice=='1':
                    elec_time=validations.check_time(Voter_id)                
                    if elec_time=="over":
                        print("\nElection Poll Closed!\n")
                        
                        def over_options():
                            over_menu=input("Press\n1 to CHECK RESULT\n2 to Return to Menu")
                            if over_menu=="1":
                                voter_flow.check_result(Voter_id)
                                print("\nReturning to Menu\n")
                                return voter_methods()
                            elif over_menu=="2":
                                print("\nThank You!\n")
                                return voter_methods()
                            else:
                                print("Invalid Input!")
                                return over_options()
                        over_options()
                    elif elec_time=="not_started":
                        print("\nPoll hasnt Begun Yet!\n")
                        print("\nReturning to Menu\n")
                        return voter_methods()
                    elif elec_time=="proceed":
                        def c_vote():
                            if validations.check_attempt(Voter_id):
                                cvote=voter_flow.cast_vote(Voter_id)
                                if cvote=="recall":
                                    c_vote()
                                else:
                                    print("\nReturning to Menu\n")
                                    return voter_methods()
                            else:
                                print("\nYou have already cast your vote!\n")
                                print("\nReturning to Menu\n")
                                return voter_methods()
                        c_vote()
                        
                            
                elif voter_choice=='2':
                    if validations.check_time(Voter_id)=='over':
                        voter_flow.check_result(Voter_id)
                        print("\nReturning to Menu\n")
                        return voter_methods()
                    else:
                        print("\nPolling not Complete yet!\n")
                        print("\nReturning to Menu\n")
                        return voter_methods()
                elif voter_choice=='3':
                    if validations.check_time(Voter_id)=='over':
                        print("\nElection has Ended!\n")
                        voter_flow.check_result(Voter_id)
                        print("\nReturning to Menu\n")
                        return voter_methods()
                    else:
                        voter_flow.live_poll(Voter_id)                        
                        print("\nReturning to Menu\n")
                        return voter_methods()
                else:
                    print("Invalid Input!")
                    print("\nReturning to Menu\n")
                    return voter_methods()
 
        voter_methods()
                                                                                            
    elif welc_page=='3':
        print("Thank you!")
        
    elif welc_page=='0':
        print("Invalid Input!")
        return main_code()
            
            