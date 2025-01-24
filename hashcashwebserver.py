import os
import socket
import threading
import time
import os


socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created successfully')
port = int(os.environ.get("PORT"))
socket.bind(('0.0.0.0',port))
def ip_and_port():
    import socket
    print(f'the port is {port} and the ip is {socket.gethostbyname(socket.gethostname())}')
ip_and_port()
socket.listen(6)
print("Listening to 6 clients")
def signup(c):
    global menu_msg
    c.send('Please type your username below'.encode())
    while True:

        username = c.recv(1024).decode()
        with open('accounts.txt','r') as file:
            for line in file:
                if  line.strip():
                    username_,password,fullname,age,job,country,city,balance= line.strip().split(',')
                    #print(f'{username_}')
                    if username_ == username:
                        c.send('This username is already in use.Please enter another one'.encode())
                        break
        if len(username) <3 or  len(username)>8:
            c.send('username should not be less than 3 characters or greater than 8 characters.Please enter another one.'.encode())

        else: break
    c.send('Please enter your password'.encode())
    password = c.recv(1024).decode()
    c.send('please enter your full name'.encode())
    fullname = c.recv(1024).decode()
    c.send('please enter your age'.encode())
    age = c.recv(1024).decode()
    c.send('please enter your job'.encode())
    job = c.recv(1024).decode()
    c.send('please enter your contry'.encode())
    country = c.recv(1024).decode()
    c.send('please enter your city'.encode())
    city = c.recv(1024).decode()
    balance = 1
    try:
        with open('accounts.txt','a') as file:
            file.write(f"\n{username},{password},{fullname},{age},{job},{country},{city},{balance}\n")
            return True,username,'account created successfully'
    except Exception as e:
        c.send(menu_msg)
        return False,username,e


def user_msg(msg,addr):
    print(f'{addr}=> {msg}')


menu_msg = """
     Welcome to HASHCASH
1.My Profile
2.Send Money
3.Cash In
4.Mobile Recharge
5.Cashout
6.Add Money
7.Logout
8.exit"""

def myprofile(c,username):
    with open('accounts.txt','r') as file :
        for line in file:
            if line.strip():
                username_, password, fullname, age, job, country, city, balance = line.strip().split(',')
                if username_ == username:
                    print(f'{username} found')
                    c.send(f"""username : {username}
Full name: {fullname}
Age : {age}
Job : {job}
Country : {country}
City : {city}
Balance : {balance}$""".encode())
                    print(f'my_profile send to {username} ')


def login(c):
    c.send('Enter your username'.encode())
    username = c.recv(1024).decode()
    print(f'{username} is trying to login')
    username_found = False
    retry = 0
    with open('accounts.txt','r') as file:
        for line in file:
            if line.strip():
                username_, password_, fullname, age, job, country, city, balance = line.strip().split(',')
                if username_ == username:
                    username_found = True
                    c.send('Please enter your password'.encode())
                    while retry<=6:
                        password = c.recv(1024).decode()
                        if password == password_:
                            print(f'{username} logged on at {time.time()}')
                            return True,username,'Logged in successfully'
                        else:
                            c.send("The password is incorrect. Please try again".encode())
                            retry += 1
        if not username_found:
            return False,None,'Username not found.Press enter to continue.'

def send_money(c,sender_username):


    valid_amount = False
    valid_username = False
    while True:
        c.send('Enter the ammount to send'.encode())
        amount= c.recv(1024).decode()
        try:
            if int(amount) <= 0 :
                c.send('Please enter a valid value.(Press enter to continue)'.encode())
                c.recv(1024)
            else:
                valid_amount = True
                break
        except ValueError:
            c.send('Please enter a valid value.(press enter to continue).'.encode())
            c.recv(1024)


    c.send('Enter the receivers username'.encode())
    retry_ = 0
    while retry_ <6:
        receiver_username = c.recv(1024).decode()
        if receiver_username == sender_username:
            c.send('Sorry. But you cant send money to yourself(Press Enter to continue)'.encode())
            c.recv(1024)
            retry_ += 1
        else: 
            valid_username = True
            break

    receiver_username_found = False
    sender_username_found = False
    receiver_balance = 0
    sender_balance = 0
    accounts = []
    if valid_amount and valid_username:
        with open('accounts.txt','r') as file:
            for line in file:
                if line.strip():
                    username_, password_, fullname, age, job, country, city, balance = line.strip().split(',')
                    if username_ == receiver_username:
                        receiver_username_found = True
                        receiver_balance = int(balance)
                    if username_ == sender_username:
                        sender_username_found = True
                        sender_balance = int(balance)
                    accounts.append([username_, password_, fullname, age, job, country, city, balance ])
        if not receiver_username_found:
            c.send('Receiver username not found'.encode())
            c.recv(1024)
        if receiver_username_found and sender_username_found and int(sender_balance) >= int(amount):
            text = f"""Summary
                Receiver name :{receiver_username}
                Total spend :{amount}
                New balance : {int(sender_balance) - int(amount) }
                Reply 'y' to confirm('n' to abort)"""
            c.send(text.encode())
            confirmation = c.recv(1024).decode().lower()
            if int(sender_balance) >= int(amount):
                if confirmation in ['y','yes']:
                    sender_balance -= int(amount)
                    receiver_balance += int(amount)
                    print('send money confirmed')
                    for account in accounts:

                        if account[0] == sender_username:
                            account[7] = sender_balance
                        if account[0] ==  receiver_username:
                            account[7] = receiver_balance
                        print('balance updated at list')
                    try:
                        with open('accounts.txt','w') as file:

                            for account in accounts:
                                accountline = ''
                                for item in account:
                                    accountline += str(item)+','
                                accountline = accountline.rstrip(',')
                                file.write(accountline+'\n')
                            print(f'{sender_username} has sucessfully sent {amount}$ to {receiver_username}')
                            c.send('send money successful (Press Enter to continue)'.encode())
                            c.recv(1024)
                    except Exception as e:
                        print(f"There was an error while {sender_username} was trying to send money to {receiver_username}: {e}")
                        c.send('an error occurred (Press Enter to continue)'.encode())
                        c.recv(1024)
        else:
            c.send(' Unsufficient balance (Press Enter to continue)'.encode())
            c.recv(1024)









def handle_client(c,addr):
    c_logged = False
    try:
        while True:
            if not c_logged:
                c.send("""        WELCOME TO HASHCASH
                    Please Login or Signup to Continue!
                    1.Signup
                    2.Login
                    3.Exit""".encode())
                c_r = c.recv(1024).decode()
                print(f'{addr}=> {c_r}')
                if c_r == '1':
                    c_logged,username,msg = signup(c)
                    c.send(msg.encode())
                    c.recv(1024)
                elif c_r == '2':
                    c_logged,username,msg = login(c)
                    c.send(msg.encode())
                    c.recv(1024)
                elif not c_r:
                    print(f'{addr} has disconnected')
                    break
    


            elif c_logged:
    
                c.send(menu_msg.encode())
                to_do = c.recv(1024).decode()
                user_msg(to_do,addr)
                if to_do == '1':
                    myprofile(c,username)
                    #c.send(menu_msg.encode())
                    c.recv(1024)
    
                elif to_do == '2':
                    send_money(c,username)
                elif not to_do:
                    print(f'{username} has disconnected')
                    break
    except Exception as e: print(f'an error occurred {e}')
    finally:
        c.close()
        print(f"{addr} has disconnected")



while True:
    c,addr = socket.accept()
    print(f'A client connected successfully from {addr}')
    thread = threading.Thread(target=handle_client,args=(c,addr))
    thread.start()
