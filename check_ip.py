import requests
import json
import os
import smtplib, ssl

def get_request(url):
    response = requests.get(url)
    response_text = response.text
    return response_text

def get_external_ip():
    ip_url = "http://whatismyip.akamai.com/"
    ip = get_request(ip_url)
    return ip

def jsonify_ip(ip):
    ip_dict = {}
    ip_dict["ip"] = ip
    ip_json = json.dumps(ip_dict)
    return ip_json

def save_json_file(json_contents,output_loc):
    output_file = output_loc + "/lastest_ip.json"
    with open('latest_ip.json', 'w') as json_file:
        json.dump(json_contents, json_file)
        


def load_old_ip_from_json(json_loc):
    with open(json_loc) as json_file:
        data = json.load(json_file)
    data = json.loads(data)
    ip = data["ip"]
    return ip

def send_email(ip):
    port = 465  # For SSL
    # password = input("Type your password and press enter: ")
    password = ""
    sender_email = ""
    reciever_email = ""
    if password == "" or sender_email == "" or reciever_email == "":
        raise SyntaxError("Need to configure email details")
    message = "IP has changed to " + str(ip)
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail(sender_email, reciever_email, message)

if __name__ == "__main__":
    path = "./"
    path = os.path.realpath(path)
    old_json_loc = path + "/latest_ip.json"
    if  not os.path.isfile(old_json_loc):
        old_ip = 0.0
    else:
        old_ip = load_old_ip_from_json(old_json_loc)
    new_ip = get_external_ip()
    if old_ip != new_ip:
        send_email(new_ip)
    else:
        pass
    ip_json = jsonify_ip(new_ip)
    save_json_file(ip_json,path)

