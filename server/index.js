const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
require('dotenv').config();
const express = require('express')
var UAParser = require('ua-parser-js');
const {v1: uuidv1, v4: uuidv4} = require('uuid');

const app = express()
const port = process.env.PORT || 3000

// Add CORS and better error handling
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

const mongoose = require('mongoose');
const bodyParser = require('body-parser');

// ENTER YOUR MONGO CLUSTER URI HERE
const uri = process.env.MONGODB_URI || 'mongodb://localhost:27017/'

// for mongo
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

//connnects to mongoDb
mongoose.connect(uri, { 
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => {
  console.log('MongoDB connected successfully');
}).catch(err => {
  console.error('MongoDB connection error:', err);
});

// /schema for the mongo json
const notesSchema = {
  title: String,
  dateTime: String,
  uuid: String,
  counter: Number,
  stats: String
}

//assigns schema to mongodb
const Note = mongoose.model('email-tracker', notesSchema);
// Note.remove({}).exec()    //  removes all past data on reload

// used to serve file
app.use(express.static(__dirname))

app.post('/', (req, res) => {
  async function main() {
    try {
      // Use server's local time instead of external API
      var now = new Date();
      var dateTime = now.toISOString().split("T")[0] + " " + now.toISOString().split("T")[1].split(".")[0] + ' UTC';
      
      var uuid = uuidv4()
      var newNote = new Note({
        title: req.body.title,
        dateTime: dateTime,
        uuid: uuid,
        counter: 0,
        stats: 'Null'
      });
      await newNote.save();

      res.json({ uuid: `p?uuid=${uuid}` });
    } catch (error) {
      console.error('Error in POST /:', error);
      res.status(500).json({ error: 'Internal server error', message: error.message });
    }
  }
  main()
})

// http://yourURL.com/p?uuid=
app.get('/p', function(req, res) {
  async function main() {
    try {
      var uuidParam = req.query.uuid
      var uuidParamChecker = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/.test(uuidParam)
      
      // Use server's local time and convert to IST
      var now = new Date();
      var istTime = new Date(now.getTime() + (5.5 * 60 * 60 * 1000)); // Add 5:30 for IST
      var dateTime = istTime.toISOString().split("T")[0] + " " + istTime.toISOString().split("T")[1].split(".")[0] + ' IST';

      // Get the first IP address (actual client IP, not proxy)
      var forwardedIps = req.headers['x-forwarded-for'];
      var ipAddress = 'Unknown';
      if (forwardedIps) {
        var ips = forwardedIps.split(',');
        ipAddress = ips[0].trim(); // Get the first (original) IP
      } else {
        ipAddress = req.connection.remoteAddress || 'Unknown';
      }
      
      var ip = await fetch(`http://ip-api.com/json/${ipAddress}`);
      var location = await ip.json()

      // List of known proxy/scanner IPs and organizations to ignore
      var ignoreList = [
        'Google', 'Gmail', 'Googlebot',
        'Yahoo', 'Microsoft', 'Outlook',
        'CloudFlare', 'Cloudflare',
        'AS15169',  // Google's ASN
        'Mountain View'  // Google HQ location
      ];
      
      // Check if this is a proxy/scanner (not a real user)
      var isProxy = false;
      if (location.org && ignoreList.some(term => location.org.includes(term))) {
        isProxy = true;
      }
      if (location.isp && ignoreList.some(term => location.isp.includes(term))) {
        isProxy = true;
      }
      if (location.as && ignoreList.some(term => location.as.includes(term))) {
        isProxy = true;
      }
      if (location.city && ignoreList.some(term => location.city.includes(term))) {
        isProxy = true;
      }

      // Handle missing location data
      var infoJson =  {
        time: dateTime,
        ip: location.query || ipAddress,
        country: location.country || 'Unknown',
        regionName: location.regionName || 'Unknown',
        city: location.city || 'Unknown',
        isProxy: isProxy,  // Flag to identify proxy/scanner opens
        zip: location.zip || 'Unknown',
        lat: location.lat ? location.lat.toString() : 'Unknown',
        lon: location.lon ? location.lon.toString() : 'Unknown',
        isp: location.isp || 'Unknown',
        org: location.org || 'Unknown',
        as: location.as || 'Unknown'
      }

    if (uuidParamChecker === true) {
      Note.find({uuid: uuidParam}, async function(err, notes) {
        if (notes.length === 0) {
          res.send("uuid not active");
        } else {

          var doc = await Note.findOne({uuid: uuidParam});
          // checks if the link is being clicked for the first time
          if (doc.stats == 'Null'){
            var main = await JSON.stringify(infoJson)
            // console.log(main);
            await Note.findOneAndUpdate({ uuid: uuidParam }, { stats: '[' + main.toString() + ']' });
          } else {    // if not it appends a json with the latest click data
            
            var oldArrs = await doc.stats.toString()
            var docStats = await doc.stats
            var arr = []
            var i = 0
            while (i != JSON.parse(doc.stats).length) {
              arr.push(JSON.parse(doc.stats)[i])
              i++
            }
            arr.push(infoJson)
            let final = JSON.stringify(arr)

            await Note.findOneAndUpdate({ uuid: uuidParam }, { stats: final.toString() });
          }

          Note.findOneAndUpdate({uuid: uuidParam}, {$inc : {'counter' : 1}}).exec();
          res.sendFile(__dirname + '/img.png');
        }
      })
    } else {
      res.send("please enter a valid uuid");
    }

    } catch (error) {
      console.error('Error in GET /p:', error);
      // Still send the image even if tracking fails
      res.sendFile(__dirname + '/img.png');
    }
  }
  main()
});

app.get('/data', function(req, res) {
  Note.find({}, async function(err, notes) {
    res.send(notes)
  })
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
