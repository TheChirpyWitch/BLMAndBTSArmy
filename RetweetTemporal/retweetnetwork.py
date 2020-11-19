'''
MIT License
Copyright (c) 2019 Luca Hammer
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

'''
Example script to create a dynamic network gexf file for Gephi from a jsonl file
Article: https://lucahammer.com/?p=367

To use this script, change the constants (UPPERCASE variables) to your needs,
and run it. For example in your CLI by executing: "python retweetnetwork.py".
'''

# name of the file with the Tweet objects
#JSONL_FILE = 'twitter_premium_api_demo.jsonl'
JSONL_FILE = '../data_dump/tweetsData.jsonl'

# name of the file that will be created/overwritten by the script
GEXF_FILE = 'demo_network.gexf'

#--------------------------- STOP -------------------------------#
# Don't edit anything below, if you don't know what you are doing.
#--------------------------- STOP -------------------------------#

import json_lines

def load_jsonl(file):
    tweets = []
    with open(file, 'rb') as f:
        for tweet in json_lines.reader(f, broken=True):
            reduced_tweet = {
                'created_at': tweet['created_at'],
                'id': tweet['id_str'],
                'username': tweet['user']['screen_name'],
                'user_joined': tweet['user']['created_at'][-4:],
                'user_id': tweet['user']['id_str'],
            }

            if 'derived' in tweet['user']:
                reduced_tweet['country'] = tweet['user']['derived']['locations'][0]['country'] \
                    if 'locations' in tweet['user']['derived'] else ""
                reduced_tweet['region'] = tweet['user']['derived']['locations'][0]['region'] \
                    if 'region' in tweet['user']['derived']['locations'][0] else ""

            if 'retweeted_status' in tweet:
                reduced_tweet['retweeted_user'] = {
                    'user_id': tweet['retweeted_status']['user']['id_str'],
                    'username': tweet['retweeted_status']['user']['screen_name'],
                    'user_joined': tweet['retweeted_status']['user']['created_at'][-4:]
                }

            tweets.append(reduced_tweet)
    return (tweets)
    
tweets = load_jsonl(JSONL_FILE)

import datetime
import lxml.etree as etree

def create_gexf(tweets, filename):
    attr_qname = etree.QName(
        "http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")

    gexf = etree.Element('gexf',
                         {attr_qname: 'http://www.gexf.net/1.3draft  http://www.gexf.net/1.3draft/gexf.xsd'},
                         nsmap={
                             None: 'http://graphml.graphdrawing.org/xmlns/graphml'},
                         version='1.3')

    graph = etree.SubElement(gexf,
                             'graph',
                             defaultedgetype='directed',
                             mode='dynamic',
                             timeformat='datetime')
    attributes = etree.SubElement(
        graph, 'attributes', {'class': 'node', 'mode': 'static'})
    etree.SubElement(attributes, 'attribute', {
                     'id': 'country', 'title': 'country', 'type': 'string'})
    etree.SubElement(attributes, 'attribute', {
                     'id': 'region', 'title': 'region', 'type': 'string'})
    etree.SubElement(attributes, 'attribute', {
                     'id': 'year', 'title': 'year', 'type': 'integer'})

    nodes = etree.SubElement(graph, 'nodes')
    edges = etree.SubElement(graph, 'edges')

    for tweet in reversed(tweets):
        node = etree.SubElement(nodes,
                                'node',
                                id=tweet['user_id'],
                                Label=tweet['username'],
                                start=datetime.datetime.strptime(tweet['created_at'], '%a %b %d %X %z %Y').isoformat(
                                    timespec='seconds'),  # Fri Jul 27 07:52:57 +0000 2018
                                end=(datetime.datetime.strptime(
                                    tweet['created_at'], '%a %b %d %X %z %Y') + datetime.timedelta(seconds=1)).isoformat(timespec='seconds')
                                )
        attvalues = etree.SubElement(node, 'attvalues')
        etree.SubElement(attvalues,
                         'attvalue',
                         {'for': 'year',
                          'value': tweet['user_joined']
                          }
                         )
        if 'region' in tweet:
            etree.SubElement(attvalues,
                             'attvalue',
                             {'for': 'region',
                              'value': tweet['region']
                              }
                             )
        if 'country' in tweet:
            etree.SubElement(attvalues,
                             'attvalue',
                             {'for': 'country',
                              'value': tweet['country']
                              }
                             )
        if 'retweeted_user' in tweet:
            etree.SubElement(edges,
                             'edge',
                             {'id': tweet['id'],
                              'source': tweet['retweeted_user']['user_id'],
                              'target': tweet['user_id'],
                              # Fri Jul 27 07:52:57 +0000 2018
                              'start': datetime.datetime.strptime(tweet['created_at'], '%a %b %d %X %z %Y').isoformat(timespec='seconds'),
                              'end': (datetime.datetime.strptime(tweet['created_at'], '%a %b %d %X %z %Y') + datetime.timedelta(seconds=1)).isoformat(timespec='seconds')
                              }
                             )
            node = etree.SubElement(nodes,
                                    'node',
                                    id=tweet['retweeted_user']['user_id'],
                                    Label=tweet['retweeted_user']['username'],
                                    start=datetime.datetime.strptime(tweet['created_at'], '%a %b %d %X %z %Y').isoformat(
                                        timespec='seconds'),  # Fri Jul 27 07:52:57 +0000 2018
                                    end=(datetime.datetime.strptime(
                                        tweet['created_at'], '%a %b %d %X %z %Y') + datetime.timedelta(seconds=1)).isoformat(timespec='seconds')
                                    )
            attvalues = etree.SubElement(node, 'attvalues')
            etree.SubElement(attvalues,
                             'attvalue',
                             {'for': 'year',
                              'value': tweet['retweeted_user']['user_joined']
                              }
                             )

    with open(filename, 'w', encoding='utf-8')as f:
        f.write(etree.tostring(gexf, encoding='utf8',
                               method='xml').decode('utf-8'))
    print('Created gexf.')


create_gexf(tweets, GEXF_FILE)

