
def get_auth_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_uri = ""
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_uri={redirect_uri}".format(client_id=237999617, redirect_uri=redirect_uri)

    print(auth_url)

def get_access_token(code):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    import requests
    re_dict = requests.post(access_token_url, data={
        "client_id": "",
        "client_secret": "",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "",
        })



if __name__ == '__main__':
    get_auth_url()
    get_access_token("123")