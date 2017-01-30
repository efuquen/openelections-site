import webapp2
import csv
import StringIO
import json

def process_csv_data(csv_data):
    precinct_to_votes = {}
    is_header = True
    f = StringIO.StringIO(csv_data)
    rows = csv.reader(f, delimiter=',')
    for row in rows:
        if is_header:
          is_header = False
          continue
        #TODO: Write your code here.
    return precinct_to_votes


class UploadHandler(webapp2.RequestHandler):
    def post(self):
        csv_data = self.request.POST.get('csv_file').file.read()
        results = process_csv_data(csv_data)
        for key in results:
            self.response.out.write(json.dumps(results[key]) + "<br>")

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
