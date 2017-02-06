import webapp2
import csv
import StringIO
import json

from google.appengine.ext import ndb

def csv_string_to_dict(csv_data):
    precinct_to_votes = {}
    is_header = True
    f = StringIO.StringIO(csv_data)
    rows = csv.reader(f, delimiter=',')
    for row in rows:
        if is_header:
          is_header = False
          continue
        office = row[2]
        if office != 'President':
          continue
        county = row[0]
        precinct = row[1]
        key = county + '__' + precinct
        entry = precinct_to_votes.get(key, {})
        precinct_to_votes[key] = entry
        entry['county'] = county
        entry['precinct'] = precinct

        precinct_votes = entry.get('votes', {})
        entry['votes'] = precinct_votes

        candidate = row[5]
        votes = int(row[6])
        if candidate in precinct_votes:
          precinct_votes[candidate] += votes
        else:
          precinct_votes[candidate] = votes
    return precinct_to_votes

class PrecinctVotes(ndb.Model):
    precinct = ndb.StringProperty()
    county = ndb.StringProperty()
    votes = ndb.JsonProperty()

class UploadHandler(webapp2.RequestHandler):
    def post(self):
        csv_data = self.request.POST.get('csv_file').file.read()
        precinct_to_votes = csv_string_to_dict(csv_data)
        for key in precinct_to_votes:
            entry = precinct_to_votes[key]
            precinct = entry['precinct']
            county = entry['county']
            votes = entry['votes']
            precinct_vote = PrecinctVotes(
                id=key, county=county, precinct=precinct, votes=votes)
            precinct_vote.put()
        self.response.status_int = 302
        self.response.headers['Location'] = '/'

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class PrecinctHandler(webapp2.RequestHandler):
    def get(self):
        county = self.request.get('county', None)
        precinct = self.request.get('precinct', None)
        results = []
        if county and precinct:
            key = county + '__' + precinct
            entry = PrecinctVotes.get_by_id(key)
            results.append(entry.to_dict())
        elif county:
            for entry in PrecinctVotes.query(PrecinctVotes.county == county):
                results.append(entry.to_dict())
        elif precinct:
            for entry in PrecinctVotes.query(PrecinctVotes.precinct == precinct):
                results.append(entry.to_dict())
        else:
            results = []
            for entry in PrecinctVotes.query():
                results.append(entry.to_dict())
        self.response.out.write(json.dumps(results))
        self.response.headers.add_header('Content-Type', 'application/json')
        self.response.headers.add_header(
          'Access-Control-Allow-Origin', '*')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/upload', UploadHandler),
    ('/precincts', PrecinctHandler)
], debug=True)
