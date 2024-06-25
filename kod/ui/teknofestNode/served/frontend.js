
const table = '<tbody  class=\"data-$a tableDataElement$\"> <tr> <td class=\"plaka\"> </td> <td class=\"algilanma\"> </td> <td class=\"konum\"> </td>   <td><a href=\"\" class=\"image_h\" > <img src=\"\" width=\"100\" height=\"100\" class=\"image\" >  </a> </td> </tr> </tbody>';
let jsonData ;
let num = 0;
let elements;
function init(){
   
        
    $.post("/data", "", (data, status) => {
        console.log(status);
        console.log(data);
        jsonData = JSON.parse(data);
        console.log(jsonData);
        aracData = Object.values(jsonData);
        keyList = Object.keys(jsonData)
        aracData.forEach(function(b){ 
            makeRow(keyList[num]); 
            document.getElementsByClassName("data-" + keyList[num]).item(0).getElementsByClassName("plaka").item(0).textContent = b.Plaka;
            document.getElementsByClassName("data-" + keyList[num]).item(0).getElementsByClassName("algilanma").item(0).textContent = b.Algilandi;
            if(b.GpsEnabled === false){
                document.getElementsByClassName("data-" + keyList[num]).item(0).getElementsByClassName("konum").item(0).textContent = "GPS devre dışı!";
            }else{
                let longitude = b.Gps._longitude;
                let latitude = b.Gps._latitude;
                let text = "Boylam " + longitude + " Enlem " + latitude;
                document.getElementsByClassName("data-" + keyList[num]).item(0).getElementsByClassName("konum").item(0).textContent = text;
            }
            document.getElementsByClassName("data-" + keyList[num]).item(0).getElementsByClassName("image").item(0).setAttribute("src",  b.sonResimAdi );
            document.getElementsByClassName("data-" + keyList[num]).item(0).getElementsByClassName("image_h").item(0).setAttribute("href", b.sonResimAdi );
            num = num + 1;
        });
    });
}
function makeRow(id){
    //console.log(id);
    var newTable = table.replace("$a",id);
    //console.log(newTable);

    document.getElementsByClassName("Durum").item(0).innerHTML = document.getElementsByClassName("Durum").item(0).innerHTML + newTable;
  
}
document.body.onload  = init();



//document.getElementsByClassName("data-1").item(0).getElementsByClassName("plaka").item(0).textContent = 'asasa'



  
