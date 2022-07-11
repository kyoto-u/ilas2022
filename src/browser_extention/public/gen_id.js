var uuid = "";
function getUniqueStr(myStrong){
    var strong = 1000;
    if (myStrong) strong = myStrong;
    return new Date().getTime().toString(16)  + Math.floor(strong*Math.random()).toString(16)
}

function load() {
    var mydata = "";
    if(!localStorage.getItem('mydata')) {
      mydata = getUniqueStr(12);
    } else {
      mydata = localStorage.getItem('mydata');
    }
    uuid = mydata;
    console.log("loaded"+uuid)
}

// 保存
function save() {
  var mydata = uuid;
  console.log(`saved_uuid`+uuid);
  localStorage.setItem('mydata', mydata);
}


document.addEventListener('DOMContentLoaded', function() {
    load()
    document.getElementById('input_id').innerHTML = uuid ;
    save()
});