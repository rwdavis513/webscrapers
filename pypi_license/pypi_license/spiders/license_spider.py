import scrapy

outfile =  open('pypi_scraping_results.csv', 'w')

def try_extract(response, xpath):
    """
    Attempt extracting data from the xpath and if it errors out then return an empty string
    :param response:
    :param xpath:
    :return:
    """
    try:
        license = response.xpath(xpath).extract()[0]
    except Exception as e:
        print(e)
        license = ""
    return license


class LicenseSpider(scrapy.Spider):
    name = "license"

    def start_requests(self):
        urls = [
            'https://pypi.python.org/pypi/botocore/1.7.16',
            'https://pypi.python.org/pypi/certifi/2017.7.27.1',
            'https://pypi.python.org/pypi/cffi/1.11.2',
            'https://pypi.python.org/pypi/chardet/3.0.4',
            'https://pypi.python.org/pypi/click/6.7',
            'https://pypi.python.org/pypi/colorama/0.3.7',
            'https://pypi.python.org/pypi/contexttimer/0.3.3',
            'https://pypi.python.org/pypi/cookies/2.2.1',
            'https://pypi.python.org/pypi/coverage/4.4.1',
            'https://pypi.python.org/pypi/cryptography/2.1.4',
            'https://pypi.python.org/pypi/cycler/0.10.0',
            'https://pypi.python.org/pypi/decorator/4.1.2',
            'https://pypi.python.org/pypi/docutils/0.14',
            'https://pypi.python.org/pypi/entrypoints/0.2.3',
            'https://pypi.python.org/pypi/Flask/0.12.2',
            'https://pypi.python.org/pypi/Flask-HTTPAuth/3.2.3',
            'https://pypi.python.org/pypi/Flask-SQLAlchemy/2.2',
            'https://pypi.python.org/pypi/gunicorn/19.7.1',
            'https://pypi.python.org/pypi/honeybadger/0.0.6',
            'https://pypi.python.org/pypi/html5lib/0.999999999',
            'https://pypi.python.org/pypi/idna/2.5',
            'https://pypi.python.org/pypi/ipykernel/4.6.1',
            'https://pypi.python.org/pypi/ipython/6.1.0',
            'https://pypi.python.org/pypi/ipython-genutils/0.2.0',
            'https://pypi.python.org/pypi/ipywidgets/6.0.0',
            'https://pypi.python.org/pypi/isort/4.2.15',
            'https://pypi.python.org/pypi/itsdangerous/0.24',
            'https://pypi.python.org/pypi/jedi/0.10.2',
            'https://pypi.python.org/pypi/Jinja2/2.9.6',
            'https://pypi.python.org/pypi/jmespath/0.9.3',
            'https://pypi.python.org/pypi/jsonschema/2.6.0',
            'https://pypi.python.org/pypi/jupyter/1.0.0',
            'https://pypi.python.org/pypi/jupyter-client/5.1.0',
            'https://pypi.python.org/pypi/jupyter-console/5.1.0',
            'https://pypi.python.org/pypi/jupyter-core/4.3.0',
            'https://pypi.python.org/pypi/lazy-object-proxy/1.3.1',
            'https://pypi.python.org/pypi/MarkupSafe/1.0',
            'https://pypi.python.org/pypi/matplotlib/2.0.2',
            'https://pypi.python.org/pypi/mccabe/0.6.1',
            'https://pypi.python.org/pypi/mistune/0.7.4',
            'https://pypi.python.org/pypi/nbconvert/5.2.1',
            'https://pypi.python.org/pypi/nbformat/4.3.0',
            'https://pypi.python.org/pypi/ndg-httpsclient/0.4.3',
            'https://pypi.python.org/pypi/nltk/3.2.5',
            'https://pypi.python.org/pypi/notebook/5.0.0',
            'https://pypi.python.org/pypi/numpy/1.13.1',
            'https://pypi.python.org/pypi/pandas/0.20.3',
            'https://pypi.python.org/pypi/pandocfilters/1.4.1',
            'https://pypi.python.org/pypi/passlib/1.7.1',
            'https://pypi.python.org/pypi/pexpect/4.2.1',
            'https://pypi.python.org/pypi/pickleshare/0.7.4',
            'https://pypi.python.org/pypi/prompt-toolkit/1.0.15',
            'https://pypi.python.org/pypi/psutil/5.4.3',
            'https://pypi.python.org/pypi/psycopg2/2.7.3',
            'https://pypi.python.org/pypi/ptyprocess/0.5.2',
            'https://pypi.python.org/pypi/pusher/1.7.2',
            'https://pypi.python.org/pypi/py/1.4.34',
            'https://pypi.python.org/pypi/pyasn1/0.3.3',
            'https://pypi.python.org/pypi/pycparser/2.18',
            'https://pypi.python.org/pypi/Pygments/2.2.0',
            'https://pypi.python.org/pypi/pylint/1.7.2',
            'https://pypi.python.org/pypi/pyOpenSSL/17.5.0',
            'https://pypi.python.org/pypi/pyparsing/2.2.0',
            'https://pypi.python.org/pypi/pytest/3.2.0',
            'https://pypi.python.org/pypi/pytest-cov/2.5.1',
            'https://pypi.python.org/pypi/pytest-pylint/0.7.1',
            'https://pypi.python.org/pypi/python-dateutil/2.6.1',
            'https://pypi.python.org/pypi/pytimeparse/1.1.7',
            'https://pypi.python.org/pypi/pytz/2017.2',
            'https://pypi.python.org/pypi/PyYAML/3.12',
            'https://pypi.python.org/pypi/pyzmq/16.0.2',
            'https://pypi.python.org/pypi/qtconsole/4.3.0',
            'https://pypi.python.org/pypi/redis/2.10.6',
            'https://pypi.python.org/pypi/requests/2.18.3',
            'https://pypi.python.org/pypi/responses/0.8.1',
            'https://pypi.python.org/pypi/rq/0.9.1',
            'https://pypi.python.org/pypi/rsa/3.4.2',
            'https://pypi.python.org/pypi/s3transfer/0.1.10',
            'https://pypi.python.org/pypi/scikit-learn/0.18.2',
            'https://pypi.python.org/pypi/scipy/0.19.1',
            'https://pypi.python.org/pypi/simplegeneric/0.8.1',
            'https://pypi.python.org/pypi/six/1.10.0',
            'https://pypi.python.org/pypi/sklearn/0.0',
            'https://pypi.python.org/pypi/spark-sklearn/0.2.2',
            'https://pypi.python.org/pypi/SQLAlchemy/1.1.12',
            'https://pypi.python.org/pypi/terminado/0.6',
            'https://pypi.python.org/pypi/testpath/0.3.1',
            'https://pypi.python.org/pypi/timeitd/1.0',
            'https://pypi.python.org/pypi/tornado/4.5.1',
            'https://pypi.python.org/pypi/traitlets/4.3.2',
            'https://pypi.python.org/pypi/tzlocal/1.4',
            'https://pypi.python.org/pypi/urllib3/1.22',
            'https://pypi.python.org/pypi/wcwidth/0.1.7',
            'https://pypi.python.org/pypi/webencodings/0.5.1',
            'https://pypi.python.org/pypi/Werkzeug/0.12.2',
            'https://pypi.python.org/pypi/widgetsnbextension/2.0.0',
            'https://pypi.python.org/pypi/wrapt/1.10.11',
            'https://pypi.python.org/pypi/xlrd/1.0.0'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        #filename = 'quotes-%s.html' % page

        xpaths = ['//*[@id="content"]/div[3]/ul/li[3]/span/text()',
                  '//*[@id="content"]/div[3]/ul/li[3]/ul/li[4]/a/text()'
                  ]
        #license = response.xpath().extract()[0]
        license = try_extract(response, xpaths[0])
        if license == "":
            license = try_extract(response, xpaths[1])
        outstring = page + "," + response.url + "," + license + "\n"
        print(outstring)
        outfile.write(outstring)
        ##self.log('Saved file %s' % filename)
