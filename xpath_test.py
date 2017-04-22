import requests
from lxml import etree
import os

LOGIN_URL = 'https://github.com/login'
SESSION_URL = 'https://github.com/session'
s = requests.session()
r = s.get(LOGIN_URL)
tree = etree.HTML(r.text)
el = tree.xpath('//input[@name="authenticity_token"]')[0]
authenticity_token = el.attrib['value']
data = {
    'commit' : 'Sign in',
    'utf8' : '✓',
    'authenticity_token' : authenticity_token,
    'login' : os.environ['LOGIN'],
    'password' : os.environ['PASSWORD']
}
r = s.post(SESSION_URL, data=data)
tree = etree.HTML(r.text)
el = tree.xpath('//ul[@id="repo_listing"]')[0]
el.xpath('//li[contains(@class, "public")]')
print (el.xpath('//span[@class="repo"]')[0].text)
# print (tree.xpath('//ul[@id="repo_listing//li[contains(@class, "public")]//span[@class="repo"]')[0].text)