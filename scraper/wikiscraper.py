import urllib
import lxml.etree
import urllib
from bs4 import BeautifulSoup
import sys, traceback
import os.path
#authors: Vinit Gupta, Akshat Dave

def is_valid_link(link):
	WIKI = '/wiki'

	if link.startswith(WIKI):
		print 'Valid link = {}'.format(link)
		return True
	return False

def get_links(root_url,category_url, tag_name):
	id_names = [tag_name] #'mw-subcategories',

	soup = get_url_data_soup(make_url(root_url,category_url))

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

	if os.path.isfile(write_filename):
		print 'file exists'
		return
	
	fptr = open(write_filename,'w')
	for line in para_data:
		line_data = line+'\n'
		fptr.write(line_data.encode('utf-8').strip())
	fptr.close()


def bfs_url(root_url, page_url, level, write_text_path, category):

	cat_name = category+'_'
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
		if is_valid_link(out_link):
			print str(out_link.encode('utf8'))+'\n'
			bfs_url(root_url, out_link, level-1, write_text_path, cat_name)


def get_links_from_paras(text_content):

	link_entries = []
	for chunk in text_content:
		links = chunk.findAll('a')
		for a in links:
			if 'href' in a:
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

	tag_dict = {}
	tag_dict['pages'] = 'mw-pages'
	tag_dict['subcats'] = 'mw-subcategories'



	cat_map = {
	'legal': '/wiki/Category:Government',
	'health': '/wiki/Category:Health'
	} 

	root_url = 'https://en.wikipedia.org'
	write_path = '../../scrapedata'
	for category in cat_map:

		full_write_path = '/'.join([write_path,category])
		subcat_links = get_links(root_url,cat_map[category],tag_dict['subcats'])
		subcat_links.append(cat_map[category]) # adding the category 
		# collect data for pages
		for sid_url in subcat_links:
			print 'subcat url info : {}'.format(sid_url)
			if not is_valid_link(sid_url):
				print '{} *****invalid link'.format(sid_url)
				continue
			
			#bfs_url(root_url, sid, 2, write_path)

			page_links = get_links(root_url,sid_url,tag_dict['pages'])

			if page_links is None or len(page_links)==0:
				continue
			# collect data for pages
			for page_link in page_links:

				if not is_valid_link(page_link):
					continue
				print 'url info : {}'.format(page_link)
				bfs_url(root_url, page_link, 2, full_write_path, category)	

# main code starts here
main()