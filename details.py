def obtenerDetalle(url):
	request = urllib.request.Request(url)
	request.add_header('User-agent', 'Mozilla/5.0 (Linux i686)')
	html = urllib.request.urlopen(request)
	soup = BeautifulSoup(html ,  "html.parser")
	rows = soup.find(id="table-center").find("tbody").find_all("tr")

	for row in enumerate(rows):
		print('experiment' +str(row))