var user_id_12 = "";

function getUniqueStr(){
    return ("000000"+(Math.floor(100050000*Math.random())).toString(16)).slice(-6)+("000000"+parseInt((Math.round(new Date().getTime()*7)%100000000)).toString(16)).slice(-6)
}

function load() {
    var value = "";
    if(!localStorage.getItem('pan_userid')) {
      value = getUniqueStr();
    } else {
      value = localStorage.getItem('pan_userid');
    }
    user_id_12 = value;
    console.log("loaded"+user_id_12)
}

// 保存
function save() {
  var value = user_id_12;
  localStorage.setItem('pan_userid', value);
  chrome.storage.local.set({'pan_userid': value}, function () {
    console.log("saved id = "+ value)
  });
}

const loop = setInterval(() => {
  if (document.querySelector(".cs-version")) {
    document.querySelector(".cs-version").insertAdjacentHTML("afterend", '<p class="user_id">連携用 User ID = <span id="input_id"></span></p>');
    load()
    document.getElementById('input_id').innerHTML = user_id_12 ;
    save()
    clearInterval(loop)
  }
}, 100)
