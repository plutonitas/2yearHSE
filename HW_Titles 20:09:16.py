import urllib.request
import re
req = urllib.request.Request('http://www.elabuga-rt.ru')
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
    
regextitles = re.compile('<h3><a class="moduleItemTitle".*?>(.*?)</a></h3>', flags = re.DOTALL)
titles = regextitles.findall(html)

titles_file = open('titles.txt','w', encoding = 'utf-8')
print(titles)
#titles_file.write(titles)
