

function randomString(len, charSet) {
    charSet = charSet || 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var randomString = '';
    for (var i = 0; i < len; i++) {
        var randomPoz = Math.floor(Math.random() * charSet.length);
        randomString += charSet.substring(randomPoz,randomPoz+1);
    }
    return randomString;
}

function encrypt_aes_key(key){
    var publicKey = forge.pki.publicKeyFromPem(sessionStorage.getItem("key"));
    var encrypted = publicKey.encrypt(key, "RSA-OAEP", {
                md: forge.md.sha256.create(),
                mgf1: forge.mgf1.create()
            });
    var base64 = forge.util.encode64(encrypted);
    return base64
}


function generate_aes_key_iv(){
    var key = randomString(16);
    var iv = randomString(16);
    sessionStorage.setItem("iv", iv);
    sessionStorage.setItem("aes_key", key);
    console.log(key);
 
}
function encrypt_aes(msg){
    var key = sessionStorage.getItem("aes_key");
    var iv = sessionStorage.getItem("iv");
    key = CryptoJS.enc.Utf8.parse(key);
    iv = CryptoJS.enc.Utf8.parse(iv);
    var encrypted = CryptoJS.AES.encrypt(msg, key, { iv: iv, mode: CryptoJS.mode.CBC});
    return encrypted.toString();
}

function send_aes_iv(){
    const requestObject = new XMLHttpRequest();
    requestObject.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            console.log(this.responseText);
        }
    }
    requestObject.open("POST", "");
    requestObject.setRequestHeader("type", "iv");
    var data = sessionStorage.getItem("iv");
    requestObject.send(encrypt_aes_key(data));
}

function send_aes_key(){
    generate_aes_key_iv();
    const requestObject = new XMLHttpRequest();
    requestObject.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            console.log(this.responseText);
            
        }
    }

    requestObject.open("POST", "");
    requestObject.setRequestHeader("type", "aes_key");
    var data = sessionStorage.getItem("aes_key");
    requestObject.send(encrypt_aes_key(data));
    send_aes_iv();

}



function send_image(image){
    const requestObject = new XMLHttpRequest();
    requestObject.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            console.log(this.responseText);
            if(this.responseText == "Stop session!"){
                stop_camera();
            }
        }
    }

    

    requestObject.open("POST", 'post/');
    image = encrypt_aes(image);
    requestObject.send(image);


}

async function camera_button() {
   	let stream = null;
	
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = stream;
    } catch (err) {
        /* handle the error */
    }
}
var intervalID = 0;
function click_button() {
    intervalID = window.setInterval(click_button_fun, 1500);
}
function stop_camera(){
    clearInterval(intervalID);
}

function click_button_fun() {
   	canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
   	let image_data_url = canvas.toDataURL('image/jpeg');
    send_image(image_data_url);
   	//data url of the image
   	//console.log(image_data_url);
    
}


function send_nr_matricol(){

    let nr_matr = document.getElementById('nr_matr').value
    const requestObject = new XMLHttpRequest();
    requestObject.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            console.log(this.responseText);
            sessionStorage.setItem("key", this.responseText);
            send_aes_key();
            window.location = "https://192.168.100.32:8080/main/";
        }
    }
    requestObject.open("POST", "");
    requestObject.setRequestHeader("type", "id");
    requestObject.send(nr_matr);
    

}

function send_subject(){
    
    const requestObject = new XMLHttpRequest();
    requestObject.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            console.log(this.responseText);
            window.confirm("A session for: " + this.responseText + " will start!");
        }
    }
    requestObject.open("POST", "");
    requestObject.setRequestHeader("type", "subject");
    data = ""
    requestObject.send(data);
}
/*
function send_datetime(){
    const requestObject = new XMLHttpRequest();
    requestObject.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            console.log(this.responseText);
        }
    }
    requestObject.open("POST", "");
    requestObject.setRequestHeader("type", "datetime");
    data = document.getElementById('datetime').value 
    requestObject.send(data);
}*/

function stop_session(){
    const requestObject = new XMLHttpRequest();
    requestObject.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200){
            console.log(this.responseText);
        }
    }
    requestObject.open("POST", "");
    requestObject.setRequestHeader("type", "stop_session");
    data = "true";
    requestObject.send(data);
}

