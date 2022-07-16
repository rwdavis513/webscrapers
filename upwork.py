import requests
from bs4 import BeautifulSoup


url = 'https://www.upwork.com/ab/feed/jobs/rss?budget=5000-100000&category2=web_mobile_software_dev&contractor_tier=2%2C3&api_params=1&q=&securityToken=c7f71498e95155d17d00645cdaabcb2e52e1a8cd88c9c3b712dc46d2a753aa40d4cbe312f13f4e3afdf563ba890a461481f346ec79e825aca082707201e8db3e&userUid=700749838806134784&orgUid=700750819111723009'

r = requests.get(url)


if r.status_code >= 200 and r.status_code < 300:
    data = r.content
    soup = BeautifulSoup(data, 'html.parser')

