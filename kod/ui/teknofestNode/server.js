var app = require('express')();
var express = require('express');
var http = require('http');
var path = require('path');
const { initializeApp, cert } = require('firebase-admin/app');
const { getFirestore } = require('firebase-admin/firestore');
const { getStorage, getDownloadURL } = require('firebase-admin/storage');
const Firestore = require('@google-cloud/firestore');
const fs = require('fs');
const serviceAccount = require('./serviceAccountKey.json');

initializeApp({
  credential: cert(serviceAccount),
  storageBucket: 'teknofest-2024.appspot.com'
});
const bucket = getStorage().bucket();


/*
const aracRef = db.collection('MainCollection').doc('MseSZ123KBR4Dm7h6onc');
aracRef.get().then(function(doc) {
if (!doc.exists) {
  console.log('No such document!');
} else {
  console.log('Document data:', doc.data());
}
});
*/

function add(plaka, gpsdurumu){
  const db = getFirestore();
  const araclar = db.collection('MainCollection');
  let gps = new Firestore.GeoPoint(0,0);
  let plakanew = String(plaka).toUpperCase();
  araclar.add({
    Plaka: plakanew,
    Algilandi: 0,
    Gps: gps,
    GpsEnabled: gpsdurumu,
    sonResimAdi: ""
  }).then(() =>{
    return;
  });
}

app.use(express.static(path.join(__dirname, '/served')));
app.listen(3030);

app.post('/data', (req, res) => {
  const db = getFirestore();
  const araclar = db.collection('MainCollection');
  let aracData = {}; 
    araclar.get().then(function(snapshot){
      snapshot.forEach(doc => {
        //console.log(doc.id, '=>', doc.data());
        const newData = doc.data();
        let resimAdi = newData.sonResimAdi;
        if(resimAdi != "" && resimAdi != " "){
          const resimAdiRef = bucket.file(doc.id + "/" + resimAdi);
          const downloadURL = getDownloadURL(resimAdiRef).then(function(downloadURL){
            newData.sonResimAdi = downloadURL;
            
          });
          
        }else{
          newData.sonResimAdi = "/images/no picture.png"
        }
        
        aracData[doc.id] = newData;  

        
         
      });
      setTimeout(() => {
        res.end(JSON.stringify(aracData));
      },600); 
  }); 


 
});


app.get("/aracekleme",(req,res) => {
  let urlData = req.query;
  if(urlData.gpsstatv != undefined){
    add(urlData.plaka, true);
  }else{
    add(urlData.plaka, false);
  }
    
  res.redirect("index.html");
});