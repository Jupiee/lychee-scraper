from curl_cffi import requests
from urllib.parse import urlparse
from selectolax.lexbor import LexborHTMLParser
import requests as req
import re

class Extractor:
    
	def __init__(self):

		self.session= requests.Session()

		self.session.headers.update({
			'authority': 'ouo.io',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
			'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
			'cache-control': 'max-age=0',
			'referer': 'http://www.google.com/ig/adde?moduleurl=',
			'upgrade-insecure-requests': '1',
		})

	def RecaptchaV3(self):

		ANCHOR_URL = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8ucHJlc3M6NDQz&hl=en&v=pCoGBhjs9s8EhFOHJFe8cqis&size=invisible&cb=ahgyd1gkfkhe'
		url_base = 'https://www.google.com/recaptcha/'
		post_data = "v={}&reason=q&c={}&k={}&co={}"

		client = req.Session()
		client.headers.update({
			'content-type': 'application/x-www-form-urlencoded'
		})

		matches = re.findall('([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
		url_base += matches[0]+'/'
		params = matches[1]
		res = client.get(url_base+'anchor', params=params)
		token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
		params = dict(pair.split('=') for pair in params.split('&'))
		post_data = post_data.format(params["v"], token, params["k"], params["co"])
		res = client.post(url_base+'reload', params=f'k={params["k"]}', data=post_data)
		answer = re.findall(r'"rresp","(.*?)"', res.text)[0]

		return answer

	def bypass(self, url):

		parsed_url= urlparse(url)
		identifier= url.split("/")[-1]

		response= self.session.get(url, impersonate= "chrome110")

		directed_url= f"{parsed_url.scheme}://{parsed_url.hostname}/go/{identifier}"

		for i in range(2):

			if response.headers.get("location"):
				
				break
			
			crawler= LexborHTMLParser(response.content)
			forms= crawler.css("form")

			input_tags= [form.css("input[type='hidden']") for form in forms][0]

			data= {input_tag.attrs["name"]: input_tag.attrs["value"] for input_tag in input_tags}

			data["x-token"]= self.RecaptchaV3()

			headers= {'content-type': 'application/x-www-form-urlencoded'}

			response= self.session.post(directed_url, data=data, headers=headers, allow_redirects=False, impersonate= "chrome110")

			directed_url= f"{parsed_url.scheme}://{parsed_url.hostname}/xreallcygo/{identifier}"

		return response.headers.get("Location")
	
extractor= Extractor()

print(extractor.bypass("https://ouo.io/fFlW96"))
