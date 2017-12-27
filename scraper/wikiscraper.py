import urllib
import lxml.etree
import urllib
from bs4 import BeautifulSoup
import sys, traceback

#authors: Vinit Gupta, Akshat Dave

def get_links(category_url):
	id_names = ['mw-pages'] #'mw-subcategories',

	soup = get_url_data_soup(category_url)

	link_entries = []
	for id_name in id_names:
		data = soup.findAll('div',attrs={'id':id_name})
		for div in data:
		    links = div.findAll('a')
		    for a in links:
		       link_entries.append(a['href'])
	return (link_entries)

def make_text_from_para_soup(para_soup):
	para_data = []
	for para in para_soup:
		para_data.append(para.text)
	return para_data

def write_to_file(write_filename, para_data):

	fptr = open(write_filename,'w')
	for line in para_data:
		line_data = line+'\n'
		fptr.write(line_data.encode('utf-8').strip())
	fptr.close()


def bfs_url(root_url, page_url, level, write_text_path):
	#TODO: make as params
	WIKI = 'wiki'
	cat_name = 'legal_'
	if level<=0:
		# done with traveral 
		return

	body_data_soup = extract_text_content(make_url (root_url, page_url))

	outgoing_links = get_links_from_paras(body_data_soup)

	para_data = make_text_from_para_soup(body_data_soup)

	name_from_url = cat_name+ page_url[page_url.rfind('/')+1:]
	write_filename = write_text_path+ '/' + name_from_url +'.txt'
	write_filename = write_filename.encode('utf-8').strip()
	print 'writing to path = {}'.format(write_filename)

	try:
		write_to_file(write_filename,para_data)
	except:
		print 'exception in file creation'
		traceback.print_exc(file=sys.stdout)
		return
	#print (para_data)

	
	for out_link in outgoing_links:
		if out_link.startswith(WIKI):
			print str(out_link.encode('utf8'))+'\n'
			bfs_url(root_url, out_link, level-1, write_text_path)
	

def get_links_from_paras(text_content):

	link_entries = []
	for chunk in text_content:
		links = chunk.findAll('a')
		for a in links:
			link_entries.append(a['href'])
	return link_entries

def get_url_data_soup(page_url):
	page_data =  urllib.urlopen(page_url).read()
	return BeautifulSoup(page_data,'html.parser')

def make_url(root, rel_path):
	return ''.join([root,rel_path])

def extract_text_content(page_url):
	soup = get_url_data_soup(page_url)
	body_data_soup = soup.find_all('p')
	return body_data_soup



# main code starts here
def main():
	categories = [
	'https://en.wikipedia.org/wiki/Category:Government'
	]

	root_url = 'https://en.wikipedia.org'
	write_path = './scrapedata'
	for category in categories:
		page_links = get_links(category)

		for pid in page_links:
			print 'url info : {}'.format(pid)
			bfs_url(root_url, pid, 2, write_path)	

# main code starts here
main()