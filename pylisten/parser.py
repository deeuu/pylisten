import os
import pandas as pd
import json


def listFiles(directory):
    filenames = os.listdir(directory)
    return [os.path.abspath(os.path.join(directory, _)) for _ in filenames]


class Parser():

    def __init__(self, path, excludes=[]):

        self.path = path

        if isinstance(excludes, str):
            self.excludes = [excludes]
        else:
            self.excludes = excludes

    def load(self, filename):
        '''
        Loads a json data file and parses the 'data' JSON string as a
        dictionary.
        '''

        with open(filename, 'r') as f:
            out = json.load(f)

        if 'name' not in out.keys():
            out['name'] = None

        out['data'] = json.loads(out['data'])

        return out

    def nullify_empty_page(self, page):

        replace_with = None
        if ('duration' not in page) or ('order' not in page):
            page['duration'] = replace_with
            page['order'] = replace_with
            page['is_replicate'] = replace_with

            for sound in page['sounds']:
                sound['value'] = replace_with

    def to_dataframe(self, data):

        frame = pd.DataFrame()

        pages = data['data']['pages']
        for page in pages:

            name = []
            value = []
            url = []

            # If we have no entry for this page, set to missing value
            self.nullify_empty_page(page)

            for sound in page['sounds']:

                name.append(sound['name'])
                url.append(sound['url'])

                value.append(sound['value'])

            temp = pd.DataFrame({'sound': name,
                                 'url': url,
                                 'value': value,
                                 'page': page['name'],
                                 'page_order': page['order'],
                                 'page_duration': page['duration'],
                                 'is_replicate': page['is_replicate'],
                                 })

            temp['on_web'] = ('http://localhost:' not in
                              data['data']['siteURL'])
            temp['experiment'] = data['experiment_id']
            temp['subject'] = data['name']

            frame = frame.append(temp)

        return frame

    def parse(self):

        if os.path.isdir(self.path):

            frame = pd.DataFrame()

            for frame_id, filename in enumerate(listFiles(self.path)):

                if (filename.endswith('.json') and
                        filename not in self.excludes):

                    result_frame = self.to_dataframe(self.load(filename))
                    result_frame['frame_id'] = frame_id
                    frame = frame.append(result_frame)
        else:

            frame = self.to_dataframe(self.load(self.path))

        return frame


class MUSHRA(Parser):

    def to_dataframe(self, data):
        '''
        Returns the mushra rating data as a Pandas DataFrame
        '''
        frame = pd.DataFrame()

        pages = data['data']['pages']
        for page in pages:

            name = []
            rating = []
            url = []

            for sound in page['sounds']:

                name.append(sound['name'])
                rating.append(sound['rating'])
                url.append(sound['url'])

            temp = pd.DataFrame({'sound': name,
                                 'url': url,
                                 'rating': rating,
                                 'page': page['name'],
                                 'page_order': page['order'],
                                 'page_duration': page['duration'],
                                 'is_replicate': page['is_replicate'],
                                 })

            temp['on_web'] = ('http://localhost:' not in
                              data['data']['siteURL'])
            temp['experiment'] = data['experiment_id']
            temp['subject'] = data['name']

            frame = frame.append(temp)

        return frame
