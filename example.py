from google.appengine.ext import ndb

class Account(ndb.Model):
    username = ndb.StringProperty()
    userid = ndb.IntegerProperty()
    email = ndb.StringProperty()
    ratings = ndb.JsonProperty()

bob = Account(
  id = "bob", # Autogenerated if missing.
  username = "bob",
  email = "bob@gmail.com",
  ratings = {
    "Rogue One": 4,
    "Hidden Figures": 5,
    "Monster Trucks": 2
  }
)
bob.put()

key = county + '__' + precinct
entry = PrecinctVotes.get_by_id(key)

queens_precints = PrecinctVotes.query(
  PrecinctVotes.county == 'Queens')
all_precincts = PrecinctVotes.query()

class PrecinctHandler(webapp2.RequestHandler):
    def get(self):
        precinct = self.request.get('precinct', None)
        if precinct:
            #CODE ..
        else:
            #CODE ..

        county = self.request.get('county', None)
        results = []
        if county and precinct:
            key = county + '__' + precinct
            entry = PrecinctVotes.get_by_id(key)
            results.append(entry.to_dict())
        else:
            for entry in PrecinctVotes.query():
                results.append(entry.to_dict())
        self.response.out.write(json.dumps(results))
        self.response.headers.add_header('Content-Type', 'application/json')
