import requests
import socket
statusCode = []
urlRedirect = []
ipAddress = []
urlCounter = 0
redirectCounter = 0
ipCounter = 0

def get_url_status(urls, maxCounter):  # checks status for each url in list urls
    global statusCode, urlCounter
    for url in urls:
        urlCounter += 1
        try:
            r = requests.get(url)
            print(url + "\tStatus: " + str(r.status_code) + " - " + str(urlCounter) + "/" + str(maxCounter))
            statusCode.append(r.status_code)
        except Exception as e:
            print(url + "\tNA FAILED TO CONNECT\t" + str(urlCounter) + "/" + str(maxCounter))
            statusCode.append(1)
    return None

def get_redirect_link(urls, maxCounter):
    global urlRedirect, redirectCounter
    for url in urls:
        redirectCounter += 1
        try:
            #Check for more than one redirect
            while True:
                redirect = requests.get(url)
                doubleRedirect = requests.get(redirect.url)
                if str(redirect.url) != str(doubleRedirect.url):#Check if first redirect equals to second redirect
                    url = doubleRedirect.url
                    print(str(redirect.url) + " redirects to " + str(doubleRedirect.url) + ". Looking for more")
                else:
                    break
            if str(redirect.url) == str(url) + "/":
                urlRedirect.append("No")
                print(url + " - no redirect" + " - " + str(redirectCounter) + "/" + str(maxCounter))
            else:
                urlRedirect.append(redirect.url)
                print(url + " redirected to " + str(redirect.url) + " - " + str(redirectCounter) + "/" + str(maxCounter))
        except Exception as e:
            print(url + " error happened, no redirect" + " - " + str(redirectCounter) + "/" + str(maxCounter))
            urlRedirect.append("No")

def get_ip_address(urls, maxCounter):
    global ipAddress, ipCounter
    for url in urls:
        ipCounter += 1
        try:
            ip = socket.gethostbyname(url)
            print(url + " ip is " + ip + " - " + str(ipCounter) + "/" + str(maxCounter))
            ipAddress.append(ip)
        except Exception as e:
            print(url + " website is not online, no ip" + " - " + str(ipCounter) + "/" + str(maxCounter))
            ipAddress.append("N/A")


def main():
    global statusCode, urlCounter, ipCounter, redirectCounter

    with open('web.txt', 'r') as f:
        urls = []
        HTTPSurls = []
        ipCheck = []
        maxCounter = 0
        for line in (line.strip('\n') for line in f):
            maxCounter += 1
            ipCheck.append(line)#Add address without http so we can find ip
            result = "http://" + line
            urls.append(result)
            result = "https://" + line
            HTTPSurls.append(result)

    print("Finding IP addresses")
    get_ip_address(ipCheck, maxCounter)
    #IP results
    with open('IPoutput.txt', 'w') as file:
        for i in range(len(ipAddress)):
            file.write(str(ipAddress[i]) + "\n")
    ipCounter = 0
    print("Checking Redirects")
    get_redirect_link(urls, maxCounter)
    #Redirect Results
    with open('REDIRECToutput.txt', 'w') as file:
        for i in range(len(urlRedirect)):
            file.write(str(urlRedirect[i]) + "\n")
    redirectCounter = 0
    print("Checking HTTP Status")
    get_url_status(urls, maxCounter)
    #HTTP results
    with open('HTTPoutput.txt', 'w') as file:
        for i in range(len(statusCode)):
            if statusCode[i] == 200:
                file.write("Yes\n")
            elif statusCode[i] == 404 or statusCode[i] == 1:
                file.write("No\n")
            else:
                file.write(str(statusCode[i]) + "\n")
    statusCode = []
    urlCounter = 0
    print("Checking HTTPS Status")
    get_url_status(HTTPSurls, maxCounter)
    # HTTPS results
    with open('HTTPSoutput.txt', 'w') as file:
        for i in range(len(statusCode)):
            if statusCode[i] == 200:
                file.write("Yes\n")
            elif statusCode[i] == 404 or statusCode[i] == 1:
                file.write("No\n")
            else:
                file.write(str(statusCode[i]) + "\n")
    #urlCounter = 0

if __name__ == "__main__":
    main()


